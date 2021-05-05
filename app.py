from flask import Flask, render_template, redirect, request, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Note
from forms import RegisterUserForm, AddNoteForm, UpdateNoteForm, LoginUserForm, DeleteForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "secrets"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
    """"redirects to users/<username> if session has a username 
        else returns homepage html
    """
    if session.get("username"):
        return redirect(f"/users/{session['username']}")
    else:    
        return render_template("homepage.html")


#--------------------------USER ROUTES-----------------------

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """ renders user registation html; handles register user form submission"""

    if session.get("username"):
        return redirect(f"users/{session['username']}")

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # write custom validator for this, separate concerns?
        curr_usernames = [u.username for u in db.session.query(User.username).all()]

        curr_user_emails = [u.email for u in db.session.query(User.email).all()]

        if username in curr_usernames and email not in curr_user_emails:
            form.username.errors = ["Username already exists!"]
            return render_template("register_user_form.html", form=form)

        if email in curr_user_emails and username not in curr_usernames:
            form.email.errors = ["Email already in use!"]
            return render_template("register_user_form.html", form=form)

        if email in curr_user_emails and username in curr_usernames:
            form.username.errors = ["Username already exists!"]
            form.email.errors = ["Email already in use!"]
            return render_template("register_user_form.html", form=form)

        else:
            user = User.register(
                username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name)

            db.session.add(user)
            db.session.commit()

            session["username"] = user.username
            flash("Sign Up Complete!")

            return redirect(f"/users/{session['username']}")

    else:
        return render_template("register_user_form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ renders log in form; authenticates login info """

    if session.get("username"):
        flash("You're already logged in!")
        return redirect(f"users/{session['username']}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            flash("Incorrect credentials")
            return render_template("login_form.html", form=form)

    else:
        return render_template("login_form.html", form=form)
            
@app.route("/users/<username>")
def display_user_info(username):
    """ show user detail if correct user logged in 
        else redirect to homepage
    """

    if session.get("username") != username:
        return redirect("/login")
    
    form = DeleteForm()
    user = User.query.get(username)
    return render_template("user_info.html", user=user, form=form)



@app.route("/logout", methods=["POST"])
def logout():
    """ logs a user out and redirects to homepage"""

    form = DeleteForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect("/")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ deletes current users notes and user data from database
        redirects to homepage
    """
    form = DeleteForm()

    if form.validate_on_submit():

        user = User.query.get_or_404(username)
        Note.query.filter("owner"==user.username).delete()

        db.session.delete(user)
        db.session.commit()

        session.pop("username", None)

    return redirect("/")


#-------------------------- NOTES ROUTES--------------------------------    

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_notes(username):
    """renders add note form; handles add note submission"""

    if session.get("username") != username:
        return redirect("/login"), 401

    user = User.query.get_or_404(username)
    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, 
                    content=content, 
                    owner=username)

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")
        
    else:
        return render_template("add_note_form.html", form=form)
        

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """update a note in database and redirects back to user info page"""

    if session.get("username") != note.owner:
        return redirect("/login"), 401
        
    note = Note.query.get_or_404(note_id)
    form = UpdateNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")
            
    else:
        return render_template("update_note_form.html", form=form)      
    
        

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """deletes a note"""

    if session.get("username") != note.owner:
        return redirect("/login"), 401
    
    if form.validate_on_submit():
        note = Note.query.get_or_404(note_id)
        form = DeleteForm()
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{session['username']}")




        

