from django.shortcuts import (render,redirect)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.
from django.http import HttpResponse 
from django.views.generic import View
from .api import TenantView
from .api import ( TenantRequestQueue,
	TenantRequestComplete,
	TenantBranchList,
	TenantServicesList,
	TenantAddServices,
	UserRegister,
	UserList,
	ObtainToken,
	StaffUser,
	AddService,
	Counters,
	TenantCounterRequest,
	User_Requests,
	UserObject,
	Request,
	)
#from django.templates import RequestContext 
from .models import UserRequests,CustomUser
def index(request):
	# print STATIC_URL
	 
	response = render(request,'index.html',{})
	return response

def dashboarduser(request):
	response= render(request,'dashboard_user.html',{})
	return response

def register(request):
	response = render(request,'bankRegister.html',{})
	return response

def home(request):
	response = render(request,'slot.html',{})
	return response

def home(request):
	response = render(request,'login.html', {})
	return response

# def ulogin(request):
def employeeDashboard(request):
	response = render(request,'emp_Dashboard.html',{})
	return response

def employeeLogin(request):
	response = render(request,'employeeLogin.html',{})
	return response

from .models import TenantList,TenantUser

def book(request):
	#tenants = TenantList.objects.all()
	tenants = ["sbh","sbi","IDBI","canara","IOB","Indian BANK"]    
	response = render(request,'allocate.html',{'tenants':tenants})
	return response


def tenantnew(request):
	response = render(request,'tenant_new.html',{})
	return response
def userSignup(request):
	response = render(request,'User_signup.html',{})
def addservices(request):
	response = render(request,'addservices.html',{})
	return response
# from django.contrib.auth.models import User, Group
# from rest_framework import viewsets, generics

# from appoint.serializers import UserSerializer, GroupSerializer

# class UserViewSet(viewsets.ModelViewSet):
# 	'''
# 	API endpoint that aloows users to be viewes.
# 	'''
# 	queryset = User.objects.all()
# 	serializer_class = UserSerializer

# class GroupViewSet(viewsets.ModelViewSet):
# 	"""docstring for GroupSerializer"""
# 	queryset = Group.objects.all()
# 	serializer_class = GroupSerializer

# class Group2ViewSet(generics.ListCreateAPIView):
# 	"""docstring for GroupViewSet"generics.ListCreateApiViewdef __init__(self, arg):
# 				super(GroupViewSet,generics.ListCreateApiView.__init__()
# 				self.arg = arg
# 	"""
# 	queryset = Group.objects.all()
# 	serializer_class = GroupSerializer		


#

def tenantrequest(request):
	response = render(request,'tenantrequest.html',{})
	return response

	
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
#from .serializers import UserSignUpSerializer

@api_view(['GET','POST'])
def services_list(request):
	"""
		List Number of Servcies for the Bank This is a endpoint just listing the services 
	"""
	if request.method == 'GET':
		services = {'servcie1':'Account Creation','service2':'Debit Card Registration',"optinal":[{"tax_services":"Avaiable","contact":"appoint@gmail.com"}]}
		serializer = services
		return HttpResponse(json.dumps(serializer))
	elif request.method == 'POST':
		serializer = UserSignUpSerializer(data=request.data)
		
		#return Response(serilazer)
		if serializer.is_valid():
			serializer.save()
			return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(
			serializer.errors, status=status.HTTP_400_BAD_REQUEST
			)

