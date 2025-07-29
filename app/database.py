# app/database.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@"
        f"{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)


def get_db():
    return db
