from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk

# for file upload
from tkinter.filedialog import askopenfilename, asksaveasfilename

# to convert to csv file
import csv

# for image upload
from PIL import Image, ImageTk, ImageDraw, ImageFont

import shutil, os, io
from datetime import datetime

import re
import random

# for email
import smtplib, ssl
from email.message import EmailMessage

# i used this to change my default email name
from email.utils import formataddr      

# for the html design in my mail i use escape
from html import *

# database functions
import database as db

# for my secret keys
from dotenv import load_dotenv

# Main Window
window = Tk()
window.title('Olaneye Software Institute')
window.geometry('540x480')
window.resizable(False, False)                     # this will lock down the window and prevent it from expanding and mininzing


# the color i used for the content
bg_color = "#350159"

# ------------------------------------------------------------
# Image For The Add_Pic_Btn Icon 
# -------------------------------------------------------------
# 1)
# add_pic_img = PhotoImage(file='C:/Projects/Desktop/Student Management System/user.png')

# ------------------------------------OR-------------------------------------------------

# 2) this helps in reshaping the image of choice
original_image = Image.open('C:/Projects/Desktop/Student Management System/user.png')
resized_image = original_image.resize((95, 96))
add_pic_img = ImageTk.PhotoImage(resized_image)

# this is for the image preview and pdf export
generated_idcard_pil = None        # will hold a PIL.Image for preview
generated_idcard_pdf_bytes = None  # will hold PDF bytes for download


# -----------------------------------------------------------
#  Confirmation Dialog Box 
# -------------------------------------------------------------
def confirmation_box(message):
    answer = BooleanVar()                  # used to show true or false value
    answer.set(False)

    def action(ans):
        answer.set(ans)                    # ans will be true or false
        confirmation_box.destroy()

    confirmation_box = Frame(window, highlightbackground=bg_color, highlightthickness=3)
    confirmation_box.place(x=100, y=120, width=320, height=220 )

    # label for the confirmation message
    message_lbl = Label(confirmation_box, text=message, fg=bg_color, font=('Comic Sans MS', 16))
    message_lbl.pack(pady=40)

    # button to cancel action
    cancel_btn = Button(confirmation_box, text='Cancel', font=('Comic Sans MS', 10, 'bold'), fg='white',
                        bg=bg_color, bd=0, relief='groove', command=lambda: action(False), cursor='hand2' )
    cancel_btn.place(x=50, y=140, width=70, height=30)

    # button to ok action
    ok_btn = Button(confirmation_box, text='Ok', font=('Comic Sans MS', 10, 'bold'), fg='white',
                    bg="red", bd=0, relief='groove', command=lambda: action(True), cursor='hand2' )
    ok_btn.place(x=190, y=140, width=70, height=30)

    window.wait_window(confirmation_box)           # this allows the confirmation box to hold for selection of cancel or ok
    # print(f'The user chose {answer.get()}')       
    return answer.get()                           # return the selected answer


# ------------------------------------------------------------
#  Message Dialog Box
# -------------------------------------------------------------
def message_box(message):
    # Shows a framed message, instead of default message box
    message_box = Frame(window, highlightbackground=bg_color, highlightthickness=3)
    message_box.place(x=100, y=120, width=320, height=170 )

    #  button X to cancel action
    close_btn = Button(message_box, text='X', fg='red', font=('Comic Sans MS', 15, 'bold'), 
                       bd=0, cursor='hand2', command=lambda: message_box.destroy())
    close_btn.place(x=280, y=0,)

    # label for the message_boxsage
    message_lbl = Label(message_box, text=message, fg=bg_color, font=('Comic Sans MS', 14))
    message_lbl.pack(pady=40)


# -----------------------------------------------------------
# 1) Welcome Page
# ------------------------------------------------------------
def welcome_page():
   # go to student page function
    def go_to_student_page():
        welcome_page_frame.destroy()    #   i closed the welcome page window
        window.update()                 #   this shows chnages quickly
        student_login()                 #   this opens the student login window

    # go to admin page function
    def go_to_admin_page():
        welcome_page_frame.destroy()     #   i closed the welcome page window
        window.update()                  #   this shows chnages quickly
        admin_login()                    #   this opens admin login window

        # go to create account page function
    def go_to_create_account_page():
        welcome_page_frame.destroy()     #   i closed the welcome page window
        window.update()                  #   this shows chnages quickly
        create_account()                    #   this opens create account window
        
    # the welcome page frame for my content 
    welcome_page_frame = Frame(window, 
                            #    highlightbackground=bg_color, highlightthickness=4
                               )
    welcome_page_frame.pack(pady=30)
    welcome_page_frame.pack_propagate(False)                #To resize the frame to match the size you want
    welcome_page_frame.config(width=350, height=320)

    # the heading label in my content
    heading_lbl = Label(welcome_page_frame, text='Olaneye Software Institute',
                        bg=bg_color, fg='white', font=('Comic Sans MS', 17,  ))
    heading_lbl.place(x=0, y=0, width=350)

    # student login button
    student_login_btn = Button(welcome_page_frame, text='Student', bg=bg_color, fg='white',
                               bd=0, cursor='hand2', font=('Comic Sans MS', 12), command=go_to_student_page)
    student_login_btn.place(x=70, y=80, width=200, height=30)

    # admin login button
    admin_login_btn = Button(welcome_page_frame, text='Admin', bg=bg_color, fg='white',
                             bd=0, cursor='hand2', font=('Comic Sans MS', 12), command=go_to_admin_page)
    admin_login_btn.place(x=70, y=150, width=200, height=30)

    # create account button
    create_acct_btn = Button(welcome_page_frame, text='Create Account', bg=bg_color, fg='white',
                             bd=0, cursor='hand2', font=('Comic Sans MS', 12), command=go_to_create_account_page)
    create_acct_btn.place(x=70, y=220, width=200, height=30)


# -----------------------------------------------------------
# 2) Student Login Page 
# ------------------------------------------------------------
def student_login():
    # show/hide password
    def show_hide_password():
         # it called for the show attribute value in the student password entry
        if student_pwd['show'] == '*':             # check if password is currently hidden
            student_pwd.config(show = '')          # this shows the password instead of *
            show_hide_btn.config(text='🔓')              # change the password to this icon when the password is displayed

        #if password is showing, this will hide password
        else:
            student_pwd.config(show = '*')               # hide the password
            show_hide_btn.config(text='🔒')             # show the icon when hidden

    def go_to_home_page():
        student_login_page.destroy()
        window.update()
        welcome_page()

    def go_to_forgot_password_page():
        student_login_page.destroy()
        window.update()
        forgot_pwd()

    def on_student_login():
        student_matric_number = student_id.get().strip()
        password = student_pwd.get().strip()
        if not student_matric_number or not password:
            print("All fields are required!")
            message_box("All fields are required!")
            return

        user = db.student_login_db(student_matric_number, password)  # uses databse file, student_login_db function

        if user:
            # id_number = student_matric_number
            student_login_page.destroy()
            student_dashboard(student = user) # this  authenticates each user
            window.update()
            print(f"Welcome {user.get('first_name')} {user.get('last_name')}!")
            message_box(f"Welcome {user.get('first_name')} {user.get('last_name')}!")
            
        else:
            print("Invalid login details\nPlease try again!")
            message_box("Invalid login details\nPlease try again!")


    # student login frame
    student_login_page = Frame(window,)
    student_login_page.pack(pady=30)
    student_login_page.propagate(False)
    student_login_page.config(width=350, height=320)

    # heading for student login frame
    std_heading_lbl = Label(student_login_page, text='Student Login', fg='white',
                            bg=bg_color, font=('Comic Sans MS', 18, ))
    std_heading_lbl.place(x=0, y=0, width=350)

    # go back to welocome page button
    back_btn = Button(student_login_page, text='<< Home', bd=0, fg=bg_color, font=('bold', 10), cursor='hand2' ,command=go_to_home_page)
    back_btn.place(x=10, y=50)

    # matric number label
    student_id_lbl = Label(student_login_page, text='Matriculation Number', font=('Comic Sans MS', 12, ))
    student_id_lbl.place(x=90, y=80,)

    # matric number input field
    student_id = Entry(student_login_page, bd=0, relief='groove',
                            justify='center', highlightcolor=bg_color, highlightthickness=2)
    student_id.place(x=95, y=120, width=160)

    # student password label
    student_pwd_lbl = Label(student_login_page, text='Password',
                        font=('Comic Sans MS', 12), justify='center')
    student_pwd_lbl.place(x=130, y=150)

    # student password input field
    student_pwd = Entry(student_login_page, bd=0, show='*', relief='groove',
                            justify='center', highlightcolor=bg_color, highlightthickness=2)
    student_pwd.place(x=95, y=190, width=160)

    # show or hide button
    show_hide_btn = Button(student_login_page, text='🔒', bd=0, font=(10),
                        cursor='hand2', command=show_hide_password)
    show_hide_btn.place(x=255, y=182)

    # student login button
    student_btn = Button(student_login_page, text='Login', fg='white',
                        bg=bg_color, bd=0, font=('Comic Sans MS', 12), cursor='hand2', command=on_student_login)
    student_btn.place(x=105, y=230, width=140)

    # frogot password button
    student_forget_pwd = Button(student_login_page, bd=0,fg=bg_color, text='Forgot Password?', 
                                cursor='hand2', command=go_to_forgot_password_page)
    student_forget_pwd.place(x=124, y=280)


