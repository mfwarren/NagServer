import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from . import db, login_manager
from sqlalchemy import desc


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    users = db.relationship('User', backref='roles', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    nags = db.relationship('Nag', backref='users', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %s>' % self.username


class Nag(db.Model):
    __tablename__ = 'nags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    frequency = db.Column(db.Integer)
    message_to_send = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entries = db.relationship('NagEntry', backref='nags', lazy='dynamic')

    @property
    def most_recent_entry(self):
        return self.entries.order_by(desc('time')).first()

    @property
    def days_until_next(self):
        days_since = (datetime.datetime.now() - self.most_recent_entry.time).days
        return self.frequency - days_since

    @property
    def entries_descending(self):
        return self.entries.order_by(desc('time'))

    @property
    def quickcheck_form(self):
        from .nag.forms import QuickCheckinForm
        form = QuickCheckinForm()
        return form

    def __repr__(self):
        return '<Nag %s>' % self.name


class NagEntry(db.Model):
    __tablename__ = 'nag_entries'
    id = db.Column(db.Integer, primary_key=True)
    nag_id = db.Column(db.Integer, db.ForeignKey('nags.id'))
    time = db.Column(db.DateTime, default=db.func.now())
    note = db.Column(db.String(256))

    def __repr__(self):
        return '<Entry %s (%s)>' % (self.time, self.note)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
