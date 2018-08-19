from drawer import app, request, login_required, render_template, redirect, url_for
from core import youtube_handler, audio_handler


@app.route('/charge', methods=['GET', 'POST'])
@login_required
def charge():

    # FIXME

    if request.method == 'POST':
        youtube_handler.VideoHandler(url=request.form['youtube_link']).download_sequence()
        return redirect(url_for('player'))
    return render_template('charge.html')
