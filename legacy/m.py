# -*- coding: utf-8 -*-

import urllib
from flask import Flask, request, render_template, session, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask.ext.session import Session
import os
import subprocess
from pytube import YouTube as yt
from glob import glob

class User(UserMixin):
    def __init__(self, user_id, passwd_hash):
        self.id = user_id
        self.password = passwd_hash

    def __repr__(self):
        r = {
                'user_id' : self.id,
                'user_password' : self.password
                }
        return str(r)

users = {
        'ruwevcedt' : User('ruwevcedt', 'wnstjr'),
        'colride' : User('colride', 'rldnr')
        }

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TESTING'] = False

login_manager = LoginManager()
login_manager.init_app(app)

Session(app)

@login_manager.user_loader
def load_user(user_id):
    return users[user_id]

@app.route('/')
def gate():
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        logger = request.form['USER']

        if logger not in users:
            return render_template('login.html')

        elif users[logger].password == request.form['PSWD']:
            session['user_id'] = logger
            login_user(load_user(logger), remember = True)

            return redirect(url_for('music', user_id = current_user))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('gate'))

musiclist = []
def update_music():
    for music in glob("../usbs/music/*"):
        musicname = music.split('/')[-1]

        musiclist.append({
            'track' : len(musiclist) + 1,
            'name' : musicname,
            'length' : 'unknown',
            'path' : "music/" + musicname
            })

@app.route('/music')
@login_required
def music():
    if len(musiclist) == 0:
        update_music()
    return render_template('music.html', musiclist = musiclist)

@app.route('/music/<musicname>')
@login_required
def musicQ(musicname):
    return send_file("../usbs/music/" + musicname, mimetype = 'Content-Type: audio/mpeg3; charset=utf32')

@app.route('/music/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
    return render_template('upload.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port = 80)
