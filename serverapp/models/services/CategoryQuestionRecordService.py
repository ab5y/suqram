import sqlalchemy as sa
import transaction
from .. import (
	get_engine,
	get_session_factory,
	get_tm_session,
	)

from ..CategoryQuestion import CategoryQuestion

class CategoryQuestionRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(CategoryQuestion).order_by(sa.desc(CategoryQuestion.id))

	@classmethod
	def by_id(cls, id, request=None):
		return CategoryQuestion.query.get(id);

	@classmethod
	def by_category_id(cls, category_id, request):
		return request.dbsession.query(CategoryQuestion).filter_by(category_id=category_id).all()

	@classmethod
	def by_question_id(cls, question_id, request):
		return request.dbsession.query(CategoryQuestion).filter_by(question_id=question_id).all()