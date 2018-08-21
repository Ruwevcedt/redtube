from flask import Flask, g, Response, render_template, send_file, request, redirect, session, escape, redirect, url_for
from drawer import app, flask_login, login_manager
import datetime
from hashlib import md5


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
        return md5(self.__xor_encode(self.__str_to_byte_array(username), self.__str_to_byte_array(self.__salted_key)).encode('utf-8'))

cryption = EncodeObj(secret_key="original_sin")


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

    def username_check(self, uid: str) -> [str]:
        return [user_id for user_id in self.user_data.keys() if cryption.encoded_username(user_id) == uid]

users = SinUsers()
users.add_user("Arheneos", cryption.encoded_username("Arheneos"))  # TODO : Load Users from mongodb
users.add_user("Ruwevcedt", cryption.encoded_username("Ruwevcedt"))
users.add_user("boco114", cryption.encoded_username("boco114"))
users.add_user("Horo", cryption.encoded_username("Horo"))
users.add_user("collride", cryption.encoded_username("collride"))
users.add_user("AngryBoy9623", cryption.encoded_username("AngryBoy9623"))
users.add_user("BWwaffle", cryption.encoded_username("BWwaffle"))
users.add_user("test", "test") # delete these on real use


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
def fake_login_page():
    if request.method == 'POST' and request.form['username'] == 'test':
        user = User()
        user.id = 'test'
        flask_login.login_user(user)
        return redirect('/player')
    return render_template("login.html")


@app.route('/login/<path:path>')
def login_function_(path: str):
    path_check = users.username_check(md5(path.encode('utf-8')))
    if path_check:
        user = User()
        user.id = path_check[0]
        flask_login.login_user(user)
        return redirect("/player")
    return redirect("/login")

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('fake_login_page'))
