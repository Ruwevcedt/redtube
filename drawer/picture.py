from drawer import app, send_file, login_required


@app.route('/picture/<image_name>')
@login_required
def send_image(image_name):
    return send_file('../picture/' + image_name)
