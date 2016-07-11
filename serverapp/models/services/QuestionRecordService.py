import sqlalchemy as sa
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..Question import Question

class QuestionRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(Question).order_by(sa.desc(Question.id))

	@classmethod
	def by_id(cls, id, request):
		return request.dbsession.query(Question).filter_by(id=id).first()

	@classmethod
	def by_type_id(cls, type_id, request):
		return request.dbsession.query(Question).filter_by(type_id=type_id).all()

	@classmethod
	def by_question(cls, question, request):
		return request.dbsession.query(Question).filter_by(question=question).first()