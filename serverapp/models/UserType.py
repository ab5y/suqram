from sqlalchemy import (
	Column,
	Integer,
	Text,
	Index
)

from sqlalchemy.orm import relationship

from .meta import Base

class UserType(Base):
	name = Column(Text, unique=True)

	users = relationship("User", back_populates="user_type")