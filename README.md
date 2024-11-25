Gettings started with building a Flask app that includes a dashboard, a home page, and Google sign-in using Flask-Dance. Here's a structured example to guide you through the process:

### Project Structure
```
my_flask_app/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   └── static/
│       └── style.css
│
├── config.py
├── requirements.txt
└── run.py
```

### Step-by-Step Guide

1. **Set Up Your Environment**
   - Create a virtual environment and install Flask and Flask-Dance:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install Flask Flask-Dance
     ```

2. **Create `config.py`**
   ```python
   import os

   class Config:
       SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
       GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
       GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
   ```

3. **Initialize Flask App in `app/__init__.py`**
   ```python
   from flask import Flask
   from flask_dance.contrib.google import make_google_blueprint, google
   from config import Config

   def create_app():
       app = Flask(__name__)
       app.config.from_object(Config)

       google_bp = make_google_blueprint(
           client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
           client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
           redirect_to='dashboard'
       )
       app.register_blueprint(google_bp, url_prefix='/login')

       from . import routes
       app.register_blueprint(routes.bp)

       return app
   ```

4. **Define Routes in `app/routes.py`**
   ```python
   from flask import Blueprint, render_template, redirect, url_for
   from flask_dance.contrib.google import google

   bp = Blueprint('main', __name__)

   @bp.route('/')
   def home():
       return render_template('home.html')

   @bp.route('/dashboard')
   def dashboard():
       if not google.authorized:
           return redirect(url_for('google.login'))
       resp = google.get('/plus/v1/people/me')
       assert resp.ok, resp.text
       return render_template('dashboard.html', google_info=resp.json())
   ```

5. **Create Templates**
   - `app/templates/base.html`
     ```html
     <!DOCTYPE html>
     <html lang="en">
     <head>
         <meta charset="UTF-8">
         <title>{% block title %}{% endblock %}</title>
         <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
     </head>
     <body>
         <nav>
             <a href="{{ url_for('main.home') }}">Home</a>
             <a href="{{ url_for('main.dashboard') }}">Dashboard</a>
         </nav>
         {% block content %}{% endblock %}
     </body>
     </html>
     ```

   - `app/templates/home.html`
     ```html
     {% extends 'base.html' %}
     {% block title %}Home{% endblock %}
     {% block content %}
     <h1>Welcome to the Home Page</h1>
     <a href="{{ url_for('google.login') }}">Sign in with Google</a>
     {% endblock %}
     ```

   - `app/templates/dashboard.html`
     ```html
     {% extends 'base.html' %}
     {% block title %}Dashboard{% endblock %}
     {% block content %}
     <h1>Welcome to the Dashboard</h1>
     <p>User info: {{ google_info }}</p>
     {% endblock %}
     ```

6. **Run the App**
   - Create `run.py`:
     ```python
     from app import create_app

     app = create_app()

     if __name__ == '__main__':
         app.run(debug=True)
     ```

7. **Install Requirements**
   - Create `requirements.txt`:
     ```
     Flask
     Flask-Dance
     ```

8. **Set Environment Variables**
   - Set your environment variables for the Google OAuth client ID and secret:
     ```bash
     export GOOGLE_OAUTH_CLIENT_ID='your-client-id'
     export GOOGLE_OAUTH_CLIENT_SECRET='your-client-secret'
     export SECRET_KEY='your-secret-key'
     ```

This should give you a basic Flask app with a home page, a dashboard, and Google sign-in functionality. Let me know if you need any more details or help with specific parts!