from drawer import app, send_file, login_required, music_list


@app.route('/picture/<image_name>')
@login_required
def send_image(image_name):
    return send_file(music_list.search(image_name).capture)