import uuid
import json
from .models import UserRequest,TenantServiceRequest,UserRequestServices
from .serializers import UserRequestServicesSerializer
from mongoengine import connect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
@api_view(['GET','POST'])
@permission_classes((AllowAny,))
def allocate_slot(request):
	"""
		Method to create a slot and sends the message to User and Client

	"""
	if request.method == 'GET':
		#return HttpResponse(json.dumps({'request':'under construction'}),status=status.HTTP_201_CREATED)
		user_requests = UserRequest.objects.filter()
		userrequest = []
		for x in user_requests:
			temp = x.to_dict()
			userrequest.append(Convert.to_d1(temp))
		user_req_json=json.dumps({"requests":userrequest},ensure_ascii=False)

		return HttpResponse(user_req_json)


	elif request.method == 'POST':
		#sss=connect('User_request')
		#print sss
		print "connecting to database"
		serializer = UserRequestServicesSerializer(data=request.data)
		if serializer.is_valid():
			print 'serializer'
			# s=serializer.save()
			# ten = TenantList.objects(org_name=serializer['bank_name'],
			# 		branch_name=serializer['branch_name'],
			# 		services_list=['service_name'])
			user = CustomUser.objects.get(username=serializer['full_name'].value)
			request_id = str(uuid.uuid4())
			s= UserRequestServices(full_name=serializer['full_name'].value,
				email=serializer['email'].value, 
				bank_name= serializer['bank_name'].value,
				branch_name=serializer['branch_name'].value,
				service_name=serializer['service_name'].value,
				processed="NO",user_id = user.user_id,
				request_id = request_id
				)
			# s.update(set__processed="NO")
			#s = serializer.all.objects.get()
			# model = UserServingD
			#user.save()
			# s.save()
			# s.update(set__processed="NO")
			
			# s= Convert.to_d1(s.to_dict())
			#s['processed'] = 'NO'
			# uid = Book.setUserid()
			# s.update({'user_id' : uid})
			# s['processed'] = "NO"

			print  " this is serializer %s", serializer['bank_name'].value
			ten = TenantList.objects(org_name=serializer['bank_name'].value,
					branch_name=serializer['branch_name'].value,
					services_list=serializer['service_name'].value)
			print ten
			tsr = TenantServiceRequest.objects(tenant_id=ten[0].tenant_id,org_name=ten[0].org_name,
            		branch_name=ten[0].branch_name)
			# tsr.save()

			s = tsr.update(add_to_set__services_name1 =[s])
			print 
			userrequest=UserRequests.objects(user_id=user.user_id)
			print userrequest
			s =userrequest.first().update(add_to_set__requests=[request_id])
			print s
			#tsr.save()
			return HttpResponse(json.dumps({"message":"successfully created ",}),status=status.HTTP_201_CREATED)
		else:
			return Response(
			serializer.errors, status=status.HTTP_400_BAD_REQUEST
			)


class Convert:
	@staticmethod
	def to_d1(i):
		d2 = dict((str(k),str(v)) for k,v in i.items())
		return d2

from .models import TenantList
class Book(object):
	counter = 0
	tcounter = 0

	@staticmethod
	def setUserid():
		Book.counter += 1

		return "APSSQU" + str(Book.counter).zfill(9)


	@staticmethod
	def setTenantid():
		Book.tcounter += 1
		return "APSSQT" + str(Book.tcounter).zfill(5)
	
	def book_service(self,object):
		#if object.servie_name == "ATM":
		user_id = setUserid()
		#tenant_id = "dasa1223"
		object['user_id'] = user_id
		#object['tenant_id'] = tenant_id
		#store to databases

		ten = TenantList.objects(org_name=object['org_name'],branch_name=object['branch_name'],services_list="cheque")

		v=add(object)
		if v == 1 :
			print "successfully created slot"
		else :
			print "Service is out today"
	
	def add(self,object):
		s=ServiceRegister(object)
		s.save()
		return s

import uuid
from .tenant import Tenant
@api_view(['POST'])
@permission_classes((AllowAny,))
def create_tenant(request):
	""" Creating new Tenants using this rest API
		parameters required are name, email,org_name, branch_name,sercies list


	 """
	if request.method == 'POST':
		tenant_new = json.loads(request.body)
		#create the tenant id 
		tenant_new['tenant_id'] = str(uuid.uuid4())

		s = Tenant(tenant_new)
		s1=s.getClass()
		s.create()
		s.createDB()
		#s.save()
        
		#partialtenant_id = "APSSQT" + str(tid).zfill(4)
		#s = Tenant()
	return HttpResponse(json.dumps({"Message":"successfully created"}))


from .models import TenantList
# @permission_classes(('AllowAny',))
@api_view(['GET','POST'])
@permission_classes((AllowAny,))
def tenants(request):
	"""retrives the information about tenants 
	"""
	if request.method == 'GET':
		# permission_classes=[permissions.AllowAny]
		tenants = TenantList.objects()
		array_tenants = []
		for x in tenants:
			array_tenants.append(Convert.to_d1(x.to_dict()))
		resp_json = array_tenants
		return HttpResponse(json.dumps({"tenants":resp_json}))




@api_view(['POST'])
def editTenant(request):
	""" editing the existing tenant id and thier related services and 
	input parameters required are name, email, org_name, branch_name,
	for updating the services list required servcies List,
	can change any name except org_name 

	"""
	if request.method == 'GET':
		return HttpResponse(json.dumps({"message":" Thank you for you application This under construction! "}))

	elif request.method == 'POST':
		tenant_edit = json.loads(request.body)
		# d = json.dumps({"message":data})
		# if tenant.update == 'services_list':
		# if tenant.update == 'username':
		# if tenant.update == '':
		ten = TenantList.objects(org_name=object['org_name'],branch_name=object['branch_name'],services_list="cheque")
		return HttpResponse(json.dumps({"message":[tenant_edit]}))


