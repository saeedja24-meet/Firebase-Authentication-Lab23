from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config={  
    'apiKey': "AIzaSyDDt_BZP5_FE4v0WvFfxkvR9snMFKm9o_8",
    'authDomain': "firstone-e6dd6.firebaseapp.com",
    'projectId': "firstone-e6dd6",
    'storageBucket': "firstone-e6dd6.appspot.com",
    'messagingSenderId': "978481786131",
    'appId': "1:978481786131:web:a42460d9b38a6a3d787ee6",
    'measurementId': "G-JW3NXNX6B3",
    'databaseURL':""
    }
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
app=Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for("add_tweet"))
       except:
            error = "Authentication failed"
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for("add_tweet"))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signupGo():
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin.html'))

if __name__ == '__main__':
    app.run(debug=True)