from flask import Blueprint, render_template, redirect, url_for, session
from flask_dance.contrib.google import google

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/dashboard')
def dashboard():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    return render_template('dashboard.html', google_info=resp.json())

@bp.route('/signin')
def signin():
    return render_template('auth.html')

@bp.route('/signup')
def signup():
    return render_template('auth.html')

@bp.route('/logout')
def logout():
    token = google.token["access_token"]
    resp = google.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": token},
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert resp.ok, resp.text
    del session['google_oauth_token']
    return redirect(url_for('main.home'))