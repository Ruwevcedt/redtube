from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_session import Session
from shutil import copyfile
import os
import subprocess
import re
from glob import glob
from pytube import YouTube as YTB


def aud_dur(aud_path):
    process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', aud_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    matches = re.search(r'Duration:\s(?P<hh>\d+?):(?P<mm>\d+?):(?P<ss>\d+\.\d+?),', stdout.decode('utf-8'), re.DOTALL)

    hour, minute, second = int(matches['hh']), int(matches['mm']), float(matches['ss'])
    duration = str(3600 * hour + 60 * minute + second)[:6]

    print(aud_path, " : ", duration)
    return duration

def vid_aud(vid_url):
    yt = YTB(vid_url).streams.all()

    for index, stream in enumerate(yt):
        print(index, stream)

        if stream.mime_type == "audio/mp4":
            print("downloading : ", stream)
            yt[index].download("music/")
            return print("downlaoded : ", stream)

    return print("err : ", 'no audio/mp4 file')


class User(UserMixin):
    def __init__(self, user_id, user_pw):
        self.id, self.pw = user_id, user_pw

    def __repr__(self):
        return str({
            'user_id': self.id,
            'user_pw': self.pw
        })


users = {
    'ruwevcedt': User('ruwevcedt', 'wnstjr'),
    'colride': User('colride', 'rldnr')
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('req : ', request.form)

        user = request.form['USER']
        if user not in users:
            return render_template('login.html')

        elif users[user].pw == request.form['PSWD']:
            session['user_id'] = user
            login_user(load_user(user), remember=True)

            print('usr : ', current_user)
            return redirect(url_for('player'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return redirect(url_for('gate'))


musiclist = []


def upd_music():
    musics = glob("music/*")
    print(musics)

    for music in musics:
        musicname = music.split('/')[-1].split('.')
        print(musicname)

        if musicname[-1] == 'mp4':
            if not "music/" + musicname[0] + '.aac' in musics:
                print('log :', 'generating aac file')
                copyfile(
                    "music/{}.mp4".format(musicname[0]),
                    "music/{}.aac".format(musicname[0])
                )

                musicname = musicname[0] + '.aac'
                print(musicname)

                musiclist.append({
                    'track': len(musiclist) + 1,
                    'name': musicname,
                    'length': aud_dur(music),
                    'path': "player/" + musicname
                })
            else:
                pass
        else:
            musicname = musicname[0] + '.' + musicname[-1]
            print(musicname)

            musiclist.append({
                'track': len(musiclist) + 1,
                'name': musicname,
                'length': aud_dur(music),
                'path': "player/" + musicname
            })


@login_required
@app.route('/player')
def player():
    if len(musiclist) == 0:
        return redirect(url_for('charge'))

    return render_template('player.html', musiclist=musiclist)


@login_required
@app.route('/player/<musicname>')
def playmusic(musicname):
    print('ply : ', musicname)
    return send_file('music/' + musicname, mimetype='Content-Type: audio/mp4; charset=utf32')


@login_required
@app.route('/charge', methods=['GET', 'POST'])
def charge():
    if request.method == 'POST':
        print('req : ', request.form)

        link = request.form['PLST']
        print('inp : ', link)

        try:
            vid_aud(link)
        except:
            print('ign : ', link)
            pass

        global musiclist
        musiclist = []

        upd_music()
        return redirect(url_for('player'))

    return render_template('charge.html')

if __name__ == '__main__':
    app.run()
