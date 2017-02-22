from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class ObtainTokenAuthentication(TokenAuthentication):
	def authenticate(self,key):
		# serializer = (data=request.DATA
		# if serializer.is_valid():
			# token = Token.objects.create(user=serializer.object['user'])
		try:
			token = self.model.objects.get(key=key)
		except self.model.DoesNotExist:
			raise exceptions.AuthenticationFailed('invalid token')

		if not token.user.is_active:
			raise exceptions.AuthenticationFailed('User inactive or deleted')

		return (token.user,token)
