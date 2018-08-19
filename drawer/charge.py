from drawer import app, request, login_required, render_template, redirect, url_for
from core import youtube_handler, audio_handler


@app.route('/charge', methods=['GET', 'POST'])
@login_required
def charge():

    # FIXME

    if request.method == 'POST':
        link = request.form['youtube_link']

        youtube_handler.VideoHandler.download_sequence(link)

        return redirect(url_for('player'))
    return render_template('charge.html')