from .models import UserRequests,CustomUser
#@exempt('authentication')

#@permission_classes((AllowAny,))
@api_view(['POST'])
@permission_classes((AllowAny,))
def newuser(request):
	if request.method == "GET":
		return HttpResponse(json.dumps({"message":" Thank you for you application This under construction! "}))
	elif request.method == 'POST':
		try :
			userNew = json.loads(request.body)
			uid =str(uuid.uuid4()).encode('utf-8')
			userNew.update({'user_id':uid})
			# print userNew
			# uid = str(uuid.uuid4())
			# temp_urequests = UserRequests()
			# temp_urequests.save()
			user_model = CustomUser(username=userNew['username'],
				email=userNew['email'],
				#mobile=userNew['mobile'],
				user_id=userNew['user_id'],
				password=userNew['password'],
				)
			user_model.save()
			userrequest=UserRequests(user_id=userNew['user_id'])
			userrequest.save()
			return HttpResponse(json.dumps({"message":"success fully created","status":1}))
		except ValueError:
			return HttpResponse(json.dumps({"error" :"value error given by user"}))
		
from .form import StaffForm,StaffNew	
from django.forms.models import model_to_dict
from .models import TenantList	
class UserLogin(View):
	form_class = StaffForm
	template_name = 'employeeLogin.html'
	def get(self,request):
		return render(request,self.template_name,{'form':StaffForm})

	def post(self,request):
		form=StaffForm(request.POST)
		print "checking form"
		if form.is_valid():
			print "Form valid"
			# user = form.save(commit=False)

			username=form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = StaffNew.objects.get(username=username,password=password)
			print user
			if user is not None:
				# if user.is_active:
				# token= Token()
				# token = Token.objects.get(user=user)
				# if token is not None:
				tenant = TenantList.objects(tenant_id=user.bank_id)
				print tenant.first()
				tenant=tenant.first().to_dict()
				# t=model_to_dict(tenant)

				# return redirect('employeeDashboard',)'user':model_to_dict(user)
				return redirect(empDash,user=user.user_id,tenant=tenant['tenant_id'])
				# else:
					# Token
		return render(request,self.template_name,{'form':StaffForm})
#tenant employees dashboard or home page
def empDash(request,user,tenant):
	user = StaffNew.objects.get(user_id=user)
	tenant= TenantList.objects(tenant_id=tenant).first().to_dict()
	return render(request,'employeeDashboard .html',{'tenant':tenant,'user':user})



#Authentication page requets and responses.
#takes request from a browser loads the page
#Gets username,pasword and autheication checks using rest api of Obtain token api
from rest_framework.authtoken.models import Token
import requests
class UserLogIn(View):
	template_name='userLogin.html'
	def get(self,request):
		return render(request,self.template_name,{'form':StaffForm})

	def post(self,request):
		form=StaffForm(request.POST)
		print "checking form1"
		if form.is_valid():
			print "if"
			# try:
			username=form.cleaned_data['username']
			password = form.cleaned_data['password']
			print "try"
			headers={'Content-type':'application/json'}
			data = {"username":username,"password":password}
			r= requests.post('http://172.27.30.119:8000/appoint/api/gettoken/',json=data,headers=headers)
			
			# print r['message']
			print r.text
			# username = serializer.initial_data['username']
			print "hell"
			print "%s,%s" %(username,password)
			user = CustomUser.objects.get(username=username,password=password)
			print user
			token = Token.objects.get(user=user)
			print token
			return redirect(userDash,user=user.user_id)
			# return HttpResponse(json.dumps({"token1":token.key}))				
		return render(request,self.template_name,{'form':StaffForm})

#user dashboard or home page
def userDash(request,user):
	user = CustomUser.objects.get(user_id=user)
	token = Token.objects.get(user=user)
	return render(request,'userDashboard.html',{'user':user})

class StaffLogin(View):
	template_name = 'employeeLogin.html'
	def get(self,request):
		return render(request,self.template_name,{'form':StaffForm})

	def post(self,request):
		form=StaffForm(request.POST)
		print "checking form"
		if form.is_valid():
			print "Form valid"
			# user = form.save(commit=False)

			username=form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = StaffUser(username=username,password=password)
			print user
			if user is not None:
				# if user.is_active:
				tenant = TenantList(tenant_id=user.bank_id)
				tenant=tenant.to_dict()
				return redirect('employeeDashboard')
		return render(request,self.template_name,{'form':StaffForm})