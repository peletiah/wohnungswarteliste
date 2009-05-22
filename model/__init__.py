import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types
from sqlalchemy import ForeignKey
import datetime


def now():
    return datetime.date.today()

def init_model(bind):
    """Call me at the beginning of the application.
       'bind' is a SQLAlchemy engine or connection, as returned by
       sa.create_engine, sa.engine_from_config, or engine.connect().
    """
    global engine, Session
    engine = bind
    Session = orm.scoped_session(
        orm.sessionmaker(transactional=True, autoflush=True, bind=bind))
    orm.mapper(applicants, applicants_table,
        order_by=[applicants_table.c.lastname.desc()])

    orm.mapper(presence, presence_table,
        order_by=[presence_table.c.date.desc()])

meta = sa.MetaData()

applicants_table = sa.Table("applicants", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("firstname", types.VARCHAR(256)),
    sa.Column("lastname", types.VARCHAR(256)),
    sa.Column("birthdate", types.TIMESTAMP(timezone=False)),
    sa.Column("origin", types.VARCHAR(256)),
    sa.Column("contact", types.VARCHAR(256)),
    sa.Column("ais", types.VARCHAR(256)),
    sa.Column("comment", types.UnicodeText)
    )

class applicants(object):
    def __str(self):
        return self.title

presence_table = sa.Table("presence", meta,
    sa.Column("id", types.Integer, primary_key=True),
    sa.Column("applicants", types.Integer, ForeignKey('applicants.id')),
    sa.Column("date",types.TIMESTAMP(timezone=False),default=now()),
    )

class presence(object):
    def __str(self):
        return self.title


