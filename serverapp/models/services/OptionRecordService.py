import sqlalchemy as sa
import transaction
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..Option import Option

class OptionRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(Option).order_by(sa.desc(Option.id))

	@classmethod
	def by_id(cls, id, request):
		return request.dbsession.query(Option).get(id)

	@classmethod
	def by_question_id(cls, question_id, request):
		return request.dbsession.query(Option).filter_by(question_id=question_id).all()

	@classmethod
	def by_option(cls, option, request):
		return request.dbsession.query(Option).filter_by(option=option).all()

	@classmethod
	def all_correct_options(cls, request):
		return request.dbsession.query(Option).filter_by(isCorrectAnswer=True).all()

	@classmethod
	def all_incorrect_answers(cls, request):
		return request.dbsession.query(Option).filter_by(isCorrectAnswer=False).all()

	@classmethod
	def correct_answer_by_question_id(cls, question_id, request):
		return request.dbsession.query(Option).\
				filter(Option.question_id==question_id).\
				filter(Option.isCorrectAnswer==True).\
				all()