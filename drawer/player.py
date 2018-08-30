from drawer import app, redirect, render_template, send_file, url_for, login_required, music_list, flask_login
import os


@app.route('/player')
@login_required
def player():
    current = str(flask_login.current_user.id)
    return render_template('player.html', music_list=music_list[current] if music_list[current] else redirect(url_for('charge')))


@app.route('/player/<path:path>')
@login_required
def play_music(path):
    current = str(flask_login.current_user.id)
    return send_file(music_list[current].search(os.path.splitext(path)[0]).file_path, mimetype='Content-Type: audio/mp4; charset=utf32')
