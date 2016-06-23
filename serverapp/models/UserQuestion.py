from sqlalchemy import (
	Column,
	Integer,
	Text,
	ForeignKey,
	DateTime,
	)

from sqlalchemy.orm import relationship
from .meta import Base

class UserQuestion(Base):
	user_id = Column(Integer, ForeignKey('user.id'))
	question_id = Column(Integer, ForeignKey('question.id'))
	selected_option_id = Column(Integer, ForeignKey('option.id'))
	started_at = Column(DateTime, nullable=False)

	user = relationship("User", back_populates="userquestions")
	question = relationship("Question", back_populates="userquestions")
	selectedoption = relationship("Option", back_populates="userquestion")