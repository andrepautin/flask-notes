from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired

class RegisterUserForm(FlaskForm):
    """creates a form for a user to register"""

    username = StringField("USERNAME", 
                            validators=[InputRequired()])

    password = PasswordField("PASSWORD", 
                            validators=[InputRequired()])

    email = StringField("EMAIL", 
                        validators=[InputRequired()])

    first_name = StringField("FIRST NAME", 
                            validators=[InputRequired()])
    
    last_name = StringField("LAST NAME", 
                            validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    """creates a form for user to log inw"""

    username = StringField("USERNAME", 
                            validators=[InputRequired()])

    password = PasswordField("PASSWORD", 
                            validators=[InputRequired()])

class AddNoteForm(FlaskForm):
    """form to add note"""

    title = StringField("Title", 
                        validators=[InputRequired()])

    content = TextAreaField("Content", 
                            validators=[InputRequired()])

class UpdateNoteForm(FlaskForm):
    """form to update note"""

    title = StringField("Title", 
                        validators=[InputRequired()])

    content = TextAreaField("Content", 
                            validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """ form for deleting """                            
