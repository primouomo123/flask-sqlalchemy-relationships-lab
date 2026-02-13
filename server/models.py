from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# TODO: add association table
session_speaker = db.Table('session_speaker', metadata,
                           db.Column('session_id', db.Integer, db.ForeignKey('sessions.id', ondelete='CASCADE'), primary_key=True),
                           db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id', ondelete='CASCADE'), primary_key=True)
)

# TODO: set up relationships for all models
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Relationship to Session
    sessions = db.relationship('Session', back_populates='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer)

    # Foreign key to Event
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # Relationship to Event
    event = db.relationship('Event', back_populates='sessions')

    # Relationship to Speaker
    speakers = db.relationship('Speaker', secondary=session_speaker, back_populates='sessions', passive_deletes=True)


    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Relationship to Bio
    bio = db.relationship('Bio', back_populates='speaker', uselist=False, cascade='all, delete-orphan')

    # Relationship to Session
    sessions = db.relationship('Session', secondary=session_speaker, back_populates='speakers', passive_deletes=True)

    def __repr__(self):
        return f'<Speaker {self.id}, {self.name}>'

class Bio(db.Model):
    __tablename__ = 'bios'

    id = db.Column(db.Integer, primary_key=True)
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer)

    # Foreign key to Speaker
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    # Relationship to Speaker
    speaker = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f'<Bio {self.id}, {self.bio_text}>'
