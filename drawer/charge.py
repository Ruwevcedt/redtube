from drawer import app, request, login_required, render_template, redirect, url_for
from core import youtube_handler, audio_handler


@app.route('/charge', methods=['GET', 'POST'])
@login_required
def charge():

    # FIXME

    if request.method == 'POST':
        link = request.form['PLST']
        try:
            youtube_handler.vid_aud(link)
        except youtube_handler.pytube.exceptions.RegexMatchError:   # FIXME
            print('ign : ', link)
            pass

        global musiclist

        audio_handler.update_music()
        return redirect(url_for('player'))
    return render_template('charge.html')
