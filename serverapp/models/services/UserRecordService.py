import sqlalchemy as sa
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..User import User

class UserRecordService(object):
	"""docstring for UserRecordService"""
	@classmethod
	def all(cls, request):
		return request.dbsession.query(User).order_by(sa.desc(User))

	@classmethod
	def by_id(cls, id, request):
		return request.dbsession.query(User).filter_by(id=id).first()

	@classmethod
	def by_name(cls, name, request):
		return request.dbsession.query(User).filter_by(name=name).first()

	@classmethod
	def by_type_id(cls, type_id, request):
		return request.dbsession.query(User).filter_by(type_id=type_id).all()

	@classmethod
	def by_full_name(cls, full_name, request):
		return request.dbsession.query(User).filter_by(full_name=full_name).all()