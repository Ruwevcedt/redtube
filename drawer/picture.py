from drawer import app, send_file, login_required
import os


@app.route('/picture/<image_name>')
@login_required
def send_image(image_name):
    print(image_name)
    print(os.getcwd())
    print(os.path.abspath(f"picture/{image_name}"))
    print(os.path.exists(os.path.abspath(f"picture/{image_name}")))
    return send_file(os.path.abspath(f"picture/{image_name}"))
