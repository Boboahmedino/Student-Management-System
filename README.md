# 🎓 Olaneye Software Institute | Student Management System

A comprehensive desktop application for student management with ID card generation, email notifications, and secure authentication system.

## ✨ Features

### 🎯 Core Functionality
- **Multi-role Authentication** (Student, Admin)
- **Student Registration** with auto-generated matric numbers
- **ID Card Generation** with professional PDF export
- **Email Integration** for account notifications and password reset
- **Database Management** with MySQL backend

### 🎨 User Interfaces
- **Student Dashboard** with profile management
- **Admin Panel** with student data management
- **Responsive Design** with modern UI elements
- **Interactive Confirmation Dialogs**
- **Password Visibility Toggle**

### 🔒 Security Features
- Secure password hashing
- Password reset tokens with expiration
- Email verification system
- Session management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Tkinter (usually comes with Python)
- PIL/Pillow library
- MySQL

### Installation
1. Clone the repository:
```bash
git clone https://github.com/boboahmedino/student-management-system.git
```

2. Install required dependencies:
```bash
pip install pillow python-dotenv
```

3. Set up environment variables:
```bash
.env
```

### 🏃‍♂️ Running the Application
```bash
python OSI.py
```

## 📁 Project Structure

```
student-management-system/
├── OSI.py                 # Main application file
├── database.py            # Database operations
├── test.py                # test the gmail ports
├── user.png               # image for button
└── README.md              # This file
```

## 🎮 Usage Guide

### For Students:
1. **Register** with personal details and photo upload
2. **Login** with matric number and password
3. **Access Dashboard** to view profile, edit information, and generate ID cards
4. **Change password** securely

### For Administrators:
1. **Login** with admin credentials
2. **View all students** in a sortable table
3. **Export data** to CSV format
4. **Manage student records** (view, delete)

## 🛠️ Technical Implementation

### Database Schema
The system uses MySQL with tables for:
- Students (personal info, credentials)
- Admin users
- Password reset tokens

### Email Integration
- SMTP with Gmail support
- HTML email templates
- Token-based password reset system
- Account creation notifications

### ID Card Generation
- Dynamic PDF creation with student photos
- Download functionality

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:

```ini
gmail_user=your.email@gmail.com
gmail_password=your_app_password
```

## 🎨 Customization

### Color Scheme
The primary color scheme uses `#350159` (deep purple) which can be modified in the `bg_color` variable.

### Email Templates
HTML email templates are embedded in the code and can be customized for different institutional branding.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes 
4. Push to the branch 
5. Open a Pull Request

## 👨‍💻 Developer

**Olaneye Ahmed Oladapo**
- Github: [Boboahmedino](https://github.com/Boboahmedino)
- LinkedIn: [Olaneye Ahmed](https://www.linkedin.com/in/olaneye/)

## 🙏 Acknowledgments

- Tkinter community for GUI resources
- PIL/Pillow team for image processing capabilities
- Python community for extensive documentation

---

⭐ **Star this repo if you found it helpful!**
