from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    comments = db.relationship('Comment', backref='user', lazy=True)
    ranks = db.relationship('Rank', backref='user', lazy=True)
    planned_trips = db.relationship('Trip', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.id}>'


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    activities = db.relationship('Activity', backref='trip', lazy=True)
    comments = db.relationship('Comment', backref='trip', lazy=True)
    maps = db.relationship('Map', backref='trip', lazy=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Trip {self.id}>'


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)

    def __repr__(self):
        return f'<Activity {self.id}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'


class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)

    def __repr__(self):
        return f'<Map {self.id}>'


class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Rank {self.id}>'