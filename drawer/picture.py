from drawer import app, send_file, login_required, music_list, flask_login


@app.route('/picture/<image_name>')
@login_required
def send_image(image_name):
    current = str(flask_login.current_user.id)
    return send_file(music_list[current].search(image_name).capture)
