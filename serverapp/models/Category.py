from sqlalchemy import (
	Column,
	Integer,
	Text,
	ForeignKey,
	)

from sqlalchemy.orm import relationship

from .meta import Base

class Category(Base):
	name = Column(Text)
	type_id = Column(Integer, ForeignKey('categorytype.id'))

	category_type = relationship("CategoryType", back_populates="categories")
	categoryquestions = relationship("CategoryQuestion", back_populates="category")
	usercategories = relationship("UserCategory", back_populates="category")