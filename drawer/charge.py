from drawer import app, request, login_required, render_template, redirect, url_for
from core import youtube_handler, audio_handler
import threading


@app.route('/charge', methods=['GET', 'POST'])
@login_required
def charge():

    def download(url: str):
        youtube_handler.VideoHandler(url=url).download_sequence()

    if request.method == 'POST':
        worker = threading.Thread(target=download, args=(request.form['youtube_link'],))
        worker.start()
        return redirect(url_for('player'))
    return render_template('charge.html')
