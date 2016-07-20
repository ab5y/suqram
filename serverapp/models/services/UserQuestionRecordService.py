import sqlalchemy as sa
from ..UserQuestion import UserQuestion

class UserQuestionRecordService(object):

	@classmethod
	def all(cls, request):
		return request.dbsession.query(UserQuestion).order_by(sa.desc(UserQuestion.id))

	@classmethod
	def by_id(cls, id, request):
		return request.dbsession.query(UserQuestion).get(id)

	@classmethod
	def by_user_id(cls, user_id, request):
		return request.dbsession.query(UserQuestion).filter_by(user_id=user_id).all()

	@classmethod
	def by_question_id(cls, question_id, request):
		return request.dbsession.query(UserQuestion).filter_by(question_id=question_id).all()

	@classmethod
	def by_user_category_id(cls, user_category_id, request):
		return request.dbsession.query(UserQuestion).filter_by(user_category_id=user_category_id).all()

	@classmethod
	def by_selected_option_id(cls, selected_option_id, request):
		return request.dbsession.query(UserQuestion).filter_by(selected_option_id=selected_option_id).all()