# -----------------------------------------------------------
# 3) Student Dashboard Page
# ------------------------------------------------------------
def student_dashboard(student):
    # If user passed student login, fetch the student record
    if isinstance(student, str):
        user = db.get_student_db(student)
    else:
        user = student or {}

    print("Authenticated student:", user.get('matric'))

    # i used this to make an on click similar to js to show yellow beside the features
    # i also used a used page to switch to the pages function created
    def switch_indicator_color(hide_indicator, page ):
        profile_btn_indicator.config(bg=bg_color)
        edit_data_btn_indicator.config(bg=bg_color)
        change_password_btn_indicator.config(bg=bg_color)
        student_id_card_btn_indicator.config(bg=bg_color)
        
        hide_indicator.config(bg = 'yellow')

        # this will destroy any open dash page and switch to prefered dash page
        for child in pages_frame.winfo_children():
            child.destroy() # this will desstroy any of the dash pages opened
            window.update()
        page()
        
    def logout():
        ans = confirmation_box(message='Do you want to log out?')
        if ans:
            student_dashboard_frame.destroy()
            window.update()
            student_login()

    student_dashboard_frame = Frame(window, 
                                    highlightbackground=bg_color,
                                    highlightthickness=3
                                    )
    student_dashboard_frame.pack(pady=25)
    student_dashboard_frame.pack_propagate(False)
    student_dashboard_frame.config(width=400, height=400)
    
    # side bar to hold different functionalities
    side_bar = Frame(student_dashboard_frame, bg=bg_color,)
    side_bar.place(x=0, width=120, height=400)

    # home button in student dashboard
    profile_btn = Button(side_bar, text='👤Profile', fg='white', activeforeground='yellow', font=('Comic Sans MS', 12),
                      bd=0, activebackground=bg_color, bg=bg_color, cursor='hand2',
                      command=lambda: switch_indicator_color(hide_indicator = profile_btn_indicator,
                                                              page=dashboard_profile_page ))
    profile_btn.place(x=13, y=50)

    profile_btn_indicator = Label(side_bar, bg=bg_color)
    profile_btn_indicator.place(x=12, y=55, width=3, height=30)

    # edit_data button in student dashboard
    edit_data_btn = Button(side_bar, text='📝Edit', fg='white', activeforeground='yellow', font=('Comic Sans MS', 12),
                      bd=0, activebackground=bg_color, bg=bg_color, cursor='hand2',
                      command=lambda: switch_indicator_color(hide_indicator = edit_data_btn_indicator,
                                                              page=dashboard_edit_page ))
    edit_data_btn.place(x=13, y=100)

    edit_data_btn_indicator = Label(side_bar, bg=bg_color)
    edit_data_btn_indicator.place(x=12, y=105, width=3, height=30)

    # edit_data button in student dashboard
    student_id_card_btn = Button(side_bar, text='🪪ID Card', fg='white', activeforeground='yellow', font=('Comic Sans MS', 12),
                      bd=0, activebackground=bg_color, bg=bg_color, cursor='hand2',
                      command=lambda: switch_indicator_color(hide_indicator = student_id_card_btn_indicator,
                                                             page = dashboard_student_card_page))
    student_id_card_btn.place(x=13, y=150)

    student_id_card_btn_indicator = Label(side_bar, bg=bg_color)
    student_id_card_btn_indicator.place(x=12, y=155, width=3, height=30)

    # change_password button in student dashboard
    change_password_btn = Button(side_bar, text='🔐Password', fg='white', activeforeground='yellow', font=('Comic Sans MS', 12),
                      bd=0, activebackground=bg_color, bg=bg_color, cursor='hand2',
                      command=lambda: switch_indicator_color(hide_indicator = change_password_btn_indicator,
                                                             page=dashboard_pwd_page))
    change_password_btn.place(x=13, y=200)

    change_password_btn_indicator = Label(side_bar, bg=bg_color)
    change_password_btn_indicator.place(x=12, y=205, width=3, height=30)

     # log_out button in student dashboard
    log_out_btn = Button(side_bar, text='<<< Logout', fg='white', activeforeground='yellow', font=('Comic Sans MS', 12),
                      bd=0, activebackground=bg_color, bg=bg_color, cursor='hand2', command=logout)
    log_out_btn.place(x=13, y=240)
 
    # to switch dashboard pages i did the below, lol
    pages_frame = Frame(student_dashboard_frame, bg=None)
    pages_frame.place(x=130, y=7, width=255, height=380)

    def dashboard_profile_page():
        profile_page_frame = Frame(pages_frame,)
        profile_page_frame.pack(fill='both', expand=True)

        # this will place the image in the profile page
        photo_path = user.get('picture_path')
        if photo_path and os.path.exists(photo_path):
            try:
                # Open the image using PIL (Python Imaging Library) and resize it to 100x100 pixels
                pil = Image.open(photo_path).resize((100,100))
                # Convert the PIL image to a Tkinter-compatible photo image
                tkimg = ImageTk.PhotoImage(pil)
                # Create a label widget to display the image
                img_lbl = Label(profile_page_frame, image=tkimg)
                # Keep a reference to the image to prevent garbage collection
                img_lbl.image = tkimg
                # Position the image label at coordinates (80, 20) with size 100x100
                img_lbl.place(x=80, y=20, width=100, height=100)
            except Exception as e:
                print(f'Failed to load picture: {e}')

        # full name label
        full_name = f"{user.get('last_name','').title()} {user.get('first_name','').title()}".strip()
        profile_full_name_lbl = Label(profile_page_frame, text=full_name or 'Unknown Student', 
                              font=('Comic Sans MS', 12, 'bold'))
        profile_full_name_lbl.place(x=67, y=130)

        # geometery fields, another style i learnt
        info_x = 10
        info_y = 170
        info_gap = 26
        
        profile_matric_lbl = Label(profile_page_frame, text=f"Matric Number: {user.get('matric','')}",  font=('Comic Sans MS', 10))
        profile_matric_lbl.place(x=info_x, y=info_y)

        profile_email_lbl = Label(profile_page_frame, text=f"Email: {user.get('email','')}", font=('Comic Sans MS', 10))
        profile_email_lbl.place(x=info_x, y=info_y + info_gap)

        profile_phone_lbl = Label(profile_page_frame, text=f"Phone: {user.get('phone_number','')}", font=('Comic Sans MS', 10))
        profile_phone_lbl.place(x=info_x, y=info_y + info_gap*2)
        
        profile_age_lbl = Label(profile_page_frame, text=f"Age: {user.get('age','')}", font=('Comic Sans MS', 10))
        profile_age_lbl.place(x=info_x, y=info_y + info_gap*3)

        profile_gender_lbl = Label(profile_page_frame, text=f"Gender: {user.get('gender','').title()}", font=('Comic Sans MS', 10))
        profile_gender_lbl.place(x=info_x, y=info_y + info_gap*4)

    def dashboard_edit_page():
        edit_page_frame = Frame(pages_frame,)
        edit_page_frame.pack(fill='both', expand=True)

        # Edit profile label
        edit_profile_lbl = Label(edit_page_frame, text='Edit Profile', font=('Times New Roman', 12, 'bold'))
        edit_profile_lbl.place(x=75, y=10)

        # edit First name label
        edit_first_name_lbl = Label(edit_page_frame, text='First Name')
        edit_first_name_lbl.place(x=10, y=50)

        # edit first name entry
        edit_first_name_entry = Entry(edit_page_frame)
        edit_first_name_entry.place(x=90, y=50, width=120)
        edit_first_name_entry.insert(0, user.get('first_name',''))

        # edit last name label
        edit_last_name_lbl =Label(edit_page_frame, text='Last Name')
        edit_last_name_lbl.place(x=10, y=85)

        # edit last name entry
        edit_last_name_entry = Entry(edit_page_frame)
        edit_last_name_entry.place(x=90, y=85, width=120)
        edit_last_name_entry.insert(0, user.get('last_name',''))

        # edit Email label
        edit_email_lbl = Label(edit_page_frame, text='Email')
        edit_email_lbl.place(x=10, y=120)

        # edit email entry
        edit_email_entry = Entry(edit_page_frame)
        edit_email_entry.place(x=90, y=120, width=160)
        edit_email_entry.insert(0, user.get('email',''))

        # edit phone entry label
        edit_phone_entry = Label(edit_page_frame, text='Phone')
        edit_phone_entry.place(x=10, y=155)

        # edit phone entry entry
        edit_phone_entry = Entry(edit_page_frame)
        edit_phone_entry.place(x=90, y=155, width=120)
        edit_phone_entry.insert(0, user.get('phone_number',''))

        # edit age label
        edit_age_lbl = Label(edit_page_frame, text='Age')
        edit_age_lbl.place(x=10, y=190)

        # edit age entry
        edit_age_entry = Entry(edit_page_frame)
        edit_age_entry.place(x=90, y=190, width=60)
        edit_age_entry.insert(0, str(user.get('age','')))

        # edit gender label
        edit_gender_lbl = Label(edit_page_frame, text='Gender')
        edit_gender_lbl.place(x=10, y=225)

        # select gender field
        gender_var = StringVar(value=user.get('gender','male'))
        Radiobutton(edit_page_frame, text='Male', variable=gender_var, value='male').place(x=80, y=225)
        Radiobutton(edit_page_frame, text='Female', variable=gender_var, value='female').place(x=140, y=225)

        # Save button
        def on_save_profile():
            # collect values
            first_update = edit_first_name_entry.get().strip().title()
            last_update = edit_last_name_entry.get().strip().title()
            email_update = edit_email_entry.get().strip().lower()
            phone_update = edit_phone_entry.get().strip()
            age_v = edit_age_entry.get().strip()
            gender_v = gender_var.get()

            # minimal validation
            if not first_update or not last_update:
                message_box("First and Last name required.")
                return
            
            if not email_update:
                message_box('Email required')
                return
            
            if not phone_update:
                message_box('Phone Number required')
                return
            
            age_int = None
            if age_v.isdigit():
                age_int = int(age_v)
            elif age_v.strip() == '':
                age_int = None
            else:
                message_box("Age must be a number.")
                return

            # attempt update in DB
            success = db.update_student_db(
                matric=user.get('matric'),
                first=first_update,
                last=last_update,
                gender=gender_v,
                age=age_v,
                phone=phone_update,
                email=email_update
            )
            if success:
                # update local user dict so the profile page shows new values immediately
                user['first_name'] = first_update
                user['last_name'] = last_update
                user['gender'] = gender_v
                user['age'] = age_int
                user['phone_number'] = phone_update
                user['email'] = email_update
                message_box("Profile updated successfully.")

                switch_indicator_color(hide_indicator=profile_btn_indicator, page=dashboard_profile_page)
            else:
                message_box("Failed to update profile. Try again.")

        save_btn = Button(edit_page_frame, text='Save', bg=bg_color, fg='white', bd=0, cursor='hand2', command=on_save_profile)
        save_btn.place(x=90, y=280, width=80)


    def dashboard_student_card_page():
        student_card_page_frame = Frame(pages_frame,)
        student_card_page_frame.pack(fill='both', expand=True)

        Label(student_card_page_frame, text='Student ID Card', font=('Times New Roman', 12, 'bold')).place(x=70, y=10)

        # preview label
        preview_lbl = Label(student_card_page_frame, text='No ID generated yet.', font=('Comic Sans MS', 10))
        preview_lbl.place(x=30, y=40, width=200, height=140)

        # function to create id card bytes and a preview PIL image from current user
        def generate_idcard_for_user():
            try:
                # basic checks
                name = f"{user.get('first_name','').title()} {user.get('last_name','').title()}"
                matric = user.get('matric','').replace('OSI/25/','')  # short code for display
                gender = (user.get('gender') or '').title()
                photo = user.get('picture_path')
                phone = user.get('phone_number').strip()

                # create canvas
                card = Image.new("RGB", (450, 300), (255, 255, 255))
                draw = ImageDraw.Draw(card)

                # student photo
                if photo:
                    # resolve relative path if needed
                    photo_path = photo
                    if not os.path.isabs(photo_path):
                        candidate = os.path.join(os.getcwd(), photo_path)
                        if os.path.exists(candidate):
                            photo_path = candidate
                    if os.path.exists(photo_path):
                        p = Image.open(photo_path).resize((135, 180))
                        card.paste(p, (30, 70))
                # fonts
                try:
                    f_large = ImageFont.truetype("arial.ttf", 28)
                    f_med = ImageFont.truetype("arial.ttf", 18)
                    f_small = ImageFont.truetype("arial.ttf", 14)
                    f_tiny = ImageFont.truetype("arial.ttf", 10)
                except Exception:
                    f_large = f_med = f_small = ImageFont.load_default()

                draw.rectangle([(0, 0), (600, 48)], fill=(53, 1, 89))
                draw.text((20, 10), "STUDENT ID CARD", fill=(255, 255, 255), font=f_large)
                draw.text((170, 90), name, font=f_large, fill=(0, 0, 0))
                draw.text((170, 130), f"Matric Number: OSI/25/{matric}", font=f_med, fill=(0, 0, 0))
                draw.text((170, 160), f"Gender: {gender}", font=f_small, fill=(0, 0, 0))
                draw.text((170, 185), f"Phone: {phone}", font=f_small, fill=(0, 0, 0))
                draw.text((30, 270), f"Expiry Date: Sept 22, 2028", font=f_tiny, fill=(0, 0, 0))

                bio = io.BytesIO()
                card.convert("RGB").save(bio, "PDF")
                pdf_bytes = bio.getvalue()

                return pdf_bytes, card
            except Exception as e:
                print(f"generate_idcard_for_user error: {e}")
                return None, None

        # create preview & download
        def on_preview_generate():
            pdf_bytes, pil_img = generate_idcard_for_user()
            if not pdf_bytes:
                message_box("Failed to generate ID card.")
                return
            # show preview (resized)
            preview_img = pil_img.resize((200, 140))
            tkimg = ImageTk.PhotoImage(preview_img)
            preview_lbl.config(image=tkimg, text='')
            preview_lbl.image = tkimg  # keep reference

            # store temporarily in closure
            preview_lbl.pdf_bytes = pdf_bytes

        def on_download_idcard():
            pdf_bytes = getattr(preview_lbl, 'pdf_bytes', None)
            if not pdf_bytes:
                message_box("Please generate preview first.")
                return
            dest = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
            if not dest:
                return
            try:
                with open(dest, "wb") as f:
                    f.write(pdf_bytes)
                message_box("ID card downloaded.")
            except Exception as e:
                print(f"Failed to save ID card: {e}")
                message_box("Failed to save file.")

        gen_btn = Button(student_card_page_frame, text='Generate Preview', bg=bg_color, fg='white', bd=0, cursor='hand2', command=on_preview_generate)
        gen_btn.place(x=30, y=200, width=110)

        dl_btn = Button(student_card_page_frame, text='Download', bg=bg_color, fg='white', bd=0, cursor='hand2', command=on_download_idcard)
        dl_btn.place(x=150, y=200, width=110)


    def dashboard_pwd_page():
        pwd_page_frame = Frame(pages_frame,)
        pwd_page_frame.pack(fill='both', expand=True)

        Label(pwd_page_frame, text='Change Password', font=('Times New Roman', 12, 'bold')).place(x=60, y=10)

        Label(pwd_page_frame, text='Current Password').place(x=7, y=60)
        current_entry = Entry(pwd_page_frame, show='*', justify = 'center')
        current_entry.place(x=110, y=60, width=120)

        Label(pwd_page_frame, text='New Password').place(x=7, y=95)
        new_entry = Entry(pwd_page_frame, show='*', justify = 'center')
        new_entry.place(x=110, y=95, width=120)

        Label(pwd_page_frame, text='Confirm New').place(x=7, y=130)
        confirm_entry = Entry(pwd_page_frame, show='*', justify = 'center')
        confirm_entry.place(x=110, y=130, width=120)

        def on_change_password():
            cur = current_entry.get().strip()
            newp = new_entry.get().strip()
            conf = confirm_entry.get().strip()
            if not (cur and newp and conf):
                message_box("All fields required.")
                return
            if newp != conf:
                message_box("New passwords do not match.")
                return
            ok, msg = db.change_student_password(user.get('matric') or user.get('email'), cur, newp)
            if ok:
                switch_indicator_color(hide_indicator=profile_btn_indicator, page=dashboard_profile_page)
                message_box("Password changed successfully.")
                # clear fields
                current_entry.delete(0, END)
                new_entry.delete(0, END)
                confirm_entry.delete(0, END)
            else:
                message_box(msg or "Failed to change password.")

        change_btn = Button(pwd_page_frame, text='Change', bg=bg_color, fg='white', bd=0, cursor='hand2', command=on_change_password)
        change_btn.place(x=130, y=180, width=80)


    # when the dashboard is opened this will be displayed first
    dashboard_profile_page()


