from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    linkedId = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=True)
    linkPrecedence = db.Column(db.String(10), nullable=False)  # "primary" or "secondary"
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = db.Column(db.DateTime, nullable=True)

    def _repr_(self):
        return f"<Contact {self.id}: {self.email}, {self.phoneNumber}, {self.linkPrecedence}>"

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()