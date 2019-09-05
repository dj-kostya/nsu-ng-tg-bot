import argparse

import sqlalchemy.exc

from app_body.BD import db


def create_groups():
    for perm in ['19137', '19144', 'Преподаватели']:
        find_ = db.Groups.query.filter_by(name=perm).first()
        if not find_:
            i = db.Groups.create(name=perm)


def create_permission():
    for perm in ['add', 'del', 'upd', 'run']:
        find_ = db.Permissions.query.filter_by(name=perm).first()
        if not find_:
            i = db.Permissions.create(name=perm)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", action="store_true", dest='drop')
    parser.add_argument("--drop-data", action="store_true", dest='drop_data')
    args = parser.parse_args()
    if args.drop:

        db.drop_all()
        db.create_all()
    db.set_session()
    if args.drop_data:
        db.RunHistory.query.delete()
        db.commit()
    create_groups()
    create_permission()
    db.commit()
