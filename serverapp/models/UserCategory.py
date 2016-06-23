from sqlalchemy import (
	Column,
	Integer,
	ForeignKey,
	DateTime,
	)
from sqlalchemy.orm import relationship
from .meta import Base

class UserCategory(Base):
	user_id = Column(Integer, ForeignKey('user.id'))
	category_id = Column(Integer, ForeignKey('category.id'))
	submitted_on = Column(DateTime)

	user = relationship("User", back_populates="usercategories")
	category = relationship("Category", back_populates="usercategories")