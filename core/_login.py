from flask import Flask, g, Response, render_template, send_file, request, redirect, session, escape, redirect, url_for
from drawer import app, flask_login, login_manager
import datetime
import hashlib


class EncodeObj:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.secret_key_byte = self.__str_to_byte_array(self.secret_key)

    @staticmethod
    def __str_to_byte_array(data: str) -> [int]:
        return [ord(x) for x in data]

    @staticmethod
    def __xor_encode(key: [int], _value: [int]) -> str:
        return "".join([chr(_ ^ __) for _, __ in zip(key, _value)])

    @property
    def __salted_key(self) -> str:
        return self.__xor_encode(self.secret_key_byte, [ord(x) for x in str(datetime.datetime.now().date())])

    def encoded_username(self, username: str) -> str:
        checksum = hashlib.md5(
            self.__xor_encode(self.__str_to_byte_array(username), self.__str_to_byte_array(self.__salted_key)).encode(
                'utf-8'))
        return str(checksum.digest()).replace('/', '').replace('\\', '')


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

    def username_check(self, encoded_data: str) -> [str]:
        return [user_id for user_id in self.user_data.keys() if cryption.encoded_username(user_id) == encoded_data]


users = SinUsers()
users.add_user("Arheneos", cryption.encoded_username("Arheneos"))  # TODO : Load Users from mongodb
users.add_user("Ruwevcedt", cryption.encoded_username("Ruwevcedt"))
users.add_user("boco114", cryption.encoded_username("boco114"))
users.add_user("Horo", cryption.encoded_username("Horo"))
users.add_user("collride", cryption.encoded_username("collride"))
users.add_user("AngryBoy9623", cryption.encoded_username("AngryBoy9623"))
users.add_user("BWwaffle", cryption.encoded_username("BWwaffle"))
users.add_user("test", "test")  # delete these on real use


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    print(username)
    if not (username, request.form['password']) in users.user_data.items():
        return
    print(f"user_loader : {username}")
    user = User()
    user.id = username
    flask_login.login_user(user)

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = True
    return user.id


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST' and request.form['username'] == 'test':
        _user = user_loader('test')
        flask_login.login_user(_user)
        return redirect('/player')
    return render_template("login.html")


@app.route('/login/<path:path>')
def login_function_(path: str):
    check_sum = users.username_check(
        path if not '/' in path or '\\' in path else path.replace('/', '').replace('\\', ''))
    # if for test
    if check_sum:
        _user = user_loader(check_sum[0])
        flask_login.login_user(_user)
        return redirect("/player")
    return redirect("/login")


@login_manager.unauthorized_handler
def unauthorized_handler():
    print(flask_login.current_user)
    print("are you fake user?")
    return redirect(url_for('login_page'))
