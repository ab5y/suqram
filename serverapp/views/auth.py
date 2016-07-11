import json
from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
	remember,
	forget,
	)
from pyramid.view import (
	forbidden_view_config,
	view_config,
	)

from ..models.services.UserRecordService import UserRecordService

@view_config(route_name='login', renderer='json')
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
			return HTTPAccepted(headers=headers)