#!/usr/bin/env python
# coding: utf-8

"""
Script to empty and recreate the database, for demo purposes for eg.
"""
from core import Base

def reset_database(db):

    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    db.session.commit()

    print('Database reset done.')
    return

if __name__ == '__main__':

    from core import db
    reset_database(db)