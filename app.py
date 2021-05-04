from flask import Flask, render_template, redirect, request, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Note
from forms import RegisterUserForm, AddNoteForm, UpdateNoteForm, LoginUserForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "secrets"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def redirect_to_register():
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

        curr_users = db.session.query(User.username).all()
        if username in curr_users:
            form.username.errors["Username already exists!"]
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

            return redirect(f"/users/{session['username']}")

    else:
        return render_template("register_user_form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ renders log in form; authenticates login info """
    form = LoginUserForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Bad name/password"] 
            form.password.errors = ["Bad name/password"] 
            return render_template("login_form.html", form=form)

    else:
        return render_template("login_form.html", form=form)
            
@app.route("/users/<username>")
def display_user_info(username):
    """ show details of user if they are logged in """


    if session.get("username") == username:
        user = User.query.get(username)
        return render_template("user_info.html", user=user)
    else:
        return redirect("/login")



@app.route("/logout", methods=["POST"])
def logout():
    """ logs a user out and redirects to homepage"""
    session.pop("username", None)
    return redirect("/")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    user = User.query.get(username)
    notes = Note.query.filter("owner"==user.username).all()

    for note in notes:
        db.session.delete(note)

    db.session.delete(user)
    db.session.commit()

    session.pop("username", None)
    return redirect("/login")

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_notes(username):
    if session["username"] == username:
        user = User.query.get(username)
        form = AddNoteForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            note = Note(title=title, content=content, owner=username)
            db.session.add(note)
            db.session.commit()

            return redirect(f"/users/{username}")
            
        else:
            return render_template("add_note_form.html", form=form)      
    
    else:
        return redirect("/login")      

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """update a note"""

    note = Note.query.get(note_id)
    if session["username"] == note.owner:
        form = UpdateNoteForm(obj=note)

        if form.validate_on_submit():
            note.title = form.title.data
            note.content = form.content.data

            db.session.commit()

            return redirect(f"/users/{note.owner}")
            
        else:
            return render_template("update_note_form.html", form=form)      
    
    else:
        return redirect("/login") 

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """deletes a note"""

    note = Note.query.get_or_404(note_id)
    if session["username"] == note.owner:
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{session['username']}")

    else:
        return redirect("/login")




        

