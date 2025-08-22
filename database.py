import mysql.connector
from mysql.connector import Error
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv


# ----------------------
# Database configuration
# ----------------------
load_dotenv()
db_config = {
    "host": os.getenv("host"),                          # Database server location
    "user": os.getenv("user"),                          # MySQL username
    "password": os.getenv("password"),                  # MySQL Password
    "database": os.getenv("database"),                  # Database name i used
    "port": os.getenv("port")                           # obviously my port which is a general port unless you change yours btw
}


# ----------------------
# Connection helper
# ----------------------
def get_db_db():
    """Return a DB connection."""
    try:
        connection = mysql.connector.connect(**db_config)     # it creates a connection to mysql using the configuration above
        return connection                                     # it will return the connection if successful
    except Error as e:
        print(f"DB connect error: {e}")                       # it will show errors if connection fails
        raise


# ----------------------
# Password helpers 
# ----------------------
USE_HASHING = False  # Change to True to use hashed passwords

def hash_pwd(plain):
    """Return password hash or plain password depending on USE_HASHING above."""
    if USE_HASHING:
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt, 100_000)
        return f"{salt.hex()}${key.hex()}"
    else:
        return plain   # store plain text for manual testing

def check_pwd(stored, plain):
    """Check password based on hashing mode."""
    if USE_HASHING:
        try:
            salt_hex, key_hex = stored.split('$')
            new_key = hashlib.pbkdf2_hmac("sha256", plain.encode(), bytes.fromhex(salt_hex), 100_000)
            return new_key == bytes.fromhex(key_hex)
        except Exception:
            return False
    else:
        return stored == plain  # direct string match for testing


