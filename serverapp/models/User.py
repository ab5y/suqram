import bcrypt
from sqlalchemy import (
	Column,
	DateTime,
	ForeignKey,
	Index,
	Integer,
	Text,
)

from sqlalchemy.orm import relationship

from .meta import Base

class User(Base):
	name = Column(Text, unique=True, nullable=False)
	full_name = Column(Text)
	password_hash = Column(Text, nullable=False)
	last_logged = Column(DateTime)
	type_id = Column(Integer, ForeignKey('usertype.id'))

	user_type = relationship("UserType", back_populates="users")
	userquestions = relationship("UserQuestion", back_populates="user")
	usercategories = relationship("UserCategory", back_populates="user")

	def set_password(self, pw):
		pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
		self.password_hash = pwhash

	def check_password(self, pw):
		if self.password_hash is not None:
			expected_hash = self.password_hash.encode('utf8')
			actual_hash = bcrypt.hashpw(pw.encode('utf8'), expected_hash)
			return expected_hash == actual_hash
		return False