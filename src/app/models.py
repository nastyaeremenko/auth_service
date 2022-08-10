import uuid
from datetime import datetime

from sqlalchemy import exc, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.db import db
from app.excepions import ObjectExists

profile_role_table = db.Table(
    'profile_role', db.Model.metadata,
    db.Column('id', UUID(as_uuid=True), primary_key=True,
              default=uuid.uuid4, unique=True, nullable=False),
    db.Column('profile_id', UUID(as_uuid=True),
              db.ForeignKey('profile.id'), nullable=False),
    db.Column('role_id', UUID(as_uuid=True),
              db.ForeignKey('role.id'), nullable=False)
)

role_permission_table = db.Table(
    'role_permission', db.Model.metadata,
    db.Column('id', UUID(as_uuid=True), primary_key=True,
              default=uuid.uuid4, unique=True, nullable=False),
    db.Column('role_id', UUID(as_uuid=True),
              db.ForeignKey('role.id'), nullable=False),
    db.Column('permission_id', UUID(as_uuid=True),
              db.ForeignKey('permission.id'), nullable=False)
)


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    session = db.relationship('Session', backref='profile', lazy='select',
                              cascade='all, delete')
    role = db.relationship('Role', backref='profile', cascade='all, delete',
                           secondary=profile_role_table)
    user = db.relationship('User', backref='profile', lazy='select',
                           cascade='all, delete', uselist=False)
    social_auth = db.relationship('SocialAuth', backref='profile',
                                  lazy='select', cascade='all, delete')

    def __repr__(self):
        return f'<Profile {self.id}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise ObjectExists('Email is already exists.')
        return self


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profile.id'),
                           nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise ObjectExists('Login is already exists.')
        return self

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


def create_partition(target, connection, **kw) -> None:
    """ creating partition by session """
    connection.execute(
        """SELECT partman.create_parent('public.session_new', 'last_active_date', 'native', 'daily');"""
    )


class Session(db.Model):
    __tablename__ = 'session'

    __table_args__ = (
        UniqueConstraint('id', 'last_active_date',
                         name='unique_id_last_active_date'),
        {
            'postgresql_partition_by': 'RANGE (last_active_date)',
            'listeners': [('after_create', create_partition)],
        }
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, nullable=False)
    profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profile.id'),
                           nullable=False)
    agent = db.Column(db.String(255), nullable=False)
    auth_date = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_active_date = db.Column(db.DateTime, nullable=False,
                                 default=datetime.utcnow,
                                 onupdate=datetime.utcnow)
    login_type = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Session {self.id}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permission = db.relationship('Permission', backref='role',
                                 cascade='all, delete',
                                 secondary=role_permission_table)

    def __repr__(self):
        return f'<Role {self.slug}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise ObjectExists('Role with this slug is already exists.')
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Permission {self.slug}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise ObjectExists('Permission with this slug is already exists.')
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class SocialAuth(db.Model):
    __tablename__ = 'social_auth'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    social_name = db.Column(db.String(120), nullable=False)
    social_user_id = db.Column(db.String(255), nullable=False)
    profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('profile.id'),
                           nullable=False)
    __table_args__ = (db.UniqueConstraint('social_name', 'social_user_id',
                                          name='_social_user'),)

    def __repr__(self):
        return f'<Social auth {self.social_name} {self.social_user_id}>'

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError:
            raise ObjectExists('This social user is already exists.')
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
