from flask import Flask, render_template, redirect, request, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterUserForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "secrets"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ECHO_SQLALCHEMY"] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def redirect():
    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        curr_users = User.query("username").all()
        if username in curr_users:
            form.username.errors["Username already exists!"]
        else:
            user = User(
                username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name)

            db.session.add(user)
            db.session.commit()

            session["username"] = user.username

            return redirect("/secret")

    else:
        return render_template("register_user_form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ renders log in form; authenticates login info """
    form = LoginUserForm()

    if form.validate_on_submit:
        username=form.username.data
        password=form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect("/secret")
        else:
            form.username.errors = ["Bad name/password"]    

    else:
        return render_template("login_form.html", form=form)
            
@app.route("/users/<username>")
def secret(username):
    """ show details of user if they are logged in """

    if session["username"] == username:
        user = User.query.get(username)
        return render_template("user_info.html", user=user)
    else:
        return redirect("/login")



@app.route("/logout")
def logout():
    """ logs a user out and redirects to homepage"""
    session.pop("username", None)
    return redirect("/")





        

