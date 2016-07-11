from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import User, UserType, UserQuestion
from ..models.services.UserTypeRecordService import UserTypeRecordService
from ..models.services.CategoryTypeRecordService import CategoryTypeRecordService
from ..models.services.QuestionTypeRecordService import QuestionTypeRecordService
from ..models.services.QuestionRecordService import QuestionRecordService
from ..models.services.OptionRecordService import OptionRecordService
from ..models.services.CategoryRecordService import CategoryRecordService
from ..models.services.CategoryQuestionRecordService import CategoryQuestionRecordService

from dateutil.parser import parse

import json

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
    if request.method == 'GET':
        user_types = UserTypeRecordService.all(request)
        json_obj = list_to_json(user_types)
        print json_obj
        return json_obj

@view_config(route_name='category_types', renderer='json')
def category_types(request):
    if request.method == 'GET':
        category_types = CategoryTypeRecordService.all(request)
        json_obj = list_to_json(category_types)
        return json_obj

@view_config(route_name='question_types', renderer='json')
def question_types(request):
    if request.method == 'GET':
        question_types = QuestionTypeRecordService.all(request)
        json_obj = list_to_json(question_types)
        return json_obj

@view_config(route_name='categories', renderer='json')
def categories(request):
    if request.method == 'GET':
        categories = CategoryRecordService.all(request)
        json_obj = list_to_json(categories, 'categories')
        return json_obj

@view_config(route_name='questions', renderer='json')
def questions(request):
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

@view_config(route_name='options', renderer='json')
def options(request):
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
    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        if 'option_id' in data:
            option = OptionRecordService.by_id(int(data['option_id']), request)
            return json.dumps(option.as_dict())
        if 'question_id' in data:
            options = OptionRecordService.by_question_id(int(data['question_id']), request)
            return list_to_json(options, 'options')
        if 'correct_answer_question_id' in data:
            options = OptionRecordService.correct_answer_by_question_id(int(data['correct_answer_question_id']))
            return list_to_json(options)
        # if data['']

@view_config(route_name='answers')
def answers(request):
    if request.method == 'POST':
        data = json.loads(json.dumps(request.json))
        answers = data['answers']
        for key in answers:
            request.dbsession.add(
                UserQuestion(
                    user_id=int(data['userid']), 
                    question_id=str(data['questionid']), 
                    started_at=parse(data['starttime']), 
                    selected_option_id=answers[key],
                    )
                )
        return Response(
            status='202 Accepted',
            # content_type='application/json; charset=UTF-8'
            )


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
