#from .models import UserSignUp
#from .serializers import UserSignUpSerializer

from django.http import Http404,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
# from rest_framework import serializers
from django.core import serializers


class UserList(APIView):
	"""docstring for UserList"APIViewf __init__(self, arg):
		super(UserList,APIView.__init__()
		self.arg = arg
	"""
	def get(self, request, format=None):
		users = UserSignUp.objects.all()
		serialized_users = UserSignUpSerializer(users, many=True)
		#HttpResponse = 
		return Response({'hello':'Rahul'})

class UserDetail(APIView):
	
	def get_object(self,pk):
		try:
			return UserSignUp.object.get(pk=pk)
		except Game.DoesNotExist:
			raise Http404


	def get(self,request,pk,format=None):
		users = self.get_object(pk)
		serialized_users = UserSignUpSerializer(users)
		return Response(serialized_users.data)

from .models import TenantList
import json
from helper import Convert
class TenantView(APIView):
	permission_classes = [permissions.AllowAny]

	def get(self,request,name,branch):
		tenant = name
		print  "The tenant is %s"  %tenant
		tenant_details= TenantList.objects(org_name=tenant,branch_name=branch)
		res = [Convert.to_d1(x.to_dict())  for x in tenant_details]
		return HttpResponse(json.dumps({"tenant":res}))
		

from .helper import Convert, Nonsense, TimerUpdate,Tenant		
from .models import TenantServiceRequest
class TenantRequestQueue(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,name,branch):
		req_cheque = TenantServiceRequest.objects.get(org_name=name,branch_name=branch)
		# .services_name1.filter(service_name="cheque")
		x=req_cheque.services_name1.filter(service_name="cheque",processed="NO")
		print "length"
		print len(x)

		# req_cheque = TenantServiceRequest.objects(org_name=name,branch_name=branch,services_name1__service_name="cheque")#,services_name1__processed="NO")
		# temp = []
		# for  x in req_cheque:
		# 	temp.append(ConToDict.convert(x))
		# reqs = ConToDict.convert(req_cheque)
		reqs = [ Convert.to_d1(x.to_dict())for x in req_cheque.services_name1.filter(processed="NO")]
		counters =4
		temp = [[] for x in range(0,counters)]
			# temp.append()
		s = Tenant(name,branch)
		counters=s.getCounters()
		
		# req2=[ d.update({'service_time':180,'process':'No'}) for d in reqs]

		# print temp
		#pull no. of counter and thier names 


		# sed = s.sched(counters,name,branch)
		# s = TimerUpdate(sed)
		# s.updateTime()
		sed=s.getRequests()
		dict1 = {'c1':'c1','c2':'c2','c3':'c3'}
		for x in reqs:
			index = reqs.index(x) + 1
			if index % 2 == 0:
				# print x
				temp[1].append(x)
			elif index % 3 == 0:
				temp[2].append(x)
			else:
				temp[0].append(x)
		dict1['c1']=temp[0]
		dict1['c2']=temp[1]
		dict1['c3']=temp[2]		


		return HttpResponse(json.dumps({"counters":sed,"counters_count":None}))


class TenantCounterRequest(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,orgname,branch,counter):
		
		# req_cheque = TenantServiceRequest.objects(org_name=orgname,branch_name=branch,services_name1__service_name="cheque",services_name1__counter=counter)
		req_cheque = TenantServiceRequest.objects.get(org_name=orgname,branch_name=branch).services_name1.filter(processed="NO",counter=counter)
		print req_cheque
		reqs = [(x.to_dict())for x in req_cheque]
		s = Tenant(orgname,branch)
		counters=s.getCounters()
		sed=s.getRequests()
		return HttpResponse(json.dumps({"counters":reqs,"counters_count":counters}))

# class CreateContactView(GenericView):	
# 	pass

# class TenantView(APIView):
# 	def get(self,request,name):
# 		try:
# 			tennant= name
# 			return HttpResponse(json.dumps({"tenant":tennant})

