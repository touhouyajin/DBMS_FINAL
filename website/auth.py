from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import yt_dlp
auth = Blueprint('auth', __name__)
urls = ['https://youtu.be/ovTiSA9T-RU?si=H5r_oO7-tboMBeYB','https://youtu.be/kkUWlcjmOew?si=LYhySQt4XrsUFOxP']
def get_URL_from_index(index):
    return urls[int(index)] 


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user,remember=True)

                return redirect(url_for('view.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email not exsist", category='error')
    return render_template("login.html",user = current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("logout.html",user = current_user)


@auth.route("/sigh-up", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        firstName = data.get("firstName")
        password1 = data.get("password1")
        password2 = data.get("password2")
        if len(email) < 4:
            flash("Email address must be more than 4 characters", category="error")
        elif len(firstName) < 2:
            flash("First name must be more than 1 characters", category="error")
        elif len(password1) < 7:
            flash(
                "Password is too short.\nPassword must be more than 7 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:

            if User.query.filter_by(email=email).first():
                flash("User is already exsisted", category="error")
                return render_template("sigh-up.html")

            new_user = User(email=email, password=generate_password_hash(
                password1, method="sha256"), first_name=firstName)
            login_user(new_user)
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully", category="success")
            return redirect(url_for('view.home'))

    return render_template("sigh-up.html",user = current_user)


@auth.route('/search', methods=['POST'])
def search():
    youtube_url = request.form['youtube_url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
        }],
    }
    audio_url = ""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_url = info_dict['url']

    return render_template('play.html', audio_url=audio_url,user = current_user)

@auth.route('/play/<path:index>',methods=['GET'])
def play(index):
    youtube_url = get_URL_from_index(index)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'webm',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        audio_url = info_dict['url']
    playlist_data = [
        {'title': 'Song 1', 'artist': 'Artist 1', 'audio_url': audio_url},
        {'title': 'Song 2', 'artist': 'Artist 2', 'audio_url': audio_url},
        {'title': 'Song 3', 'artist': 'Artist 3', 'audio_url': 'song3.webm'},
    ]
    return render_template('play.html', playlist_data=playlist_data, user = current_user)

