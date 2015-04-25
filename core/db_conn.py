import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConn():
    """Database connection class to imitate Flask-SQLAlchemy syntax.
    """
    def __init__(self, db_url):

        self.engine = create_engine(db_url, echo=int(os.environ['ON_HEROKU']))
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()