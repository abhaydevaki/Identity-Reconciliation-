from flask import Flask, request, jsonify
from sqlalchemy import select
from models import db, init_db, Contact
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

init_db(app)


@app.route('/identify', methods=['POST'])
def identify():
    data = request.get_json()
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')

    # Fetch existing contacts that match email or phoneNumber
    query = select(Contact).filter(
        (Contact.email == email) | (Contact.phoneNumber == phoneNumber)
    )
    existing_contacts = db.session.execute(query).scalars().all()

    
    # If no existing contact, create a new one
    new_contact = Contact(
        email=email,
        phoneNumber=phoneNumber,
        linkPrecedence="primary"
    )
    db.session.add(new_contact)
    db.session.commit()


    return jsonify({
        "contact": {
            "primaryContatctId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }
    })


# Export the app for Vercel
def handler(event, context):
    return app(event, context)