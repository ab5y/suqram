import json

from dateutil.parser import parse

from pyramid.httpexceptions import (
    HTTPCreated,
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    HTTPOk,
    )
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
import transaction
import zope.sqlalchemy

from ..models import Follow, User, UserType, UserQuestion, UserCategory
from ..models.services.CategoryQuestionRecordService import CategoryQuestionRecordService
from ..models.services.CategoryRecordService import CategoryRecordService
from ..models.services.CategoryTypeRecordService import CategoryTypeRecordService
from ..models.services.FollowRecordService import FollowRecordService
from ..models.services.OptionRecordService import OptionRecordService
from ..models.services.QuestionRecordService import QuestionRecordService
from ..models.services.QuestionTypeRecordService import QuestionTypeRecordService
from ..models.services.UserCategoryRecordService import UserCategoryRecordService
from ..models.services.UserQuestionRecordService import UserQuestionRecordService
from ..models.services.UserRecordService import UserRecordService
from ..models.services.UserTypeRecordService import UserTypeRecordService


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(User)
        one = query.filter(User.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'serverapp'}

@view_config(route_name='hello', renderer='string')
def hello(request):
    if request.method == 'POST':
        print 'ooh it tickles!'
    return 'Hello World!'

@view_config(route_name='user_types', renderer='json')
def user_types(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        user_types = UserTypeRecordService.all(request)
        json_obj = list_to_json(user_types, 'user_types')
        print json_obj
        return json_obj

@view_config(route_name='category_types', renderer='json')
def category_types(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        category_types = CategoryTypeRecordService.all(request)
        json_obj = list_to_json(category_types)
        return json_obj

@view_config(route_name='question_types', renderer='json')
def question_types(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        question_types = QuestionTypeRecordService.all(request)
        json_obj = list_to_json(question_types)
        return json_obj

@view_config(route_name='users', renderer='json')
def users(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'user_type_id' in data:
            usertype = UserTypeRecordService.by_id(int(data['user_type_id']), request)
            users = UserRecordService.by_type_id(int(data['user_type_id']), request)
            return list_to_json(users, usertype.name)


@view_config(route_name="followees", renderer='json')
def followees(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        followees = FollowRecordService.by_follower_id(user.id, request)
        return list_to_json(followees, 'followees')
    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        if 'followee_id' in data:
            follow = Follow(follower_id=user.id, followee_id=int(data['followee_id']))
            
            with transaction.manager:
                zope.sqlalchemy.register(request.dbsession, transaction_manager=transaction.manager)
                request.dbsession.add(follow)
            
            responseCreated = HTTPCreated()
            responseCreated.body = "followed"
            return responseCreated
    
    if request.method == 'DELETE':
        data = json.loads(json.dumps(request.json))
        if 'followee_id' in data:
            with transaction.manager:
                zope.sqlalchemy.register(request.dbsession, transaction_manager=transaction.manager)
                request.dbsession.query(Follow).filter_by(followee_id=int(data['followee_id'])).filter_by(follower_id=user.id).delete()
                transaction.commit()
            responseDeleted = HTTPOk()
            responseDeleted.body = "unfollowed"
            return responseDeleted


@view_config(route_name='num_categories', renderer='json')
def num_categories(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'creator_id' in data:
            categories = CategoryRecordService.by_creator_id(int(data['creator_id']), request)
            return json.loads('{"num_categories":'+str(len(categories))+'}')

@view_config(route_name='categories', renderer='json')
def categories(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'creator_id' in data:
            categories = CategoryRecordService.by_creator_id(int(data['creator_id']), request)
            return list_to_json(categories, 'categories')
        categories = CategoryRecordService.by_creator_id(user.id, request)
        json_obj = list_to_json(categories, 'categories')
        return json_obj

@view_config(route_name='usercategories', renderer='json')
def usercategories(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'category_id' in data:
            usercategories = UserCategoryRecordService.by_category_id(int(data['category_id']), request)
            return list_to_json(usercategories, 'usercategories')

@view_config(route_name='userquestions', renderer='json')
def userquestions(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'user_category_id' in data:
            userquestions = UserQuestionRecordService.by_user_category_id(int(data['user_category_id']), request)
            return list_to_json(userquestions, 'userquestions')

@view_config(route_name='questions', renderer='json')
def questions(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'question_id' in data:
            question = QuestionRecordService.by_id(int(data['question_id']), request)
            return json.dumps(question.as_dict())
        if 'question_type_id' in data:
            questions = QuestionRecordService.by_type_id(int(data['question_type_id']), request)
            return list_to_json(questions)
        if 'category_id' in data:
            category_questions = CategoryQuestionRecordService.by_category_id(int(data['category_id']), request)
            questions = []
            for category_question in category_questions:
                questions.append(QuestionRecordService.by_id(category_question.question_id, request))
            return list_to_json(questions, 'questions')
        # If no parameters, return all questions
        questions = QuestionRecordService.all(request)
        json_obj = list_to_json(questions, 'questions')
        return json_obj

@view_config(route_name='options', renderer='json')
def options(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'option_id' in data:
            option = OptionRecordService.by_id(int(data['option_id']), request)
            return json.dumps(option.as_dict())
        if 'question_id' in data:
            options = OptionRecordService.by_question_id(int(data['question_id']), request)
            return list_to_json(options, 'options')
        if 'correct_answer_question_id' in data:
            options = OptionRecordService.correct_answer_by_question_id(int(data['correct_answer_question_id']))
            return list_to_json(options)
        # Return all options if no parameter specified
        options = OptionRecordService.all(request)
        return list_to_json(options)

@view_config(route_name='answers', renderer='json')
def answers(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        answers = data['answers']
        user_category_id = None
        questions = 0
        correctanswers = 0
        if 'categoryid' in data:
            if int(data['categoryid']) > 0:
                userCategory = UserCategory(
                    user_id=int(data['userid']), 
                    category_id=int(data['categoryid']), 
                    started_at=parse(data['starttime'])
                    )
                request.dbsession.add(userCategory)
                request.dbsession.flush()
                user_category_id = userCategory.id
        for key in answers:
            request.dbsession.add(
                UserQuestion(
                    user_id=int(data['userid']), 
                    question_id=int(data['questionid']), 
                    user_category_id=user_category_id, 
                    selected_option_id=answers[key],
                    )
                )
            questions = questions + 1
            option = OptionRecordService.by_id(int(answers[key]), request)
            if option.isCorrectAnswer:
                correctanswers = correctanswers + 1
        jsonResult = json.loads('{"attempted":'+str(questions)+',"correct":'+str(correctanswers)+'}')
        return jsonResult


def list_to_json(list, name=None):
    dicts = []
    for item in list:
        dicts.append(item.as_dict())
    if name == None:
        jsonobj = json.dumps(dicts);
    else:
        jsonobj = json.dumps("{"+'"'+name+'"'+":"+str(dicts)+"}")
    return jsonobj


get = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_serverapp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""