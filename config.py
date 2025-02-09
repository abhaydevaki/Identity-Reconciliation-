import os

class Config:
    SQLITE_DB_NAME = "contacts.db"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_DB_NAME}")
    SQLALCHEMY_TRACK_MODIFICATIONS=False