import json
class TenantRequestComplete(APIView):
	permission_classes = [permissions.AllowAny]

	"""docstring for TenantRequestComplete : after completing the  User request it will updates the database"""

	
	def post(self,request,name,branch):

		user_request= json.loads(request.body)
		print user_request
		# proccess_cheque=TenantServiceRequest.objects(org_name=name,services_name1__S__service_name="cheque",
		# 	services_name1__S__processed="NO",
		# 	services_name1__S__branch_name=str(user_request['branch_name']),		
		# 	services_name1__S__full_name= str(user_request['full_name']),
		# 	services_name1__S__email=str(user_request['email']))
		proccess_cheque = TenantServiceRequest.objects(org_name=str(user_request['bank_name']))
		print " the Objects are  %s" %(proccess_cheque)
		# print proccess_cheque[0].services_name1
		proccess_chequew = TenantServiceRequest.objects.get(org_name=name).services_name1.filter(user_id=str(user_request['user_id']))   
		# 		branch_name=str(user_request['branch_name']),
		#  			full_name= str(user_request['full_name']),
		#  			email=str(user_request['email']),
		#  			user_id=str(user_request['user_id']),
		#  			processed="NO"				
		# )
				# ).update(set__services_name1__S__processed="YES")
		# print proccess_chequew[0]
		# proccess_chequew[0].update_one(set_processed="YES")
		tent_update = TenantServiceRequest._get_collection()
		bbb = tent_update.update({"services_name1.user_id":str(user_request['user_id'])},{'$set':{'services_name1.$.processed':"YES"}})
		# proccess_chequew1 = TenantServiceRequest.objects(__raw__())
		print bbb
		# temp =  TenantServiceRequest.objects.get(org_name=name).services_name1.filter(branch_name=str(user_request['branch_name']),user_id=str(user_request['user_id'])).update_one(set__processed__S="YES")
		# temp[0].update_one(set__processed="YES")
		# print 

		return HttpResponse(json.dumps({"message":"success","status":1}))

from .models import TenantList
class TenantBranchList(APIView):
	permission_classes = [permissions.AllowAny]

	def get(self,request,orgname):
		branches = TenantList.objects(org_name=orgname)
		branch_list = [x.branch_name for x in branches]
		dict_branch = {"branches":branch_list} 
		return HttpResponse(json.dumps(dict_branch))

class TenantServicesList(APIView):
	permission_classes = [permissions.AllowAny]

	def get(self,request,branch,orgname):
		services_list = TenantList.objects(org_name=orgname,branch_name=branch)
		services_list = services_list[0].services_list
		return HttpResponse(json.dumps({"services":services_list}))


class TenantAddServices(APIView):
	def get(self,request,branch,orgname,servicename):
		services_list = TenantList.objects(org_name=orgname,branch_name=branch).update(
						add_to_set__services_list=servicename)
		ten = TenantServiceRequest.objects(org_name=orgname,branch_name=branch)
		ten[0].update(add_to_set__services_list=servicename)
		ten = TenantServiceRequest.objects(org_name=orgname,branch_name=branch)
		services_list1 = ten[0].services_list
		print services_list1
		services_list = TenantList.objects(org_name=orgname,branch_name=branch)
		services_list = services_list[0].services_list
		return HttpResponse(json.dumps({"services":services_list}))       

#from rest_framework.views import CreateAPIView
from .serializers import CustomUserSerializer
from .models import CustomUser,UserRequest
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView
	)
import uuid
class UserRegister(APIView):
	# def post(self,request):
	# 	try:
	permission_classes = [permissions.AllowAny]

	def post(self,request,format=None):
		user_register_data=json.loads(request.body)
		s = str(uuid.uuid4()).decode('utf-8')
		
		user_register_data.update({'user_id':s})
		print user_register_data
		user_req = CustomUserSerializer(data=user_register_data)
		if user_req.is_valid():
		#	print type(user_req)
			#user_req.update({'user_id':str(uuid.uuid4())})
			user_req.save()
			user_request=UserRequests(user_id=s)
			user_request.save()
			return HttpResponse(json.dumps({"Message":"success"}))
		else:
			queryset = CustomUser.objects.all()
			return HttpResponse(json.dumps({"message ":'Sorry not created'}))
		
		#req = [Convert.to_d1(x.to_dict())for x in queryset]
		

class UserList(ListAPIView):
	#ss=get_serializer_class(CustomUser)
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer

