from sqlalchemy import (
	Column,
	Integer,
	Text,
	ForeignKey,
	)

from sqlalchemy.orm import relationship

from .meta import Base

class Follow(Base):
	follower_id = Column(Integer, ForeignKey('user.id'))
	followee_id = Column(Integer, ForeignKey('user.id'))

	# user = relationship("User", back_populates="follow")

	# Define relationships
	follower_user = relationship (
		'User',
		foreign_keys="Follow.follower_id",
		)
	followee_user = relationship(
		'User', 
		foreign_keys="Follow.followee_id",
		)