# -----------------------------------------------------------
# 4) Admin Login Page + Dashboard
# ------------------------------------------------------------
def admin_login():

    def show_hide_password():
     if admin_pwd['show'] == '*':                # check if password is currently hidden
            admin_pwd.config(show = '')          # this shows the password instead of *
            show_hide_btn.config(text='🔓')     # change the password to this icon when the password is displayed

    #if password is showing, this will hide password
     else:
        admin_pwd.config(show = '*')               # hide the password
        show_hide_btn.config(text='🔒')           # show the icon when hidden

    def go_to_home_page():
        admin_login_page.destroy()
        window.update()
        welcome_page()

    # callback for admin login button
    def on_admin_login():
        username = admin_id.get().strip()
        password = admin_pwd.get().strip()
        if not username or not password:
            print("All fields are required!")
            message_box("All fields are required!")
            return

        admin = db.admin_login_db(username, password)  # uses db.py admin_login_db
        if admin:
            # open admin dashboard
            admin_login_page.destroy()
            show_admin_dashboard(admin_username = admin)
            message_box(f"Welcome! {admin.get('username').title()}")
            # show_admin_dashboard(admin.get('username'))
        else:
            print("Invalid login details\nPlease try again!")
            message_box("Invalid login details\nPlease try again!")


    def show_admin_dashboard(admin_username):
       
        admin_dashboard = Frame(window, highlightbackground=bg_color, highlightthickness=2)
        admin_dashboard.pack(fill='both', expand=True, padx=8, pady=8)

        header = Frame(admin_dashboard)
        header.pack(fill='x', padx=6, pady=(6, 4))

        heading = Label(header, text='Admin Dashboard', bg=bg_color, fg='white',
                        font=('Comic Sans MS', 14))
        heading.pack(side='left', fill='x', expand=True, pady=4, padx=(0,10))

        def logout_and_back():
            answer = confirmation_box(message='Do you want to close your \n Dashboard?')
            if answer:
                admin_dashboard.destroy()
                window.update()
                admin_login()

        logout_btn = Button(header, text="Logout", bg='red', fg='white', bd=0, cursor='hand2', command=logout_and_back)
        logout_btn.pack(side='right', padx=(6,0))

        # Frame for treeview + scrollbars
        table_frame = Frame(admin_dashboard)
        table_frame.pack(fill='both', expand=True, padx=6, pady=(4,6))

        # Create the treeview. First column is S/N for serial numbers.
        columns = ("sn", "matric", "first_name", "last_name", "email", "phone", "age", "gender", "created_at")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        # Configure column headings & widths
        tree.heading("sn", text="S/N")
        tree.column("sn", width=40, anchor='center')

        tree.heading("matric", text="Matric")
        tree.column("matric", width=90, anchor='center')

        tree.heading("first_name", text="First Name")
        tree.column("first_name", width=110, anchor='center')

        tree.heading("last_name", text="Last Name")
        tree.column("last_name", width=110, anchor='center')

        tree.heading("email", text="Email")
        tree.column("email", width=180, anchor='w')

        tree.heading("phone", text="Phone")
        tree.column("phone", width=110, anchor='center')

        tree.heading("age", text="Age")
        tree.column("age", width=50, anchor='center')

        tree.heading("gender", text="Gender")
        tree.column("gender", width=70, anchor='center')

        tree.heading("created_at", text="Created At")
        tree.column("created_at", width=140, anchor='center')

        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Layout: treeview with scrollbars
        tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        # Make grid cells expand properly inside table_frame
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Load students from DB and insert into treeview with S/N
        try:
            connection = db.get_db_db()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT matric, first_name, last_name, email, phone_number AS phone, age, gender, created_at "
                "FROM students ORDER BY created_at DESC"
            )
            rows = cursor.fetchall()
            cursor.close()
            connection.close()

            if not rows:
                # show a friendly message in place of rows (keeps UI consistent)
                tree.insert("", "end", values=("", "No records found", "", "", "", "", "", "", ""))
            else:
                for idx, r in enumerate(rows, start=1):
                    # r is expected to be (matric, first, last, email, phone, age, gender, created_at)
                    # Insert serial number as first column
                    tree.insert("", "end", values=(idx,) + tuple(r))

        except Exception as e:
            # show an error row in the treeview and print to console for debugging
            print(f"Error loading students in dashboard: {e}")
            tree.insert("", "end", values=("", "Error loading records", "", "", "", "", "", "", ""))
            message_box(f"Error loading students: \n {e}")

        # Below the page i have refresh and export csv buttons
        actions = Frame(admin_dashboard)
        actions.pack(fill='x', padx=6, pady=(4,6))

        def refresh_table():
            # remove all items and reload
            for item in tree.get_children():
                tree.delete(item)
            try:
                conn = db.get_db_db()
                cur = conn.cursor()
                cur.execute(
                    "SELECT matric, first_name, last_name, email, phone_number AS phone, age, gender, created_at "
                    "FROM students ORDER BY created_at DESC"
                )
                new_rows = cur.fetchall()
                cur.close()
                conn.close()

                for idx, r in enumerate(new_rows, start=1):
                    tree.insert("", "end", values=(idx,) + tuple(r))
            except Exception as e:
                print(f"Refresh failed: {e}")
                message_box("Failed to refresh list.")

        refresh_btn = Button(actions, text='Refresh', bg=bg_color, fg='white', bd=0, cursor='hand2', command=refresh_table)
        refresh_btn.pack(side='left', padx=(0,8))

        def export_csv():
            # collect displayed rows from the treeview
            items = tree.get_children()
            if not items:
                print("No Data to export.")
                message_box("No Data to export.")
                return

            # prepare rows and header
            header = ["S/N", "Matric", "First Name", "Last Name", "Email", "Phone", "Age", "Gender", "Created At"]
            rows = []
            for iid in items:
                vals = tree.item(iid, "values")
                # skip empty/error placeholder rows
                if not vals or all(str(v).strip()=="" for v in vals):
                    continue
                rows.append([str(v) for v in vals])

            if not rows:
                print("No valid rows to export.")
                message_box("No valid rows to export.")
                return

            try:
                # Ask user for file location to save
                file_path = asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Save CSV File"
                )
                
                if not file_path:  # User cancelled
                    return
                    
                with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(header)
                    writer.writerows(rows)
                print(f"Export successful!\nSaved to: {file_path}")
                message_box(f"File saved successfully!")

            except Exception as e:
                print(f"CSV failed to export: {e}")
                message_box("Failed to export CSV.")
        
        export_btn = Button(actions, text='Export CSV', bg=bg_color, fg='white', bd=0, cursor='hand2', command=export_csv)
        export_btn.pack(side='left')

        # Add this to your admin dashboard after the export button
        def delete_selected():
            selected = tree.selection()
            if not selected:
                print("Please select a student to delete.")
                message_box("Please select a student to delete.")
                return
            
            # Get the matric number from the selected row (2nd column, index 1)
            matric_to_delete = tree.item(selected[0])["values"][1]
            
            if confirmation_box(f"Do you want to delete student:\n{matric_to_delete}?"):
                try:
                    success = db.delete_student_db(matric_to_delete)
                    if success:
                        tree.delete(selected[0])
                        print("Student deleted successfully.")
                        message_box("Student deleted successfully.")
                        refresh_table()  # Refresh to update serial numbers
                    else:
                        print("Failed to delete student.")
                        message_box("Failed to delete student.")
                except Exception as e:
                    print(f"Delete error: {e}")
                    message_box("Error deleting student.")

        # Add delete button to your actions frame
        delete_btn = Button(actions, text='Delete', bg='red', fg='white', 
                        bd=0, cursor='hand2', command=delete_selected)
        delete_btn.pack(side='left', padx=(8,0))

        # make sure the UI updates
        window.update()


    # admin login frame
    admin_login_page = Frame(window,)
    admin_login_page.pack(pady=30)
    admin_login_page.propagate(False)
    admin_login_page.config(width=350, height=320)

    # heading for admin login frame
    admin_heading_lbl = Label(admin_login_page, text='Admin Login', fg='white',
                            bg=bg_color, font=('Comic Sans MS', 18, ))
    admin_heading_lbl.place(x=0, y=0, width=350)

  # go back to welocome page button
    back_btn = Button(admin_login_page, text='<< Home', bd=0, fg=bg_color, font=('bold', 10), cursor='hand2' ,command=go_to_home_page)
    back_btn.place(x=10, y=50)

    # admin login label
    admin_id_lbl = Label(admin_login_page, text='Username', font=('Comic Sans MS', 12, ))
    admin_id_lbl.place(x=140, y=80,)

    # admin login input field
    admin_id = Entry(admin_login_page, bd=0, relief='groove',
                            justify='center', highlightcolor=bg_color, highlightthickness=2)
    admin_id.place(x=95, y=120, width=160)

    # admin password label
    admin_pwd_lbl = Label(admin_login_page, text='Password',
                        font=('Comic Sans MS', 12), justify='center')
    admin_pwd_lbl.place(x=130, y=150)

    # admin password input field
    admin_pwd = Entry(admin_login_page, bd=0, show='*', relief='groove',
                            justify='center', highlightcolor=bg_color, highlightthickness=2)
    admin_pwd.place(x=95, y=190, width=160)

    # show or hide button
    show_hide_btn = Button(admin_login_page, text='🔒', bd=0, font=(10),
                        cursor='hand2', command=show_hide_password )
    show_hide_btn.place(x=255, y=182)

    # admin login button (now wired to on_admin_login)
    admin_btn = Button(admin_login_page, text='Login', fg='white',
                        bg=bg_color, bd=0, font=('Comic Sans MS', 12), cursor='hand2', command=on_admin_login)
    admin_btn.place(x=105, y=230, width=140)


