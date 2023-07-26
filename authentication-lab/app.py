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
    'databaseURL':"https://meet-project1-default-rtdb.europe-west1.firebasedatabase.app/"
    }
gameAndImages={
    "darkSouls":"https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/92db2e21-619b-46d3-ba25-95303ecc1903/db7m27z-0e8a2cce-dcf3-47cb-8055-1bdcd945fdbf.jpg/v1/fill/w_900,h_507,q_75,strp/dark_souls_3_wallpaper_by_allofgamewallpapers_db7m27z-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NTA3IiwicGF0aCI6IlwvZlwvOTJkYjJlMjEtNjE5Yi00NmQzLWJhMjUtOTUzMDNlY2MxOTAzXC9kYjdtMjd6LTBlOGEyY2NlLWRjZjMtNDdjYi04MDU1LTFiZGNkOTQ1ZmRiZi5qcGciLCJ3aWR0aCI6Ijw9OTAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.Gu99lH5oHaWHnBHH-l31OSY_Hx16GrzGMISFPcSo8ko",
    "cupHead":"https://image.api.playstation.com/vulcan/img/cfn/11307fd0s0uyV-ba4dy5E9qskf6CIntl28sAerYTFbYC7vPUBrfgp7zokliHVbVoJ5ghylOBamo2Q2i5pbEYxQKFnSsiLHaY.png",
    "overWatch2":"data:image/png;base64,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",
    "hearthstone":"https://logos-world.net/wp-content/uploads/2021/02/Hearthstone-Symbol.jpg",
    "GTA5":"https://upload.wikimedia.org/wikipedia/en/a/a5/Grand_Theft_Auto_V.png",

}
users={"":""}
firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
app=Flask(__name__)
db=firebase.database()
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
            login_session['user']['name']=email[0:len(email)-10]
            UID = login_session['user']['localId']
            users.update(login_session['user']['localId'])
            return redirect(url_for("store"))
       except Exception as e:
            print(e)
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
                login_session['user']['name']=email[0:len(email)-10]
                UID = login_session['user']['localId']
                return redirect(url_for("store"))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/store', methods=['GET', 'POST'])
def store():
    return render_template("store.html",gameAndImagesHtml=gameAndImages)


@app.route('/addGame/<string:name>')
def addGame(name):
    db.child("users").child(UID).child(games).push()
    print(db.child("users").child(UID).child(games).push({{gameName}}))
@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin.html',userHtml=UID))
if __name__ == '__main__':
    app.run(debug=True)