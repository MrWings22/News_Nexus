# 📰 News Nexus

**News Nexus** is a dynamic Django-based web app that aggregates and displays the latest news with a clean, responsive user interface.

---

## 📖 About

News Nexus fetches and displays live news articles in an elegant way.  
It supports:
- User authentication
- Google OAuth login
- Email services via SMTP
- Secure environment variables

---

## ✨ Features

- 📰 Aggregates real-time news content.
- 👤 User authentication (Signup/Login).
- 🔑 Google OAuth 2.0 Authentication.
- 📧 Email notifications (Gmail SMTP setup).
- 📱 Responsive UI with SCSS and JavaScript.
- 🔐 Secure environment management using `.env`.

---

## 🚀 Installation and Setup

### Clone the repository
```bash
git clone https://github.com/MrWings22/News_Nexus.git
cd News_Nexus
```

### Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set up the `.env` file
Create a `.env` file in the root directory and add:
```env
SECRET_KEY=your-django-secret-key

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail-address@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-gmail-address@gmail.com

# Google OAuth Settings
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```
⚡ **Important:** Never commit your `.env` file to GitHub!

### Run migrations
```bash
python manage.py migrate
```

### Create a Superuser
```bash
python manage.py createsuperuser
```
Provide:
- Username
- Email
- Password

### Start the development server
```bash
python manage.py runserver
```

Access the app at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🛠 Project Structure

```
News_Nexus/
│
├── .vscode/            # VSCode settings
├── news_project/       # Django project
│   ├── settings.py     # Django settings (.env included)
│   ├── urls.py         # Project URL routes
│   ├── templates/      # HTML templates
│   ├── static/         # CSS, JS, images
│   └── manage.py       # Django management script
├── requirements.txt    # Python dependencies
├── LICENSE             # Project license
└── README.md           # This file
```

---

## 🔥 Tech Stack

- **Backend**: Django (Python 3.10+)
- **Frontend**: HTML5, CSS3, SCSS, JavaScript
- **Database**: SQLite (default; easily switchable)
- **Authentication**: Django Auth + Google OAuth
- **Email Service**: Gmail SMTP

---

## 🛡️ License

This project is licensed under the **MIT License**.

---
