from flask import Flask, g, Response, render_template, send_file, request, redirect, session, escape, redirect, url_for
from drawer import app, flask_login, login_manager


class SinUsers:

    __slots__ = (
        "user_data"
    )

    def __init__(self):
        self.user_data = {}

    def add_user(self, uid: str, pw: str):
        self.user_data.update({uid: pw})

    def password_check(self, uid: str, pw: str) -> bool:
        return self.user_data[uid] == pw

    def username_check(self, uid: str) -> bool:
        return True if uid in self.user_data.keys() else False


users = SinUsers()
users.add_user("asdf", "asdf")      # TODO : Load Users from mongodb


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    # print("user_loader : {}".format(username))
    if not users.username_check(username):
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    print(username)
    if not users.username_check(username):
        return
    print("user_loader : {}".format(username))
    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = users.password_check(username, request.form['password'])
    return user


@app.route('/login', methods=['GET', 'POST'])
def login_function():
    print("login_function")
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form['username']
        print(username)
        try:
            if users.password_check(username, request.form['password']):
                user = User()
                user.id = username
                flask_login.login_user(user)
                return redirect("/")
        except KeyError:
            return render_template("login.html")
        return redirect("/")
    return render_template("login.html")


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login_function'))