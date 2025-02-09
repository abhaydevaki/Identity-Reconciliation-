from flask import Flask, request, jsonify
from sqlalchemy import select
from config import Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

init_db(app)



# Export the app for Vercel
def handler(event, context):
    return app(event, context)