# class StaffN(ListAPIView):
# 	queyset = StaffNew.objects(bank_id=)

from .serializers import UserAuthenticate	
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
class ObtainToken(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self,request):
		serializer = UserAuthenticate(data=request.data)
		# print "yeah"
		if serializer.is_valid():
			try:
				username = serializer.initial_data['username']
				user = CustomUser.objects.get(username=username,password=serializer.initial_data['password'])
				token = Token.objects.get(user=user)
				return HttpResponse(json.dumps({"token1":token.key}))
				
			except Exception:
				try:
					customer = CustomUser.objects.get(username=username)
					if customer is not None:
						return HttpResponse(json.dumps({"Message":"Password or Username incorrect"}))
					else:
						return HttpResponse(json.dumps({"Message":"Password or Username incorrect"}))
				except Exception:
					return HttpResponse(json.dumps({"status":"0","Message":"User Doesnot Exist"}))
		else:
			return HttpResponse(json.dumps({"status":"0",'Message':'Something went wrong in username or password'}))
		

from .serializers import Staff
from .models import StaffNew
from django.forms.models import model_to_dict
class StaffUser(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self,request):
		try:
			datd=request.data
			serializer = Staff(data=request.data)
			if serializer.is_valid():
				print "valid"
				bank_id=TenantList.objects(org_name=datd['org_name'],branch_name=datd['branch_name']).first().tenant_id
				# print ow valid	
				print bank_id			
				staff= StaffNew(username=datd['username'],
					password=datd['password'],
					email=datd['email'],
					user_id=str(uuid.uuid4()).decode('utf-8'),
					bank_id=bank_id)
				staff.save()
				# print staff.username
				# staff.save()
				return HttpResponse(json.dumps({'message':'successfully created1'}))	
			else:
				return HttpResponse(json.dumps({'message':'Something went @@('}))
		except Exception:
			return HttpResponse(json.dumps({"message":"something went wrong"}))
		# return HttpResponse(json.dumps({"message":Exception}))
	def get(self,request,branch,orgname):
		# try:
		bank_id=TenantList.objects(org_name=orgname,branch_name=branch).first().tenant_id
		# staff = StaffNew.objects.filter(bank_id=bank_id)
		staff = StaffNew.objects.filter(bank_id=bank_id)
		new=[]
		for x in staff:
			new.append(model_to_dict(x))
		# print staff
		# for each x in 
		# sda=model_to_dict(staff)
		# data = serializers.serialize('json',StaffNew.objects.get(bank_id=bank_id))

		return HttpResponse(json.dumps({'staff':new}))

		# except Exception:
		# return HttpResponse(json.dumps({"message":"something went wrong"})) 



# class AllotCounter(APIView):
# 	def post(self,request):
# 		try:
			
class AddService(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,orgname,branch,servicename):
		try:
			services1_list = TenantList.objects(org_name=orgname,branch_name=branch).update(
				add_to_set__services_list=servicename)
			tenant = TenantServiceRequest.objects(org_name=orgname,branch_name=branch)
			tenant = tenant.first()
			tenant.update(add_to_set__services_list=servicename)
		except Exception:
			return HttpResponse(json.dumps({"message":"something went wrong"}))
		return HttpResponse(json.dumps({"message":"successfully added","status":1}))