# ----------------------
# Student operations
# ----------------------
def add_student_db(matric, first, last, gender, age, phone_number, email, password_plain, photo=None):
    """Add the student data into the ddtabase"""
    connection = None
    cursor = None
    try:
        connection = get_db_db()
        cursor = connection.cursor()
        sql = """
            INSERT INTO students
            (matric, first_name, last_name, gender, age, phone_number, email, password_hash, picture_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        hashed = hash_pwd(password_plain)
        cursor.execute(sql, (matric, first, last, gender, age, phone_number, email, hashed, photo))
        connection.commit()
        return True
    except mysql.connector.IntegrityError as e:
        # duplicate primary key or unique email
        print(f"Integrity error: {e}")
        return False
    except Exception as e:
        print(f"add_student_db error: {e}")
        return False
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception:
            pass

def get_student_db(search):
    """Return first student row matching matric as dict, or None."""
    connection = None
    cursor = None
    try:
        connection = get_db_db()
        cursor = connection.cursor(dictionary=True)
        #   this query checks both columns
        cursor.execute("SELECT * FROM students WHERE matric=%s LIMIT 1", (search,))
        row = cursor.fetchone()
        return row
    except Exception as e:
        print(f"get_student_db error: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception:
            pass

def student_login_db(id, password):
    """Authenticate student by matric and return student dict (no password_hash) or None."""
    student = get_student_db(id)
    if not student:
        return None
    stored = student.get('password_hash')
    if stored and check_pwd(stored, password):
        student.pop('password_hash', None)
        return student
    return None

def update_student_db(matric, first=None, last=None, gender=None, age=None, phone=None, email=None, picture_path=None):
    """Update student fields."""
    if not matric:
        return False
    try:
        connection = get_db_db()
        cursor = connection.cursor()
        # build dynamic update
        fields = []
        params = []
        if first is not None:
            fields.append("first_name=%s"); params.append(first)
        if last is not None:
            fields.append("last_name=%s"); params.append(last)
        if gender is not None:
            fields.append("gender=%s"); params.append(gender)
        if age is not None:
            fields.append("age=%s"); params.append(age)
        if phone is not None:
            fields.append("phone_number=%s"); params.append(phone)
        if email is not None:
            fields.append("email=%s"); params.append(email)
        if picture_path is not None:
            fields.append("picture_path=%s"); params.append(picture_path)

        if not fields:
            # nothing to update
            return True

        params.append(matric)
        sql = f"UPDATE students SET {', '.join(fields)} WHERE matric=%s"
        cursor.execute(sql, tuple(params))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"update_student_db error: {e}")
        return False

def delete_student_db(matric_number):
    try:
        connection = get_db_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE matric = %s", (matric_number,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Database delete error: {e}")
        return False

def change_student_password(matric, current_password, new_password):
    """Validate current_password for matric, then set new_password (hashed if enabled)"""
    try:
        student = get_student_db(matric)
        if not student:
            return (False, "Student not found.")
        stored = student.get('password_hash')
        if not stored:
            return (False, "No password set for this user.")
        if not check_pwd(stored, current_password):
            return (False, "Current password incorrect.")
        new_hash = hash_pwd(new_password)
        connection = get_db_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET password_hash=%s WHERE matric=%s", (new_hash, student['matric']))
        connection.commit()
        cursor.close()
        connection.close()
        return (True, None)
    except Exception as e:
        print(f"change_student_password error: {e}")
        return (False, "Internal error.")


# ----------------------
# Admin operations
# ----------------------
def create_admin_db(username, password_plain):
    """Create an admin user. Return True on success, False otherwise."""
    connection = None
    cursor = None
    try:
        connection = get_db_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (%s, %s)", (username, hash_pwd(password_plain)))
        connection.commit()
        return True
    except mysql.connector.IntegrityError:
        print("create_admin_db: username exists")
        return False
    except Exception as e:
        print(f"create_admin_db error: {e}")
        return False
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception:
            pass

def admin_login_db(username, password):
    """Authenticate admin. Return admin dict (no password_hash) or None."""
    connection = None
    cursor = None
    try:
        connection = get_db_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username=%s LIMIT 1", (username,))
        admin = cursor.fetchone()
        if admin and admin.get('password_hash') and check_pwd(admin['password_hash'], password):
            admin.pop('password_hash', None)
            return admin
        return None
    except Exception as e:
        print(f"admin_login_db error: {e}")
        return None
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception:
            pass


# ----------------------
# Password Reset
# ----------------------
def create_password_reset_entry(matric_or_email, ttl_minutes=10):
    """Create a numeric 6-digit OTP reset entry for the given matric or email."""
    connection = None
    cursor = None
    try:
        connection = get_db_db()
        cursor = connection.cursor(dictionary=True)

        # find user by matric or email
        cursor.execute(
            "SELECT matric, email FROM students WHERE matric=%s OR email=%s LIMIT 1",
            (matric_or_email, matric_or_email)
        )
        user = cursor.fetchone()
        if not user:
            return (None, None)

        user_matric = user['matric']
        user_email = user.get('email')

        # Generate numeric 6-digit OTP, ensure not colliding with existing active OTPs (small loop)
        attempts = 0
        token = None
        token_hash = None
        while attempts < 10:
            attempts += 1
            # generate integer 0 to 9 and format with leading zeros
            token_plain = f"{secrets.randbelow(10**6):06d}"
            token_hash_candidate = hashlib.sha256(token_plain.encode()).hexdigest()
            # check if this exact token_hash is already an active token (very unlikely)
            cursor.execute(
                "SELECT id FROM password_resets WHERE token_hash=%s AND used=0 AND expires_at > NOW() LIMIT 1",
                (token_hash_candidate,)
            )
            if not cursor.fetchone():
                token = token_plain
                token_hash = token_hash_candidate
                break

        if not token:
            # fallback to alphanumeric long token if we couldn't find a unique OTP (extremely unlikely lol)
            token = secrets.token_urlsafe(16)
            token_hash = hashlib.sha256(token.encode()).hexdigest()

        expires = datetime.now() + timedelta(minutes=ttl_minutes)

        cursor.execute(
            "INSERT INTO password_resets (user_matric, token_hash, expires_at) VALUES (%s, %s, %s)",
            (user_matric, token_hash, expires)
        )
        connection.commit()

        return (token, user_email)
    except Exception as e:
        print(f"create_password_reset_entry error: {e}")
        return (None, None)
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception:
            pass

def verify_token_and_reset_password(token, new_password):
    """Verify token and, if valid, set new_password for the associated user."""
    try:
        connection = get_db_db()
        cursor = connection.cursor(dictionary=True)

        token_hash = hashlib.sha256(token.encode()).hexdigest()
        cursor.execute(
            "SELECT * FROM password_resets WHERE token_hash=%s AND used=0 AND expires_at > NOW() LIMIT 1",
            (token_hash,)
        )
        row = cursor.fetchone()
        if not row:
            return False

        user_matric = row['user_matric']

        # set new password (use your existing hash_pwd helper)
        new_hash = hash_pwd(new_password)
        cursor.execute("UPDATE students SET password_hash=%s WHERE matric=%s", (new_hash, user_matric))

        # mark token used
        cursor.execute("UPDATE password_resets SET used=1 WHERE id=%s", (row['id'],))

        connection.commit()
        return True
    except Exception as e:
        print(f"verify_token_and_reset_password error: {e}")
        return False
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except Exception:
            pass
