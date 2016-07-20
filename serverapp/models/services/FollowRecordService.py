import sqlalchemy as sa
from ..Follow import Follow

class FollowRecordService(object):
	"""docstring for FollowRecordService"""

	@classmethod
	def all(cls, request):
		return request.dbsession.query(Follow).order_by(sa.desc(Follow.id))

	@classmethod
	def by_id(cls, id, request):
		return request.dbsession.query(Follow).get(id);

	@classmethod
	def by_followee_id(cls, followee_id, request):
		"""Get user's followers list"""
		return request.dbsession.query(Follow).filter_by(followee_id=followee_id).all()

	@classmethod
	def by_follower_id(cls, follower_id, request):
		"""Get user's followed list"""
		return request.dbsession.query(Follow).filter_by(follower_id=follower_id).all()