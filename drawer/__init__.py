from flask import Flask, render_template, request, redirect, url_for, session, send_file
import flask_login
from core.audio_handler import MusicList
from flask_login import login_required
import os


# Music Init

music_list = MusicList("music/")

# Music Init

app = Flask(__name__)
app.template_folder = "../templates"
app.static_folder = "../static"
app.secret_key = os.urandom(24)


# Login Function Setting

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
from core import _login

# Login Function Setting


from drawer import index
from drawer import charge
from drawer import player
from drawer import picture
