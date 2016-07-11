from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models.services import UserRecordService

class AuthenticationPolicy(AuthTktAuthenticationPolicy):
	def authenticated_userid(self, request):
		user = request.user
		if user is not None:
			return user.id

def get_user(request):
	user_id = request.unauthenticated_userid
	if user_id is not None:
		user = UserRecordService.by_id(user_id, request)
		return user

def includeme(config):
	settings = config.get_settings()
	authn_policy = AuthenticationPolicy(
		settings['auth.secret'],
		hashalg='sha512',
		)
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(ACLAuthorizationPolicy())
	config.add_request_method(get_user, 'user', reify=True)