import os

class Config:
    # SQLITE_DB_NAME = "contacts.db"
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_4hv1QcztYINm@ep-quiet-grass-a47k35sq-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")
    SQLALCHEMY_TRACK_MODIFICATIONS=False