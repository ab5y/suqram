from default import list_to_json
import json
from pyramid.httpexceptions import (
	HTTPBadRequest,
	HTTPCreated,
	HTTPOk,
	)
from pyramid.security import (
	remember,
	forget,
	)
from pyramid.view import (
	forbidden_view_config,
	view_config,
	)

from ..models import User
from ..models.services.UserRecordService import UserRecordService
from ..models.services.UserTypeRecordService import UserTypeRecordService

@view_config(route_name='login')
def login(request):
	if request.method == 'POST':
		login = ''
		password = ''
		message = ''
		print "Request dot json looks like ", request.json
		data = json.loads(json.dumps(request.json))
		if 'login' in data:
			login = data['login']
		if 'password' in data:
			password = data['password']
		user = UserRecordService.by_name(login, request)
		if user is not None and user.check_password(password):
			headers = remember(request, user.id)
			okResponse = HTTPOk(headers=headers)
			okResponse.body = "Login success"
			return okResponse
		else:
			badRequestResponse = HTTPBadRequest()
			badRequestResponse.body = 'Login fail. User name or password incorrect.'
			return badRequestResponse

@view_config(route_name='logout')
def logout(request):
	headers = forget(request)
	return HTTPOk(headers=headers)

@view_config(route_name='register', renderer='json')
def register(request):
	if request.method == 'GET':
		userTypes = UserTypeRecordService.all(request)
		return list_to_json(userTypes, 'user_types')
	if request.method == 'POST':
		data = json.loads(json.dumps(request.json))
		login = ''
		password = ''
		confirmpassword = ''
		fullname = ''
		type_id = 0
		badRequestResponse = HTTPBadRequest()
		if 'login' in data: login = str(data['login'])
		if 'password' in data: password = str(data['password'])
		if 'confirmpassword' in data: confirmpassword = str(data['confirmpassword'])
		if 'fullname' in data: fullname = str(data['fullname'])
		if 'typeid' in data: type_id = int(data['typeid'])

		if len(login) < 3:
			badRequestResponse.body = 'Login needs to be 3 or more characters.'
			return badRequestResponse
		if len(password) < 5:
			badRequestResponse.body = 'Password needs to be 5 or more characters.'
			return badRequestResponse
		if type_id < 1: 
			badRequestResponse.body = 'Valid Type needs to be selected.'
			return badRequestResponse
		
		user = UserRecordService.by_name(login, request)
		if user is None:
			if confirmpassword == password:
				user = User(name=login, full_name=fullname, type_id=int(type_id))
				user.set_password(password)
				request.dbsession.add(user)
				responseCreated = HTTPCreated()
				responseCreated.body = "registered"
				return responseCreated
			else:
				badRequestResponse.body = 'Passwords don\'t match.'
				return badRequestResponse
		else:
			badRequestResponse.body = 'Login name already exists. Please use a different name.'
			return badRequestResponse