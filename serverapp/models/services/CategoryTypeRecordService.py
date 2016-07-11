import sqlalchemy as sa
import transaction
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..CategoryType import CategoryType

class CategoryTypeRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(CategoryType).order_by(sa.desc(CategoryType.id))

	@classmethod
	def by_id(cls, id, request=None):
		return CategoryType.query.get(id)

	@classmethod
	def by_name(cls, name, request):
		return request.dbsession.query(CategoryType).filter_by(name=name).first()