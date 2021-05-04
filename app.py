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



        
