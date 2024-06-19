from config import db


class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, first_name, last_name, email, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.user_id = user_id

    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name}; Email {self.email}>"

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    contacts = db.relationship("Contact", backref="owner", lazy=True)


    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def __repr__(self):
        return f"<User {self.username}; Full Name {self.full_name}>"

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullName": self.full_name
        }