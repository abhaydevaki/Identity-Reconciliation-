from flask import Flask, request, jsonify
from sqlalchemy import select
from models import db, init_db, Contact
from config import Config
from flask_cors import CORS
from flask_migrate import Migrate
import logging

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

init_db(app)
migrate = Migrate(app, db)

# # Setup console logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info("Flask App startup")

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

    if existing_contacts:
        # Identify all primary contacts from the results
        primary_contacts = [c for c in existing_contacts if c.linkPrecedence == "primary"]

        if len(primary_contacts) > 1:
            # If multiple primaries exist, determine the oldest one
            oldest_primary = min(primary_contacts, key=lambda c: c.createdAt)

            # Convert all other primaries to secondary and link them to the oldest
            for contact in primary_contacts:
                if contact.id != oldest_primary.id:
                    contact.linkPrecedence = "secondary"
                    contact.linkedId = oldest_primary.id
                    db.session.commit()

        # Re-fetch updated contacts
        query = select(Contact).filter(
            (Contact.email == email) | (Contact.phoneNumber == phoneNumber)
        )
        updated_contacts = db.session.execute(query).scalars().all()

        # Identify the primary contact again after updates
        primary_contact = min(updated_contacts, key=lambda c: c.createdAt)
        emails = [primary_contact.email] if primary_contact.email else []
        phoneNumbers = [primary_contact.phoneNumber] if primary_contact.phoneNumber else []

        # Append secondary contact details
        for contact in updated_contacts:
            if contact.id != primary_contact.id:
                if contact.email and contact.email not in emails:
                    emails.append(contact.email)
                if contact.phoneNumber and contact.phoneNumber not in phoneNumbers:
                    phoneNumbers.append(contact.phoneNumber)

        secondary_ids = [c.id for c in updated_contacts if c.id != primary_contact.id]


        return jsonify({
            "contact": {
                "primaryContatctId": primary_contact.id,
                "emails": list(emails),
                "phoneNumbers": list(phoneNumbers),
                "secondaryContactIds": secondary_ids
            }
        })



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