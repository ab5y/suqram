from sqlalchemy import (
	Text,
	Integer,
	Column,
	)

from sqlalchemy.orm import relationship

from .meta import Base

class CategoryType(Base):
	name = Column(Text, unique=True)

	categories = relationship("Category", back_populates="category_type")