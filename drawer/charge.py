from drawer import app, request, login_required, render_template, redirect, url_for, flask_login
from core import youtube_handler
import threading


@app.route('/charge', methods=['GET', 'POST'])
@login_required
def charge():
    current = flask_login.current_user.get_id()

    def download(user: str, url: str):
        youtube_handler.VideoHandler(user=user, url=url).download_sequence()


    if request.method == 'POST':
        worker = threading.Thread(target=download, args=(current, request.form['youtube_link'],))
        worker.start()
        return redirect(url_for('player'))
    return render_template('charge.html')
