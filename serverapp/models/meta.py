import datetime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import MetaData
from sqlalchemy import Column, Integer, DateTime

class Base(object):
	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()

	def as_dict(self):
		return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name is not 'password_hash' and c.name is not 'last_logged' and c.name is not 'created'}

	id = Column(Integer, primary_key=True)
	created = Column(DateTime, default=datetime.datetime.utcnow)

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.readthedocs.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata, cls=Base)
