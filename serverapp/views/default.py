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

from ..models import Category, CategoryQuestion, Follow, Option, Question, User, UserType, UserQuestion, UserCategory
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
        json_obj = list_to_json(category_types, 'category_types')
        return json_obj

@view_config(route_name='question_types', renderer='json')
def question_types(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        question_types = QuestionTypeRecordService.all(request)
        json_obj = list_to_json(question_types, 'question_types')
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
        if 'user_id' in data:
            user_to_ret = UserRecordService.by_id(int(data['user_id']), request)
            # return list_to_json([user], 'user')
            return json.loads('{"user":'+json.dumps(user_to_ret.as_dict())+'}')

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

@view_config(route_name='num_user_questions', renderer='json')
def num_user_questions(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'user_category_id' in data:
            user_questions = UserQuestionRecordService.by_user_category_id(int(data['user_category_id']), request)
            return json.loads(
                '{"num_user_questions":'+
                str(len(user_questions))+
                ', "user_category_id":'+
                data['user_category_id']+
                '}'
                )


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

    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        category_name = ''
        category_type_id = 0
        if 'category_name' in data:
            category_name = data['category_name']
        if 'category_type_id' in data:
            category_type_id = data['category_type_id']
        if len(category_name) > 0 and category_type_id > 0:
            newcategory = Category(name=category_name, type_id=category_type_id, creator_id=user.id)
            with transaction.manager:
                zope.sqlalchemy.register(request.dbsession, transaction_manager=transaction.manager)
                request.dbsession.add(newcategory)
                transaction.commit()
            responseCreated = HTTPCreated()
            responseCreated.body = "category created"
            return responseCreated

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

@view_config(route_name='categoryquestions', renderer='json')
def categoryquestions(request):
    user = request.user
    if user is None:
        raise HTTPForbidden
    if request.method == 'GET':
        data = request.params
        if 'category_id' in data:
            categoryquestions = CategoryQuestionRecordService.by_category_id(int(data['category_id']), request)
        elif 'question_id' in data:
            categoryquestions = CategoryQuestionRecordService.by_question_id(int(data['question_id']), request)
        return list_to_json(categoryquestions, 'categoryquestions')

    elif request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        if 'category_id' and 'question_id' in data:
            categoryquestion = CategoryQuestion(category_id=data['category_id'], question_id=data['question_id'])
            with transaction.manager:
                zope.sqlalchemy.register(request.dbsession, transaction_manager=transaction.manager)
                request.dbsession.add(categoryquestion)
                transaction.commit()
            responseCreated = HTTPCreated()
            responseCreated.body = "categoryquestion created"
            return responseCreated

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

    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        if 'question' and 'type_id' in data:
            question = Question(question=data['question'], type_id=data['type_id'])
            id = 0
            with transaction.manager:
                zope.sqlalchemy.register(request.dbsession, transaction_manager=transaction.manager)
                request.dbsession.add(question)
                request.dbsession.flush()
                id = question.id
                transaction.commit()
            return json.loads('{"created_question_id":'+str(id)+'}')

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
            options = OptionRecordService.correct_answer_by_question_id(int(data['correct_answer_question_id']), request)
            return list_to_json(options, 'correctoptions')
        # Return all options if no parameter specified
        options = OptionRecordService.all(request)
        return list_to_json(options)

    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        if 'options' and 'question_id' in data:
            question_id = data['question_id']
            optionsJsonArray = data['options']
            for optionJson in optionsJsonArray:
                option = Option(
                    option=optionJson['option'],
                    isCorrectAnswer=optionJson['isCorrectAnswer'],
                    question_id=question_id,
                    )
                with transaction.manager:
                    zope.sqlalchemy.register(request.dbsession, transaction_manager=transaction.manager)
                    request.dbsession.add(option)
                    transaction.commit()
            responseCreated = HTTPCreated()
            responseCreated.body = "options created"
            return responseCreated

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
                    user_id=user.id, 
                    category_id=int(data['categoryid']), 
                    started_at=parse(data['starttime'])
                    )
                request.dbsession.add(userCategory)
                request.dbsession.flush()
                user_category_id = userCategory.id
        for key in answers:
            request.dbsession.add(
                UserQuestion(
                    user_id=user.id,
                    question_id=key,
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
