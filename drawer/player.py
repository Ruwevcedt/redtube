from drawer import app, redirect, render_template, send_file, url_for, login_required, music_list


@app.route('/player')
@login_required
def player():
    return render_template('player.html', music_list=music_list) if music_list else redirect(url_for('charge'))


@app.route('/player/<path:path>')
@login_required
def play_music(path):
    return send_file(music_list.search(path).file_path, mimetype='Content-Type: audio/mp4; charset=utf32')


