import sqlalchemy as sa
from ..UserCategory import UserCategory

class UserCategoryRecordService(object):
	
	@classmethod
	def all(cls, request):
		return request.dbsession.query(UserCategory).order_by(sa.desc(UserCategory.id))

	@classmethod
	def by_id(cls, id, request):
		return request.dbsession.query(UserCategory).get(id)

	@classmethod
	def by_user_id(cls, user_id, request):
		return request.dbsession.query(UserCategory).filter_by(user_id=user_id).all()

	@classmethod
	def by_category_id(cls, category_id, request):
		return request.dbsession.query(UserCategory).filter_by(category_id=category_id).all()