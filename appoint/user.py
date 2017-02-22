"module for user creation, update and processing several operations"
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


from .models import CustomUser,UserRequests,TenantServiceRequest


class UserHandler:

	def __init__(self,username):
		try:
			self.user=CustomUser.objects.get(username=username)
		except ObjectDoesNotExist:
			self.user=None

	def getUser(self):
		try:
			user=CustomUser.objects.get(username=self.user.username)
			return	user.to_dict()
		except ObjectDoesNotExist:
		 	return "user doesnot exists"

	def getRequests(self,request_id=None):
		# try:
		# print self.user.user_id
		if request_id is not None:
			# tenant = TenantServiceRequest.objects(org_name=orgname,branch_name=branch)
			# user_requests = TenantServiceRequest.objects(services_names1__request_id=request_id)
			userRequest = TenantServiceRequest.objects.get().services_name1.filter(request_id=request_id)
			print userRequest.first().to_dict()

			return userRequest.first().to_dict()
			# return None
		else:
			user_requests= UserRequests.objects(user_id=self.user.user_id).first().requests
			# print user_requests
			if len(user_requests) > 0:
				return user_requests
			else:
				return	"No requests by you"
		# except ObjectDoesNotExist:
			# return "user doesnot exists"




			
