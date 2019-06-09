import logging
from app import db

logger = logging.getLogger(__name__)

db.Model.metadata.reflect(db.engine)


class Tracks(db.Model):
    """Create a data model for the database to be set up for capturing songs

    """
    try:
        __table__ = db.Model.metadata.tables['tracks']
    except:
        logger.warning("'tracks' table not found")

    def __repr__(self):
        return '<Track %r>' % self.title
