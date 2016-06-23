from sqlalchemy import (
	Column,
	Integer,
	Text,
	Index,
)

from sqlalchemy.orm import relationship

from .meta import Base

class QuestionType(Base):
	name = Column(Text, unique=True)

	questions = relationship("Question", back_populates="question_type")