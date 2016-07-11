import sqlalchemy as sa
import transaction
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..UserType import UserType

class UserTypeRecordService(object):

	@classmethod
	def all(cls, request):
		with transaction.manager:
			return request.dbsession.query(UserType).order_by(sa.desc(UserType.id))

	@classmethod
	def by_id(cls, id, request=None):
		return UserType.query.get(id)

	@classmethod
	def by_name(cls, name, request):
		with transaction.manager:
			return request.dbsession.query(UserType).filter_by(name=name).first()