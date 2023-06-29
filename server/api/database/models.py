from .db import db
from datetime import datetime

class File(db.EmbeddedDocument):
    filename = db.StringField(required=True)
    type = db.StringField( required=True)
    length = db.IntField(min_value=0)
    frames = db.IntField(min_value=0)
    rate = db.IntField(min_value=0)
    fps = db.IntField(min_value=0)

class Activity(db.Document):
    name = db.StringField(required=True, unique=True)
    files = db.ListField(db.EmbeddedDocumentField(File))

class Analysis(db.Document):
    time = db.DateTimeField(default=datetime.now)
    id_activity = db.ReferenceField(Activity)
    start = db.IntField(min_value=0) 
    end = db.IntField(min_value=0)
    indicators = db.ListField(db.StringField())

class User(db.Document):
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    email = db.EmailField(required=True, unique=True)
    phone_numbers = db.ListField(db.StringField(max_length=20))
    is_active = db.BooleanField(default=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    password = db.StringField(required=True, min_length=6)
    meta = {
        'collection': 'users',
        'strict': False,
        'indexes': [
            'email',
            'phone_numbers'
        ]
    }


