News Nexus 📰

News Nexus is a dynamic web app that aggregates and displays the latest news, offering a clean and responsive user experience.

📖 About
News Nexus is a Django-based web app that fetches and displays live news articles in an elegant, responsive design.
It also supports user authentication, Google OAuth login, and email services configured via SMTP.

✨ Features
📰 Aggregates real-time news content.

👤 User authentication (Signup/Login).

🔑 Google OAuth 2.0 Authentication.

📧 Email notifications (SMTP setup via Gmail).

📱 Responsive and clean UI using SCSS and JS.

🔐 Secure environment management with .env.

🚀 Installation and Setup
Clone the repository

bash
Copy
Edit
git clone https://github.com/MrWings22/News_Nexus.git
cd News_Nexus
Create and activate a virtual environment

bash
Copy
Edit
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up the .env file

Create a .env file inside the project root and add:

env
Copy
Edit
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
⚡ Important: Never commit the .env file to GitHub!

Run migrations

bash
Copy
Edit
python manage.py migrate
Create a Superuser

bash
Copy
Edit
python manage.py createsuperuser
You'll be asked to enter:

Username

Email

Password

Start the development server

bash
Copy
Edit
python manage.py runserver
Access the app Go to: http://127.0.0.1:8000/

🛠 Project Structure
csharp
Copy
Edit
News_Nexus/
│
├── .vscode/            # VSCode settings
├── news_project/       # Django project
│   ├── settings.py     # Configurations (.env reading)
│   ├── urls.py         # URL routes
│   ├── templates/      # HTML files
│   ├── static/         # CSS, JS, Images
│   └── manage.py       # Django manager
├── requirements.txt    # Required Python packages
├── LICENSE             # MIT License
└── README.md           # You are here!
🔥 Tech Stack
Backend: Django (Python 3.10+)

Frontend: HTML5, CSS3, SCSS, JavaScript

Database: SQLite (default) – easily switchable

Auth: Django Auth + Google OAuth

Email: Gmail SMTP backend

🛡️ License
This project is licensed under the MIT License.

