import sqlalchemy as sa
from ..Category import Category

class CategoryRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(Category).order_by(sa.desc(Category.id))

	@classmethod
	def by_id(cls, id, request=None):
		return Category.query.get(id)

	@classmethod
	def by_name(cls, name, request):
		return request.dbsession.query(Category).filter_by(name=name).first()

	@classmethod
	def by_type_id(cls, type_id, request):
		return request.dbsession.query(Category).filter_by(type_id=type_id).all()

	@classmethod
	def by_creator_id(cls, creator_id, request):
		return request.dbsession.query(Category).filter_by(creator_id=creator_id).all()