class ServicesList(APIView):
	permission_classes =[permissions.AllowAny]
	def get(self,request,orgname,branch):
		try:

			tenant = TenantServiceRequest.objects(org_name=orgname,branch_name=branch)
			tenant = tenant.first()
			services = tenant.services_list
		except Exception:
			return HttpResponse(json.dumps({"message":"something went wrong","status":1}))
		return HttpResponse(json.dumps({"services":services,"status":1}))

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from .helper import Tenant
from .models import ServiceCounter,Counter
from .serializers import CounterSerializer
class Counters(APIView):
	permission_classes = [permissions.AllowAny]
	def post(self,request,orgname,branch):
		# try:
		counterSerializer = CounterSerializer(data=request.data)
		if counterSerializer.is_valid():
			staff = StaffNew.objects.filter(username=request.data['staff_name'])
			if staff is not None:
				counter = Counter(counter_name=request.data['counter_name'],services_list=[request.data['service']],staff=request.data['staff_name'])
				tenant = TenantList.objects(org_name=orgname,branch_name=branch).first().tenant_id				
				counter = ServiceCounter(bank_id=tenant,allot=[counter])
				counter.save()
				staff = StaffNew.objects.filter(username=request.data['staff_name'])
				staff.update(counter=request.data['counter_name'])

				print "created"
				return HttpResponse(json.dumps({"message":"successfully created","status":1}))

			else:
				return HttpResponse(json.dumps({"Message":"unable to create please try again","status":0}))
		else:
			return HttpResponse(json.dumps({"fa":"not valid","status":0}))
		# except Exception:
		# 	return HttpResponse(json.dumps({"message":"Something went wrong"}))
		# return HttpResponse(json.dumps({"MEssage":"Something done check correctly"}))
	# permission_classes = [permissions.AllowAny]

	def get(self,request,orgname,branch):
		# try:
		tenant = TenantList.objects(org_name=orgname,branch_name=branch).first().tenant_id
		# print tenant
		counters = ServiceCounter.objects(bank_id =tenant)
		x1 = counters.first().allot
		# x1 = [x.to_dict() for x in counters]
		# x1 = [Convert.to_d1(x.to_dict()) for x in x1]
		x1 = [str(x.counter_name) for x in x1]
		print x1
		tee= Tenant(orgname,branch)
		asa = tee.getCounters()
		# x2 = serialize('json', counters, cls=DjangoJSONEncoder)
		# x = model_to_dict(counters)
		return HttpResponse(json.dumps({"counters":asa,"status":1}))
		# except:
			# return HttpResponse(json.dumps({"MEssage":"something went wrong","status":0}))



# class CounterList(ListAPIView):
# 	#ss=get_serializer_class(CustomUser)
# 	queryset = ServiceCounter.objects()
# 	serializer_class = CustomUserSerializer
class StaffObtainToken(APIView):
	permission_classes = [permissions.AllowAny]

	def post(self,request):
		serializer = UserAuthenticate(data=request.data)
		# print "yeah"
		if serializer.is_valid():
			try:
				username = serializer.initial_data['username']
				user = StaffNew.objects.get(username=username,password=serializer.initial_data['password'])
				token = Token.objects.get(user=user)
				return HttpResponse(json.dumps({"token1":token.key}))
				
			except Exception:
				try:
					customer = StaffNew.objects.get(username=username)
					if customer is not None:
						return HttpResponse(json.dumps({"Message":"Password or Username incorrect"}))
					else:
						return HttpResponse(json.dumps({"Message":"Password or Username incorrect"}))
				except Exception:
					return HttpResponse(json.dumps({"status":"0","Message":"User Doesnot Exist"}))
		else:
			return HttpResponse(json.dumps({"status":"0",'Message':'Something went wrong in username or password'}))


from user import UserHandler
from django.core.exceptions import ObjectDoesNotExist
class User_Requests(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,username):
		# try:
		user=UserHandler(username)
		# print user.user
		if user.user is not None:

			requests = user.getRequests()
			return HttpResponse(json.dumps({"status":"1","user_requests":requests}))
		else:
			return HttpResponse(json.dumps({"message":"Its no good"}))

class UserObject(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,username):
		try:

			# print "In user Object"
			user= UserHandler(username)
			if user.user is not None:			 
				# print user.getUser()
				u=user.getUser()
				return HttpResponse(json.dumps({"user":u,"status":"success"}))
			else:
				return HttpResponse(json.dumps({"message":"User does not exist or try correct username","status":"success"}))

		except ObjectDoesNotExist:
			return HttpResponse(json.dumps({"message":"User does not exist or try correct username","status":"success"}))

class Request(APIView):
	permission_classes = [permissions.AllowAny]
	def get(self,request,username,requestId):
		try:
			user=UserHandler(username)
			if user.user is not None:
				userRequest = user.getRequests(requestId)
				return HttpResponse(json.dumps({"request":userRequest,"status":1}))
			else:
				return HttpResponse(json.dumps({"message":"please register and use the app"}))
		except:
			return HttpResponse(json.dumps({"message":"Its no good","status":0}))