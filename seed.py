from app import app
from models import db, User, Note

db.drop_all()
db.create_all()

user1 = User.register(
    username="andrepautin",
    password="itsasecret",
    email="blahblahblah@gmail.com",
    first_name="andre",
    last_name="pautin"
)

user2 = User.register(
    username="celineyu",
    password="itsalsoasecret",
    email="blahblahblah2@gmail.com",
    first_name="celine",
    last_name="yu"
)
db.session.add_all([user1, user2])
db.session.commit()

note1 = Note(
    title="Seed Title",
    content="blah blah blah",
    owner=user1.username
)

note2 = Note(
    title="Seed Title2",
    content="blah blah blah2",
    owner=user2.username
)

db.session.add_all([note1, note2])
db.session.commit()
