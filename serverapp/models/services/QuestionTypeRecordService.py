import sqlalchemy as sa
import transaction
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..QuestionType import QuestionType

class QuestionTypeRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(QuestionType).order_by(sa.desc(QuestionType.id))

	@classmethod
	def by_id(cls, id, request=None):
		return QuestionType.query.get(id)

	@classmethod
	def by_name(cls, name, request):
		return request.dbsession.query(QuestionType).filter_by(name=name).first()