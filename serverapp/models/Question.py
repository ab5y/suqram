from sqlalchemy import (
	Column,
	Integer,
	Text,
	Index,
	ForeignKey,
)

from sqlalchemy.orm import relationship

from .meta import Base

class Question(Base):
	question = Column(Text)
	type_id = Column(Integer, ForeignKey('questiontype.id'))

	question_type = relationship("QuestionType", back_populates="questions")
	options = relationship("Option", back_populates="question")
	categoryquestions = relationship("CategoryQuestion", back_populates="question")
	userquestions = relationship("UserQuestion", back_populates="question")