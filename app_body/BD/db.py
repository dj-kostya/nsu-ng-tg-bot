import os
from datetime import datetime
from app_body import debug, Contants
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


class Permissions(BaseModel):
    __tablename__ = 'Permissions'
    __repr_attrs__ = ['name']

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)


role_permissions = sa.Table('Role_permissions', Base.metadata,
                            sa.Column('id_role', sa.Integer, sa.ForeignKey('Roles.id'), primary_key=True),
                            sa.Column('id_permission', sa.Integer, sa.ForeignKey('Permissions.id'), primary_key=True)
                            )


class Roles(BaseModel):
    __tablename__ = 'Roles'
    __repr_attrs__ = ['name']

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    permission = sa.orm.relationship('Permissions', secondary=role_permissions)


class Groups(BaseModel):
    __tablename__ = 'Groups'
    __repr_attrs__ = ['name']
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)


class Users(BaseModel):
    __tablename__ = 'Users'
    __repr_attrs__ = ['tg_username', 'tg_id']

    id = sa.Column(sa.Integer, primary_key=True)
    tg_username = sa.Column(sa.String)
    tg_id = sa.Column(sa.Integer)
    sh_dt = sa.Column(sa.DateTime, default=datetime.now())
    id_role = sa.Column(sa.Integer, sa.ForeignKey('Roles.id'))
    id_group = sa.Column(sa.Integer, sa.ForeignKey('Groups.id'))


class RunHistory(BaseModel):
    __tablename__ = 'RunHistory'
    __repr_attrs__ = ['id', 'id_user']
    id = sa.Column(sa.Integer, primary_key=True)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('Users.id'))
    total = sa.Column(sa.Integer)
    sh_dt = sa.Column(sa.DateTime, default=datetime.now())


abs_path = os.path.abspath(os.path.dirname(__file__))
if debug:
    engine = sa.create_engine('sqlite:///' + os.path.join(abs_path, 'sqlite/app_body.db'), echo=True)
else:
    engine = sa.create_engine(Contants.HEROKU_URL, echo=True)
session = scoped_session(sessionmaker(bind=engine))


def commit():
    global session
    session.commit()


def get_list():
    global Base
    return Base.metadata.tables.keys()


def drop_all():
    global Base, engine
    Base.metadata.drop_all(engine)


def create_all():
    global Base, engine
    Base.metadata.create_all(engine)


def set_session():
    BaseModel.set_session(session)
