from flask import Flask, request, redirect, g, render_template, session
from db import Database
from passlib.hash import pbkdf2_sha256

app = Flask(__name__, )

# Secret Key for session
app.secret_key = b'CS375@SUMMER@ABDULLAH&HAJUN!'

# db:
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Maybe make a general home page
@app.route('/')
def index():
    return render_template("landing.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['password']
        if username and passwd:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(passwd, user['passwd']):
                    session['user'] = user
                    return redirect('/')
            else:
                message = "Incorrect username or password"
    return render_template("login.html", message=message)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first']
        last_name = request.form['last']
        passwd = request.form['passwd']
        conf_passwd = request.form['confirm_pass']
        if passwd != conf_passwd:
            message = "Please confirm your password again"
        # check if username already exists:
        else:
            user = get_db().get_user(username)
            if user:
                message = "User already exists"
            else:
                encrypted_pass = pbkdf2_sha256.encrypt(passwd, rounds=200000, salt_size=16)
                get_db().create_user(username, first_name, last_name, encrypted_pass)
                return redirect('/login')
    return render_template('/create_account.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

## Add the generic function here

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port=8080, debug=True)
