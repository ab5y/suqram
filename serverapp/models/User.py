from sqlalchemy import (
	Column,
	Integer,
	Text,
	Index,
	ForeignKey,
)

from sqlalchemy.orm import relationship

from .meta import Base

class User(Base):
	name = Column(Text, unique=True)
	full_name = Column(Text)
	type_id = Column(Integer, ForeignKey('usertype.id'))

	user_type = relationship("UserType", back_populates="users")
	userquestions = relationship("UserQuestion", back_populates="user")
	usercategories = relationship("UserCategory", back_populates="user")