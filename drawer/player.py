from drawer import app, redirect, render_template, send_file, url_for, login_required, music_list


@app.route('/player')
@login_required
def player():
    # FIXME 'musiclist'
    return render_template('player.html', musiclist=music_list) if music_list else redirect(url_for('charge'))


@app.route('/player/<music_name>')
@login_required
def play_music(music_name):
    return send_file('../music/' + music_name, mimetype='Content-Type: audio/mp4; charset=utf32')


