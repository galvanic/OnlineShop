#!/usr/bin/env python
# coding: utf-8

import os
from webapp import app, db
from db_reset import reset_database

if bool(int(os.environ['ON_HEROKU'])):
    @app.before_first_request
    def setup():
        reset_database(db)
        return

if __name__ == '__main__':

    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)