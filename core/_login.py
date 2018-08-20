from flask import Flask, g, Response, render_template, send_file, request, redirect, session, escape, redirect, url_for
from drawer import app, flask_login, login_manager
import datetime


class EncodeObj:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.secret_key_byte = self.__str_to_byte_array(self.secret_key)

    @staticmethod
    def __str_to_byte_array(data: str) -> [int]:
        return [ord(x) for x in data]

    @staticmethod
    def __xor_encode(key: [int], _value: [int]) -> str:
        return "".join([chr(_^__) for _, __ in zip(key, _value)])

    @property
    def __salted_key(self) -> str:
        return self.__xor_encode(self.secret_key_byte, [ord(x) for x in str(datetime.datetime.now().date())])

    def encoded_username(self, username: str) -> str:
        return self.__xor_encode(self.__str_to_byte_array(username), self.__str_to_byte_array(self.__salted_key))

    def decoded_data(self, encoded_data: str) -> str:
        return self.__xor_encode(self.__str_to_byte_array(encoded_data), self.__str_to_byte_array(self.__salted_key))


cryption = EncodeObj(secret_key="OriginalSin")


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
users.add_user("Arheneos", "asdf")      # TODO : Load Users from mongodb


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
    print(f"user_loader : {username}")
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


@app.route('/login/<path:path>')
def login_function_(path):
    print("api_login_function")
    print(path)
    crypted = cryption.decoded_data(path)
    if users.username_check(crypted):
        user = User()
        user.id = crypted
        flask_login.login_user(user)
        return redirect("/player")
    return redirect("/login")


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login_function'))
