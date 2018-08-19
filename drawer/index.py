from drawer import app, redirect, url_for, login_required


@app.route('/')
@login_required
def gate():
    return redirect(url_for('player'))
