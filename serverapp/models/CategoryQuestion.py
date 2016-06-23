from sqlalchemy import (
	Column,
	Text,
	Integer,
	ForeignKey,
	)

from sqlalchemy.orm import relationship
from .meta import Base

class CategoryQuestion(Base):
	category_id = Column(Integer, ForeignKey('category.id'))
	question_id = Column(Integer, ForeignKey('question.id'))

	category = relationship("Category", back_populates="categoryquestions")
	question = relationship("Question", back_populates="categoryquestions")