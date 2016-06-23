from sqlalchemy import (
	Column,
	Integer,
	Text,
	Index,
	Boolean,
	ForeignKey,
)

from sqlalchemy.orm import relationship

from .meta import Base

class Option(Base):
	option = Column(Text)
	isCorrectAnswer = Column(Boolean(create_constraint=False), nullable=False)
	question_id = Column(Integer, ForeignKey('question.id'))

	question = relationship("Question", back_populates="options")
	userquestion = relationship("UserQuestion", back_populates="selectedoption")