from rest_framework import authentication,permissions

class DefaultMixin(object):
	authentication_classes = (
			authentication.BasicAuthentication,
			authentication.TokenAuthentication,
		)
	permissions_classes = (
		permissions.IsAuthenticated,
		)