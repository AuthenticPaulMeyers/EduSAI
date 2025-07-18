from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# initialise the database
db = SQLAlchemy()

# Users table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(32), nullable=False, unique=True)
    phonenumber = db.Column(db.String(30), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f'User>>>{self.id}'

# Messages table
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id', ondelete="CASCADE"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(30), nullable=False, default='user')

    user = db.relationship('User', backref='messages', lazy=True)
    language = db.relationship('Language', backref='messages', lazy=True)
    subject = db.relationship('Subject', backref='messages', lazy=True)

    def to_dict(self):
        return {
            "role": self.role, 
            "subject": self.subject.name, 
            "content": self.content,
            "created_at": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "updated_at": self.updated_at
        }
    def __repr__(self) -> str:
        return f'Message>>>{self.id}'

# Languages table
class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'Language>>>{self.id}'
    
# Subjects table
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'Subject>>>{self.id}'