# -----------------------------------------------------------
# 5) Create Account Page + Student ID Card Generator
# ------------------------------------------------------------
def create_account():
    
    # this is for image upload  
    picture_path = StringVar()  # Creates a special Tkinter string variable
    picture_path.set('')        # Initializes it as empty

    # function to open picture from folder
    def open_picture():
        # Open file dialog with image type filters
        path = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All files", "*.*")])
        if not path:  # If user cancels the dialog
            return

        try:
            # Open and resize the image
            img = Image.open(path).resize((100, 100))
            # Convert to Tkinter-compatible format
            converted_image = ImageTk.PhotoImage(img)
            # Store the file path
            picture_path.set(path)
            # Update the button to show the image
            add_pic_btn.config(image=converted_image)
            # Keep reference to avoid garbage collection
            add_pic_btn.image = converted_image  
        except Exception as e:
            print(f"Failed to open image: \n{e}")
            message_box(f"Failed to open image")
            return

    # function for a go to home button
    def go_to_home_page():

        # this is from the confirmation dialog box function created above which can be used anywhere
        ans = confirmation_box(message = f'Do you want to close the \n registration page?')
        
        if ans : 
            create_account_page.destroy()
            window.update()
            welcome_page()

    # this function helps me generate a unique matric number and ensure it is not already in DB
    def generate_matric_number():
        # keep trying until unique found (max attempts to avoid infinite loop)
        attempts = 0
        while attempts < 30:
            attempts += 1
            
            matric_number = ''.join(str(random.randint(0,9)) for r in range(6))  # runs  times to generate 8 numbers
                    
            # check DB if this matric exists using your get_student helper in db file
            existing = db.get_student_db(matric_number)
            if not existing:
                # found unique matric
                student_matric_number.config(state='normal')
                # clear any existing text in the front end, then insert
                student_matric_number.delete(0, END)
                student_matric_number.insert(END, matric_number)
                student_matric_number.config(state='readonly')
                return matric_number
                
        # if we reach here, something is wrong (very unlikely)
        print("Failed to generate unique matric. Try again.")
        message_box("Failed to generate unique matric. Try again.")
        return None

    # to check valid email
    def check_valid_email(email):
        pattern = '^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]+(\\.[a-z0-9]+)*(\\.[a-z]{2,4})$'
        match = re.match(pattern=pattern, string=email)
        return match

    # function to start student card
    def student_id_card():

        # student id card frame
        student_id_card = Frame(window, 
                                # highlightbackground=bg_color, highlightthickness=3
                                )
        student_id_card.place(x=100, y=50, width=320, height=380)

        # student heading label
        heading_lbl = Label(student_id_card, 
                            # text = 'Student ID Card', 
                            fg='white', bg=bg_color,
                            font=('Comic Sans MS', 13,))
        heading_lbl.pack(fill='both')

        # close the student id card frame
        close_btn = Button(student_id_card, text='X', fg='white', bg=bg_color,
                            font=('Comic Sans MS', 10, 'bold'), bd=0, 
                            cursor='hand2', command=lambda: student_id_card.destroy()
                            )
        close_btn.place(x=290, y=0)
        
        # preview id card before download
        preview = Label(student_id_card)
        preview.place(x=30, y=50, width=260, height=210)

        # load PIL image from memory for preview (if available)
        pil_img = globals().get('generated_idcard_pil', None)
        if pil_img:
            # create a resized copy for preview and convert to ImageTk
            preview_img = pil_img.resize((260, 210))
            tkimg = ImageTk.PhotoImage(preview_img)
            preview.config(image=tkimg)
            preview.image = tkimg   # keep reference
        else:
            preview.config(text="No ID card generated yet.", justify='center')

        # function to download id card to pdf 
        def download_id_card():
            pdf_bytes = globals().get('generated_idcard_pdf_bytes', None)
            if not pdf_bytes:
                print("No generated PDF found.\nPlease generate an ID card first.")
                message_box("No generated PDF found.\nPlease generate an ID card first.")
                return
            dest = tk.filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf")],
                                                title="Save ID card as PDF")
            if not dest:
                return
            try:
                with open(dest, "wb") as f:
                    f.write(pdf_bytes)   # write the in-memory PDF bytes to chosen path
                print("ID card saved successfully.")
                message_box("ID card saved successfully.")
            except Exception as e:
                print(f"Failed to save ID card: \n{e}")                                         


        # save student card
        save_student_id_card_btn = Button(student_id_card, text='⬇ Download', fg='white', bg=bg_color, bd=1,
                                        relief='groove', font=('Comic Sans MS',10,), cursor='hand2',
                                        command=download_id_card)
        save_student_id_card_btn.place(x=110, y=290, width=100)

    # function to generate id card
    def generate_id_card():

        # --- collect form values ---
        name = f"{student_first_name.get().strip().title()} {student_last_name.get().strip().title()}"
        matric = student_matric_number.get().strip()
        photo = picture_path.get().strip()
        gender = student_gender.get().strip().title()
        age = student_age.get().strip()
        phone = student_number.get().strip()
        email = student_email.get().strip().lower()

        
        if not matric:
            message_box("Cannot generate ID: \n Missing matric number.")
            return
        if not name.strip():
            message_box("Cannot generate ID: \n Missing student name.")
            return
        if not photo or not os.path.exists(photo):
            message_box("Please upload a valid photo \n before generating the ID card.")
            return

        try:
            # canvas 
            card = Image.new("RGB", (450, 300), (255, 255, 255))
            draw = ImageDraw.Draw(card)

            # student photo (may raise if file invalid)
            p = Image.open(photo).resize((135, 180))  
            card.paste(p, (30, 70)) 

            # fonts (try truetype, fallback to default)
            try:
                f_large = ImageFont.truetype("arial.ttf", 28)
                f_med = ImageFont.truetype("arial.ttf", 18)
                f_small = ImageFont.truetype("arial.ttf", 14)
                f_tiny = ImageFont.truetype("arial.ttf", 10)
            except Exception:
                f_large = f_med = f_small = ImageFont.load_default()

            # header + info
            draw.rectangle([(0, 0), (600, 48)], fill=(53, 1, 89))
            draw.text((20, 10), "STUDENT ID CARD", fill=(255, 255, 255), font=f_large)
            draw.text((170, 90), name, font=f_large, fill=(0, 0, 0))
            draw.text((170, 130), f"Matric Number: OSI/25/{matric}", font=f_med, fill=(0, 0, 0))
            draw.text((170, 160), f"Gender: {gender}", font=f_small, fill=(0, 0, 0))
            draw.text((170, 185), f"Phone: {phone}", font=f_small, fill=(0, 0, 0))
            # draw.text((170, 185), f"Email: {email}", font=f_small, fill=(0, 0, 0))
            # draw.text((30, 270), f"Issue Date: {datetime.now().strftime('%b %d, %Y')}", font=f_tiny, fill=(0, 0, 0))
            draw.text((32, 270), f"Expiry Date: Sept 22, 2028", font=f_tiny, fill=(0, 0, 0))
        

            # store image and PDF bytes 
            bio = io.BytesIO()
            card.convert("RGB").save(bio, "PDF")         # write PDF to bytes buffer
            pdf_bytes = bio.getvalue()                   # extract bytes

            globals()['generated_idcard_pil'] = card     # PIL image for preview
            globals()['generated_idcard_pdf_bytes'] = pdf_bytes  # PDF bytes for download

        except Exception as e:
            # minimal friendly error reporting
            print(f"Failed to create ID card: \n{e}")
            # message_box(f"Failed to create ID card: \n{e}")
            return

    # function to check validation
    def check_input_validation():
        # basic password match check
        if student_pwd.get().strip() != student_confirm_pwd.get().strip():
            student_pwd.config(highlightcolor='red', highlightbackground='red')
            student_confirm_pwd.config(highlightcolor='red', highlightbackground='red')
            message_box(message=f"Passwords do not match!")
            return

        # field validations 
        if student_first_name.get().strip() == '':
            student_first_name.config(highlightcolor='red', highlightbackground='red')
            student_first_name.focus()
            message_box(message='First Name required!')
            return
        else:
            student_first_name.config(highlightcolor=bg_color, highlightbackground=bg_color)

        if student_last_name.get().strip() == '':
            student_last_name.config(highlightcolor='red', highlightbackground='red')
            student_last_name.focus()
            message_box(message='Last Name Required!')
            return
        else:
            student_last_name.config(highlightcolor=bg_color, highlightbackground=bg_color)

        if student_age.get().strip() == '':
            student_age.config(highlightcolor='red', highlightbackground='red')
            student_age.focus()
            message_box(message='Age Required!')
            return
        else:
            student_age.config(highlightcolor=bg_color, highlightbackground=bg_color)

        if student_number.get().strip() == '':
            student_number.config(highlightcolor='red', highlightbackground='red')
            student_number.focus()
            message_box(message='Phone Number Required!')
            return
        else:
            student_number.config(highlightcolor=bg_color, highlightbackground=bg_color)

        if student_email.get().strip() == '':
            student_email.config(highlightcolor='red', highlightbackground='red')
            student_email.focus()
            message_box(message='Email Address Required!')
            return
        elif not check_valid_email(email= student_email.get().strip().lower()):
            student_email.config(highlightcolor='red', highlightbackground='red')
            student_email.focus()
            message_box(message='Invalid! \n Please enter a valid email')
            return
        else:
            student_email.config(highlightcolor=bg_color, highlightbackground=bg_color)

        if not picture_path.get().strip():
            message_box("Image required!")
            return

        if student_pwd.get().strip() == '':
            message_box(message='Password Required!')
            return

        # all validations passed: prepare values and call add_student()
        matric_val = student_matric_number.get().strip()
        if not matric_val:
            # attempt to generate if for some reason it's empty
            matric_val = generate_matric_number()
            if not matric_val:
                return

        
        # convert age safely to digit
        age_val = None
        if student_age.get().strip().isdigit():
            age_val = int(student_age.get().strip())

        try:
            # Create uploads directory if it doesn't exist
            uploads_dir = os.path.join(os.getcwd(), "uploads")          # this creates the folder directory
            os.makedirs(uploads_dir, exist_ok=True)

            # Prepare destination filename/path
            orig_path = picture_path.get().strip()
            ext = os.path.splitext(orig_path)[1] or ".jpg"             # Get extension or default to .jpg
            dest_filename = f"{matric_val}{ext}"                       # Use matric number as filename
            dest_path = os.path.join(uploads_dir, dest_filename)

            # Copy image to uploads directory
            shutil.copy2(orig_path, dest_path)
            photo_to_store = dest_path  # Will store this path in database


            student_data = db.add_student_db(
                matric=f"OSI/25/{matric_val}",
                first=student_first_name.get().strip().title(),
                last=student_last_name.get().strip().title(),
                gender=student_gender.get(),
                age=age_val,
                phone_number=student_number.get().strip(),
                email=student_email.get().strip().lower(),
                password_plain=student_pwd.get().strip(),
                photo=photo_to_store
            )
            if student_data:
                def send_via_gmail(to_addr, timeout=40, debug=False):
                    SMTP_HOST = "smtp.gmail.com"
                    SMTP_PORT_1 = 465         # use 465 or 587, check the test file to see which port works 
                    SMTP_PORT_2 = 587        # use 465 or 587, check the test file to see which port works 

                    load_dotenv()
                    gmail_user = os.getenv('gmail_user')
                    gmail_pass = os.getenv('gmail_password')  

                    if not gmail_user or not gmail_pass:
                        print("Email credentials not configured")
                        message_box("Email credentials not configured.")
                        return False

                
                    display_name = 'Olaneye Software Institute'
                    matric = f"OSI/25/{matric_val}"
                    msg = EmailMessage()
                    msg["Subject"] = "Account Created Successfully 🎉"
                    msg["From"] = formataddr((display_name, gmail_user))
                    msg["To"] = to_addr
                    msg.set_content(
                        f"Dear {student_last_name.get().strip().title()} {student_first_name.get().strip().title()},\n\n"
                        f"Welcome to Olaneye Software Institute! Your student registration account has been successfully created.\n\n"

                        f"You can now access your academic dashboard and resources using the credentials provided below:\n"
                        f"Matriculation Number: {matric}.\n"
                        f"Password: {student_pwd.get().strip()}.\n\n"

                        f"⚠ Important Security Requirement:\n"
                        f"We recommend changing your password after your first login for enhanced security.\n\n"
                        f"If you did not create this account, please contact our IT Support Desk immediately at olaneye.ahmed@institute.edu or +234 903 896 7463.\n\n"
                        
                        "Getting Started:\n"
                        "1. Go to our website www.olaneyesoftwareinstitute.edu\n\n"
                        "2. Enter your Matriculation Number and the Password provided above.\n"
                        "3. Once logged in, navigate to `password` to create a new, strong password.\n\n"
                        "Welcome to our academic community. We wish you success in your studies!\n\n"
                        "Sincerely,"
                        "©️ Olaneye Ahmed Oladapo"
                        "Founder and Developer"
                        "https://www.linkedin.com/in/olaneye/"


                        "This is an automated message. Please do not reply to this email."
                        "©️2025 Olaneye Software Institute. | All rights reserved"
                        )
                    
                    msg.add_alternative(
                        f"""\
                        <html>
                        <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f9f9f9; color:#222;">
                            <div style="max-width:600px; margin:20px auto; background:#ffffff; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); padding:20px;">
                                
                                <!-- Header -->
                                <div style="text-align:center; padding-bottom:10px; border-bottom:2px solid #4CAF50;">
                                    <h1 style="color:#4CAF50; margin:0;">🎓 Olaneye Software Institute</h1>
                                    <p style="font-size:14px; color:#666;">Empowering Students Through Technology</p>
                                </div>

                                <!-- Body -->
                                <div style="padding:20px;">
                                    <p>Dear <strong>{student_last_name.get().strip().title()} {student_first_name.get().strip().title()}</strong>,</p>
                                    
                                    <p>Welcome to <b>Olaneye Software Institute</b>! Your student registration account has been successfully created.</p>
                                    <div style="background:#f4fdf6; padding:15px; border-left:4px solid #4CAF50; margin:15px 0; border-radius:4px;">
                                        <p>You can now access your academic dashboard and resources using the credentials provided below:</p>
                                        <p style="margin:0;"><b>Matriculation Number:</b> 
                                            <code style="font-size:1rem; padding:2px 6px; background:#eee; border-radius:4px;">{matric}</code>
                                        </p>
                                        <br>
                                        <p style="margin:0;"><b>Password:</b> 
                                            <code style="font-size:1rem; padding:2px 6px; background:#eee; border-radius:4px;">{student_pwd.get().strip()}</code>
                                        </p>
                                    </div>

                                    <center><p>⚠️ <b>Important Security Requirement:</b><br>We recommend changing your password after your first login for enhanced security.</p></center>
                                    
                                    <h3 style="margin-top:20px; color:#4CAF50;">Getting Started</h3>
                                    <ol style="padding-left:18px; line-height:1.6;">
                                        <li>Go to our website: <a href="http://www.olaneyesoftwareinstitute.edu" style="color:#4CAF50;">www.olaneyesoftwareinstitute.edu</a></li>
                                        <li>Enter your Matriculation Number and the password provided above.</li>
                                        <li>Navigate to <b>Password</b> to set a new, strong password.</li>
                                    </ol>

                                    <p>If you did not create this account, please contact our IT Support Desk immediately at 
                                    <a href="mailto:olaneye.ahmed@institute.edu" style="color:#4CAF50;">olaneye.ahmed@institute.edu</a> 
                                    or call <b>+234 903 896 7463</b>.</p>

                                    <p style="margin-top:20px;">We’re excited to have you join our academic community. Wishing you success in your studies!</p>
                                    
                                    <p style="margin-top:30px; font-size:14px; color:#555;">
                                        Sincerely,<br>
                                        <b>Olaneye Ahmed Oladapo</b><br>
                                        Founder & Developer<br>
                                        <a href="https://www.linkedin.com/in/olaneye/" style="color:#4CAF50;">LinkedIn Profile</a>
                                    </p>
                                </div>

                                <!-- Footer -->
                                <div style="text-align:center; padding:15px; border-top:1px solid #eee; font-size:12px; color:#888;">
                                    <p style="margin:5px 0;">©️2025 Olaneye Software Institute | All rights reserved.</p>
                                </div>

                            </div>
                        </body>
                        </html>
                        """, 
                        subtype="html"
                    )

                    ctx = ssl.create_default_context()

                    # i encountered some errors using my gmail, due to the ports
                    print('Mail Port 465 being tested!!')
                    try:
                        if debug: 
                            print('try smtp.gmail.com:465 first......')
                        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT_1, timeout=timeout, context=ctx) as smtp:
                        
                            if debug:
                                smtp.set_debuglevel(1)
                            smtp.login(gmail_user, gmail_pass)
                            smtp.send_message(msg)
                        if debug:
                            print('The mail has been sent, smtp_ssl:465 worked lol')
                        return True
                    except Exception as e1:
                        print(f"-------First Failed Attempt-----")
                        print(f'Mail Port 465 failed!!')
                        print(f"smtp_ssl:465 failed: {e1}")
                        print(f"--------------------------------")

                    print('Mail Port 587 being tested!!')
                    try:
                        if debug:
                            print('try smtp.gmail.com:587') 
                        with smtplib.SMTP(SMTP_HOST, SMTP_PORT_2, timeout=timeout) as smtp:
                            if debug:
                                smtp.set_debuglevel(1)
                            smtp.ehlo()
                            smtp.starttls(context=ctx)
                            smtp.ehlo()
                            smtp.login(gmail_user, gmail_pass)
                            smtp.send_message(msg)
                        if debug:
                            print('The mail has been sent, smtp_stattls:587 worked finally')
                        return True
                    except Exception as e2:
                        print(f"-------Second Failed Attempt-----")
                        print(f'Mail Port 587 failed!!')
                        print(f"smtp_starttls:587 failed {e2}")
                        print(f"--------------------------------")

                    print('The two smtp attempts failed.')
                    return False

                recipient = student_email.get().strip().lower()
                email_sent = send_via_gmail(to_addr=recipient, timeout=50, debug=False)        # this sends the mail first
                
                if not email_sent: 
                    generate_id_card()      # this generates the id card
                    student_id_card()       #this dsiplays the id card on the screen
                    print(f"-----------------------------------")
                    print(f"Registration successful! \nEmail delivery failed.\nPlease download your ID Card")
                    message_box(f"Registration successful! \nEmail delivery failed.\nPlease download your ID Card")
                    print(f"-----------------------------------")
                    
                else:
                    generate_id_card()      # this generates the id card
                    student_id_card()       #this dsiplays the id card on the screen
                    print(f"-----------------------------------")
                    print(f"Registration successful! \nCheck Email for further details.\nPlease download your ID Card")
                    message_box(f"Registration successful! \nCheck Email for further details.\nPlease download your ID Card")
                    print(f"-----------------------------------")


                # clear minimal fields:
                student_first_name.delete(0, END)
                student_last_name.delete(0, END)
                student_age.delete(0, END)
                student_number.delete(0, END)
                student_email.delete(0, END)
                student_pwd.delete(0, END)
                student_confirm_pwd.delete(0, END)
               
                 # Reset picture upload
                picture_path.set('')
                add_pic_btn.config(image=add_pic_img)  # Reset to default icon
                add_pic_btn.image = add_pic_img  # Maintain reference
                
                # Generate new matric for next registration
                generate_matric_number()
            else:
                # add_student returned False
                message_box("Registration failed: \n Email already exist.")
        except Exception as e:
            print(f"Registration error: \n{e}")
            # message_box(f"Registration error: \n{e}")


    # Build the create account page UI (kept same as your layout)
    create_account_page = Frame(window)
    create_account_page.pack(pady=20)
    create_account_page.propagate(False)
    create_account_page.config(width=400, height=400)

    # create account label
    create_account_lbl = Label(create_account_page, text='Student Registration Form', fg='white',
                            bg=bg_color, font=('Comic Sans MS', 10, ))
    create_account_lbl.place(x=0, y=0, width=400)

    # add picture frame to the form
    add_pic = Frame(create_account_page, highlightbackground=bg_color, highlightthickness=3, )
    add_pic.place(x=286, y=26, width=105, height=105)

    # add a button to the picture frame (add_pic) to upload picture
    add_pic_btn = Button(add_pic, image=add_pic_img, bd=0, command=open_picture, cursor = 'hand2')
    add_pic_btn.pack(fill='both')

    # student matric number label
    student_matric_number_lbl = Label(create_account_page, text='Matric Number:',
                                 fg='black', font=('Comic Sans MS', 12), )
    student_matric_number_lbl.place(x=4, y=70)

    # student matric number display field
    student_matric_number = Entry(create_account_page, fg='black', font=('Comic Sans MS', 15), cursor='hand2')
    student_matric_number.place(x=130, y=73, width=120, height=25)
    student_matric_number.config(state='readonly')

    # generate initial matric (unique)
    generate_matric_number()

    # student first name label
    student_first_name_lbl = Label(create_account_page, text='First Name', fg='black', font=('Comic Sans MS', 12))
    student_first_name_lbl.place(x=19, y=135)

    # student first name entry
    student_first_name = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
    student_first_name.place(x=2, y=165, width=120)

    # student last name label
    student_last_name_lbl = Label(create_account_page, text='Last Name', fg='black', font=('Comic Sans MS', 12))
    student_last_name_lbl.place(x=147, y=135)
    
    # student last name entry
    student_last_name = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey',  highlightthickness=2)
    student_last_name.place(x=130, y=165, width=120)

    # student gender label
    student_gender_lbl = Label(create_account_page, text='Gender', fg='black', font=('Comic Sans MS', 12))
    student_gender_lbl.place(x=290, y=135)

    # for the selction of the gender
    student_gender = StringVar()
    student_gender.set('male')

    # male gender radio
    male_gender_btn= Radiobutton(create_account_page, text='Male', fg='black', font=('bold', 10), 
                                 activebackground='white', variable=student_gender, value='male', cursor='hand2')
    male_gender_btn.place(x=255, y=165)

    # female gender radio
    female_gender_btn= Radiobutton(create_account_page, text='Female', fg='black', font=('bold', 10), 
                                 activebackground='white', variable=student_gender, value='female', cursor='hand2')
    female_gender_btn.place(x=310, y=165)

    # student age label
    student_age_lbl = Label(create_account_page, text='Age', fg='black', font=('Comic Sans MS', 12))
    student_age_lbl.place(x=40, y=195)

    # student age input field
    student_age = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
    student_age.place(x=2, y=230, width=120)

    # student phone number label
    student_number_lbl = Label(create_account_page, text='Phone Number', fg='black', font=('Comic Sans MS', 12))
    student_number_lbl.place(x=135, y=195)

    # student phone number input field
    student_number = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
    student_number.place(x=130, y=230, width=120)

    # student email address
    student_email_lbl = Label(create_account_page, text='Email Address', fg='black', font=('Comic Sans MS', 12))
    student_email_lbl.place(x=265, y=195)

    # student email address entry
    student_email = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
    student_email.place(x=260, y=230, width=120)

    # student password
    student_pwd_lbl = Label(create_account_page, text='Password', fg='black', font=('Comic Sans MS', 12))
    student_pwd_lbl.place(x=25, y=260)

    # student password entry
    student_pwd = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
    student_pwd.place(x=2, y=295, width=120)

    # student confirm password
    student_confirm_pwd_lbl = Label(create_account_page, text='Confirm Password', fg='black', font=('Comic Sans MS', 12))
    student_confirm_pwd_lbl.place(x=129, y=260)

    # student confirm password entry
    student_confirm_pwd = Entry(create_account_page, bd=0, relief='groove', 
                            justify='center', highlightcolor=bg_color, highlightbackground='grey', highlightthickness=2)
    student_confirm_pwd.place(x=135, y=295, width=120)

    # go to home button
    home_btn = Button(create_account_page, text='Home', fg='white', bg='red', font=('bold', 10),
                    bd=0, relief='groove', cursor='hand2', command = go_to_home_page)
    home_btn.place(x=190, y=340, width=90, height=25)
    
    # submit home button
    submit_btn = Button(create_account_page, text='Submit', fg='white', bg=bg_color, font=('bold', 10),
                        bd=0, relief='groove', cursor='hand2', command=check_input_validation)
    submit_btn.place(x=290, y=340, width=90, height=25)


# -----------------------------------------------------------
# 6) Forgot Password Page
# ------------------------------------------------------------
def forgot_pwd():


    def go_back_to_student_login_page():
        ans = confirmation_box("Do you want to close this page")
        if ans:
            forgot_pwd_frame.destroy()
            window.update()
            student_login()


    # Fogot password frame (keeps your original look & placement)
    forgot_pwd_frame = Frame(window)
    forgot_pwd_frame.place(x=100, y=120, width=320, height=220)

    # Fogot password heading
    forgot_pwd_heading = Label(forgot_pwd_frame, text='Forgot Password?', fg='white',
                               font=('Comic Sans MS', 15), bg=bg_color
                            )
    forgot_pwd_heading.pack(fill='both')

    close_forgot_pwd_frame = Button(forgot_pwd_frame, text='X', font=('Comic Sans MS', 11, 'bold'), fg='white',
                                    activeforeground='red', bd=0, bg=bg_color, activebackground=bg_color,
                                    cursor='hand2', command= go_back_to_student_login_page
                                )
    close_forgot_pwd_frame.place(x=290, y=-4)

    # forgot password label
    forgot_pwd_lbl = Label(forgot_pwd_frame, text='Please enter Matric Number', font=('Comic Sans MS', 11))
    forgot_pwd_lbl.place(x=65, y=50)

    # Fogot password entry
    matric_number_entry = Entry(forgot_pwd_frame, bd=1, relief='groove', justify='center', highlightcolor=bg_color,
                                highlightthickness=2, width=30
                            )
    matric_number_entry.place(x=40, y=80, width=240)

    submit_forgot_pwd = Button(forgot_pwd_frame, text='Submit', fg='white', bg=bg_color,
                                bd=0, relief='groove', cursor='hand2'
                            )
    submit_forgot_pwd.place(x=130, y=115, width=63)

    
    def send_via_gmail(to_addr, token, timeout=40, debug=False):
        SMTP_HOST = "smtp.gmail.com"
        SMTP_PORT_1 = 465         # use 465 or 587, check the test file to see which port works 
        SMTP_PORT_2 = 587        # use 465 or 587, check the test file to see which port works 

        load_dotenv()
        gmail_user = os.getenv('gmail_user')
        gmail_pass = os.getenv('gmail_password')  

        if not gmail_user or not gmail_pass:
            message_box("Email credentials not configured.")
            print("Email credentials not configured")
            return False

        display_name = 'Olaneye Software Institute'
        msg = EmailMessage()
        msg["Subject"] = "Password Reset Token"
        msg["From"] = formataddr((display_name, gmail_user))
        msg["To"] = to_addr
        msg.set_content(
                f"You requested a password reset.\n\n"
                f"Token: {token}\n\n"
                "This token expires in 10 minutes. If you didn't request this, please ignore this message.\n\n"
                "©️ Olaneye Ahmed Oladapo"
            )
        
        token_html = escape(token)          # it prevents accidental HTML injection
        msg.add_alternative(
            
        f"""\
            <html>
            <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f9f9f9; color:#222;">
                <div style="max-width:600px; margin:20px auto; background:#ffffff; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); padding:20px;">
                    
                    <!-- Header -->
                    <div style="text-align:center; padding-bottom:10px; border-bottom:2px solid #4CAF50;">
                        <h1 style="color:#4CAF50; margin:0;">🎓 Olaneye Software Institute</h1>
                        <p style="font-size:14px; color:#666;">Empowering Students Through Technology</p>
                    </div>

                    <!-- Body -->
                    <div style="padding:20px;">
                        <p>You requested a password reset.</p>
                        <div style="background:#f4fdf6; padding:15px; border-left:4px solid #4CAF50; margin:15px 0; border-radius:4px;">
                            <p style="margin:0;"><b>Token:</b> 
                                <code style="font-size:1rem; padding:2px 6px; background:#eee; border-radius:4px;">{token_html}</code>
                            </p>
                        </div>

                        <p>⚠️This token expires in <strong>10 minutes</strong>. If you didn't request this, please ignore this message.</p>
                       
                        <p style="margin-top:30px; font-size:14px; color:#555;">
                            Sincerely,<br>
                            <b>Olaneye Ahmed Oladapo</b><br>
                            Founder & Developer<br>
                            <a href="https://www.linkedin.com/in/olaneye/" style="color:#4CAF50;">LinkedIn Profile</a>
                        </p>
                    </div>

                    <!-- Footer -->
                    <div style="text-align:center; padding:15px; border-top:1px solid #eee; font-size:12px; color:#888;">
                        <p style="margin:5px 0;">©️2025 Olaneye Software Institute | All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
        """, 
        subtype="html")

        ctx = ssl.create_default_context()

        # i encountered some errors using my mail, due to the ports
        print('Mail Port 465 being tested!!')
        try:
            if debug: 
                print('I want to try smtp_ssl on smtp.gmail.com with port 465 first......')
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT_1, timeout=timeout, context=ctx) as smtp:
            
                if debug:
                    smtp.set_debuglevel(1)
                smtp.login(gmail_user, gmail_pass)
                smtp.send_message(msg)
                print('Mail Port 465 worked')

            if debug:
                print('The mail has been sent, smtp_ssl:465 worked lol')
            return True
        except Exception as e1:
            print(f'The mail was not sent, let`s try smtp_starttls:587')
            print(f"smtp_ssl:465 failed: {e1}")
        
        print('Mail Port 587 being tested!!')
        try:
            if debug:
                print('let`s try starttls on smtp.gmail.com:587 secondly') 
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT_2, timeout=timeout) as smtp:
                if debug:
                    smtp.set_debuglevel(1)
                smtp.ehlo()
                smtp.starttls(context=ctx)
                smtp.ehlo()
                smtp.login(gmail_user, gmail_pass)
                smtp.send_message(msg)
                print('Mail Port 587 worked')

            if debug:
                print('The mail has been sent, smtp_stattls:587 worked finally')
            return True
            
        except Exception as e2:
            print(f'The mail was not sent............')
            print(f"Smtp_starttls:587 failed {e2}")

        print('All smtp attempts failed.')
        return False
        

    # placehoders for reset widgets
    token_label = None
    token_entry = None
    new_pwd_label = None
    new_pwd_entry = None
    confirm_pwd_label = None
    confirm_pwd_entry = None
    submit_reset_btn = None

    def reveal_reset_widgets(prefill_token=None):

        # increase frame height to fit new widgets
        forgot_pwd_frame.place_configure(height=370)

        nonlocal token_label, token_entry, new_pwd_label, new_pwd_entry, confirm_pwd_label, confirm_pwd_entry, submit_reset_btn

        # avoid creating duplicates if already revealed
        if token_entry:
            return

        token_label = Label(forgot_pwd_frame, text='Enter Token', font=('Comic Sans MS', 10))
        token_label.place(x=15, y=140)

        token_entry = Entry(forgot_pwd_frame, bd=1, relief='groove', justify='center', 
                            highlightcolor=bg_color,
                            highlightthickness=2, width=25
                            )
        token_entry.place(x=140, y=140)
        if prefill_token:
            token_entry.insert(0, prefill_token)

        new_pwd_label = Label(forgot_pwd_frame, text='New Password', font=('Comic Sans MS', 10))
        new_pwd_label.place(x=15, y=170)
        
        new_pwd_entry = Entry(forgot_pwd_frame, bd=1, relief='groove',  justify='center',
                               highlightcolor=bg_color,
                               highlightthickness=2, width=25
                             )
        new_pwd_entry.place(x=140, y=170)

        confirm_pwd_label = Label(forgot_pwd_frame, text='Confirm Password', font=('Comic Sans MS', 10))
        confirm_pwd_label.place(x=15, y=200)

        confirm_pwd_entry = Entry(forgot_pwd_frame, bd=1, relief='groove', justify='center',
                               highlightcolor=bg_color,
                               highlightthickness=2, width=25
                             )
        confirm_pwd_entry.place(x=140, y=200)

        submit_reset_btn = Button(
            forgot_pwd_frame, text='Reset Password', fg='white', bg=bg_color, bd=0, relief='groove',
            cursor='hand2'
        )
        submit_reset_btn.place(x=130, y=230, width=90)

        def on_submit_reset():
            t = token_entry.get().strip()
            p1 = new_pwd_entry.get().strip()
            p2 = confirm_pwd_entry.get().strip()
            if not (t and p1 and p2):
                message_box("All fields required")
                return
            if p1 != p2:
                message_box("Passwords do not match!")
                return
            ok = db.verify_token_and_reset_password(t, p1)
            if ok:
                forgot_pwd_frame.destroy()
                student_login()
                message_box("Password reset successful. \n Please login.")

            else:
                message_box("Invalid or expired token.")
        submit_reset_btn.config(command=on_submit_reset)

    
    def on_submit_forgot():
        matric_val = matric_number_entry.get().strip()

        # if the field is empty
        if not matric_val:
            message_box("Please enter matric number")
            return

        # check that matric exists first
        try:
            student = db.get_student_db(matric_val)     # returns dictionary or None
        except Exception as e:
            print(f"Error get_student_db raised: {e}")
            message_box("Error checking matric. Try again.")
            return

        #  incorrect matric number gives me this
        if not student:
            message_box("Incorrect matric number")
            return

        user_email = student.get('email')
        if not user_email:
            # if student exists but has no email in the database (which is not possible my create function has done all checking))
            message_box("No email on file for this matric. \nContact admin.")
            # optional: reveal reset widgets for admin/dev use
            # reveal_reset_widgets()
            return

        # create reset entry in DB; expects (token, user_email)
        try:
            result = db.create_password_reset_entry(matric_val, ttl_minutes=10)
        except Exception as e:
            print(f"Error create_password_reset_entry raised: {e}")
            message_box("Failed to create reset token. \nTry again!.")
            return

        token = None
        email_from_result = None
        if result is None:
            message_box("Failed to create reset token. Try again!.")
            return
        elif isinstance(result, tuple):
            token, email_from_result = result
        elif isinstance(result, str):
            token = result
            email_from_result = user_email
        else:
            print(f"Unexpected create_password_reset_entry return: {result}")
            message_box("Failed to create reset token. \nTry again!.")
            return

        # prefer database email if returned, otherwise use student.email
        target_email = email_from_result or user_email

        # Attempt to send via Outlook
        sent = send_via_gmail(target_email, token)
        if sent:
            print(f"------------------------------------")
            print(f"Token sent to {target_email}.")
            print(f"Matric Number: {matric_val}")
            print(f"Token: {token}")
            print(f"------------------------------------")
            message_box(f"Token sent to your mail. \nProceed to change password")
            reveal_reset_widgets(prefill_token=None)
        else:
            # fallback: print token and reveal reset widgets for dev/testing
            print(f"------------------------------------")
            print(f"Could not send email")
            print(f"Matric Number: {matric_val}")
            print(f"Token: {token}")
            print(f"------------------------------------")
            message_box("Failed to send email. \nToken printed to console.")
            # reveal_reset_widgets(prefill_token=token)
            reveal_reset_widgets(prefill_token=None)

    submit_forgot_pwd.config(command=on_submit_forgot)


# -----------------------------------------------------------
# Call For Functions I Created 
# -----------------------------------------------------------
welcome_page()


window.mainloop()

"""
Thank you for checking my code
"""