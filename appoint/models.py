from __future__ import unicode_literals
#from djangotoolbox.fields import ListField
from django.db import models
# from django.db.models import user
#from mongoengine  import Document
from mongoengine import *


# Create your models here.
from django.conf import settings

from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth.models import ( BaseUserManager,AbstractBaseUser)
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
	#user = models.OneToOneField(settings.AUTH_USER_MODEL)
	#email = models.EmailField(max_length=150,unique=True)
	#username=models.CharField(max_length=40)
	user_id = models.CharField(max_length=40,unique=True)
	#password=models.CharField(max_length=40,default='password')
	#is_staff = models.BooleanField(default=False)
	#is_admin = models.BooleanField(default=False)
	#USERNAME_FIELD= 'email'
	REQUIRED_FIELDS=['user_id']
	class Meta:
		db_table ='auth_user'

	def to_dict(self):
		d={}
		d['user_id']=str(self.user_id)
		d['username']=str(self.username)
		d['email']=str(self.email)
		d['date_joined']=str(self.date_joined)
		return d




class UserServingD(DynamicDocument):
	"""
		Model for incoming request and also for database
		which takes input of the user and checks the feilds.
	"""

	email = StringField(required=True)
	full_name = StringField(max_length=20,blank=True,null=True)
	bank_name = StringField(max_length=20)
	branch_name = StringField(max_length=20)
	service_name = StringField(max_length=20)
	timestamp = DateTimeField(auto_now_add=True,auto_now=False)


class UserRequest(DynamicDocument):
	"""
		Model for incoming request and also fro database
		which takes input of the user and checks the feilds.
	"""

	email = StringField(required=True)
	full_name = StringField(max_length=20,blank=True,null=True)
	bank_name = StringField(max_length=20)
	branch_name = StringField(max_length=20)
	service_name = StringField(max_length=20)
	timestamp = DateTimeField(auto_now_add=True,auto_now=False)
 	
 	def to_dict(self):
 		d = {}
		d['email']=str(self.email)
		d['full_name']=str(self.full_name)
		d['branch_name']=str(self.branch_name)
		d['bank_name']=str(self.bank_name)
		d['service_name']=str(self.service_name)
		return d


	#meta = {'allow_inheritance':True}

	#def __unicode__(self):
	#	return self
    #    return self.emaili
import datetime
class UserRequestServices(EmbeddedDocument):
	"""
		Model for incoming request and also for database
		which takes input of the user and checks the feilds.
	"""

	email = StringField(required=True)
	full_name = StringField(max_length=20,blank=True,null=True)
	bank_name = StringField(max_length=20)
	branch_name = StringField(max_length=20)
	service_name = StringField(max_length=20)
	processed = StringField(auto_now_add=True,auto_now_value="NO")
	timestamp = DateTimeField(default=datetime.datetime.now())
	user_id = StringField(required=True)
	request_id = StringField(required=True)
	timep = StringField()
	counter=StringField()

	def to_dict(self):
 		d = {}
 		d['request_id'] = str(self.request_id)
 		d['user_id'] = str(self.user_id)
		d['email']=str(self.email)
		d['full_name']=str(self.full_name)
		d['branch_name']=str(self.branch_name)
		d['bank_name']=str(self.bank_name)
		d['service_name']=str(self.service_name)
		d['processed'] = str(self.processed)
		d['timestamp'] = str(self.timestamp)
		d['timep']=str(self.timep)
		d['counter']=str(self.counter)

		return d






class ServiceRegister(DynamicDocument):
	"""all the tennats and their mapped tennats not in usage
	"""
	user_id = StringField(required=True)
	tenant_id = StringField(required=True)




#creates the new tenants 
class TenantList(DynamicDocument):
	"""database fro tenants 
	"""
	tenant_id = StringField(required=True,unique=True)
	tenant_name = StringField(required=True)
	org_name = StringField(required=True)
	branch_name = StringField(required=True,unique=True)
	services_list = ListField(StringField(max_length=10,unique=True))
	email = EmailField(required=True)
	meta = {'allow_inheritance':True}

	def to_dict(self):
 		d = {}
		d['tenant_id']=str(self.tenant_id)
		d['tenant_name']=str(self.tenant_name)
		d['org_name']=str(self.org_name)
		d['branch_name']=str(self.branch_name)
		d['services_list']=str(self.services_list)
		return d




#stores the user requests for the tenants
#from .helper import ConToDict
class TenantServiceRequest(DynamicDocument):
	"""database for the tenants requests,requests are stores this database
	"""
	tenant_id = StringField(required=True)
	org_name = StringField(required=True)
	branch_name = StringField(required=True)
	services_name1 = EmbeddedDocumentListField(UserRequestServices)

#DB of request of Users and a new request for each request, sub document of the User requests Field 	
# class UserRequests(EmbeddedDocument):
	# request_id = StringField(required=True)
	# counter = StringField(required=True)
	# timestamps = StringField(required=True)

# this class stores the users in nosql as followibg format 
class UserRequests(DynamicDocument):
	user_id = StringField(required=True)
	# full_name = StringField(required=True)
	# email = EmailField(required=True)
	# mobile = StringField(required = True)
	requests=ListField(StringField(max_length=50))
	# requests = EmbeddedDocumentListField(UserRequests)
	# meta = {'allow_inheritnace':True}
	
	def to_dict(self):
		d={}
		d['user_id']=str(self.user_id)
		d['requests']=str(self.requests)




class TenantUser(DynamicDocument):
	tenant_id = StringField(required=True)
	Manager_name = StringField(required=True)
	email = EmailField(required=True)
	mobile = StringField(required=True)
	password = StringField(required=True)
	meta = {'allow_inheritnace':True}
from django.contrib.auth.models import User

# class User(user):
# 	"""docstring for User"""
# 	def __init__(self, arg):
# 		super(User, self).__init__()
# 		self.arg = arg
# 		

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False,**kwawrgs):
	if created:
		Token.objects.create(user=instance)


# class StaffUser(AbstractUser):
# 	#user = models.OneToOneField(settings.AUTH_USER_MODEL)
# 	#email = models.EmailField(max_length=150,unique=True)
# 	#username=models.CharField(max_length=40)
# 	user_id = models.CharField(max_length=40,unique=True)
# 	#password=models.CharField(max_length=40,default='password')
# 	#is_staff = models.BooleanField(default=False)
# 	#is_admin = models.BooleanField(default=False)
# 	#USERNAME_FIELD= 'email'
# 	REQUIRED_FIELDS=['user_id']
# 	class Meta:
# 		db_table ='auth_user'

# from authtools.models import AbstractNamedUser
# class MyUserManager(BaseUserManager):
#  	def create_user(self,email,password=None):
#  		if not email:
#  			raise ValueError('Usres must have an email address')
#  		user = self.model(
#  			email=slef.normailize_email(email),
#  		)

#  		user.set_password(password)
#  		user.save(using=self._db)
#  		return user
#  	def create_superuser(self,email,password):
#  		user = self.create_user(
#  			email,password=password,
#  		)
#  		user.is_admin = True
#  		user.save(using=self._db)
#  		return user

# class StaffUser(AbstractBaseUser):
#  	email = models.EmailField(
#  		verbose_name='email address',
#  		max_length = 200,
#  		unique= True,
#  	)
# # 	date_of_birth=models.DateField()
#  	is_active = models.BooleanField(default=True)
#  	is_admin = models.BooleanField(default=False)
#  	bank_id = models.CharField(unique=True,max_length=50)
#  	user_id = models.CharField(unique=True,max_length=50)
#  	username = models.CharField(unique=True,max_length=50)
#  	counter = models.CharField(max_length=5)
#  	objects=MyUserManager()

#  	USERNAME_FIELD = 'email'
#  	REQUIRED_FIELDS=['email']


# # 	def get_full_name(self):
# # 		return self.email 
# # 	def get_short_name(self):
# # 		return self.email
# # 	def __str__(self):
# # 		return self.email

# 	def has_perm(self,perm,obj=None):
# 		return True
# 	def has_module_perms(self,app_label):
# 		return True
#  	@property
#  	def is_staff(self):
#  	    return self.is_admin
	
class Counter(EmbeddedDocument):
	staff = StringField(required=True)
	counter_name = StringField(required=True)
	services_list = ListField(StringField(max_length=10))
	timestamps = DateTimeField(required=True,default=datetime.datetime.now())

	def to_dict(self):
		d={}
		d['staff']=str(self.staff)
		d['counter_name']=str(self.counter_name)
		d['services_list']=str(self.services_list)
		d['timestamps']=str(self.timestamps)
		return d


class ServiceCounter(DynamicDocument):
	bank_id = StringField(required=True)
	#service = StringField(max_length=10)
	# counter_list = ListField(StringField(max_length=10))
	allot = EmbeddedDocumentListField(Counter)

	 

	def to_dict(self):
		return self.__dict__

	def to_onbe(self):
		d={}
		d['bank_id']=str(self.bank_id)
		d['allot'] =str(self.allot)
		# d['tenant_name']=str(self.tenant_name)
		# d['org_name']=str(self.org_name)
		# d['branch_name']=str(self.branch_name)
		# d['services_list']=str(self.services_list)
		return d



# class StaffUser(Model):
#  	email = models.EmailField(
#  		verbose_name='email address',
#  		max_length = 200,
#  		unique= True,
#  	)
# # 	date_of_birth=models.DateField()
#  	is_active = models.BooleanField(default=True)
#  	is_admin = models.BooleanField(default=False)
#  	bank_id = models.CharField(unique=True,max_length=50)
#  	user_id = models.CharField(unique=True,max_length=50)
#  	username = models.CharField(unique=True,max_length=50)
#  	counter = models.CharField(max_length=5)
#  	objects=MyUserManager()

#  	USERNAME_FIELD = 'email'
#  	REQUIRED_FIELDS=['email']
class StaffNew(models.Model):
	#user = models.OneToOneField(settings.AUTH_USER_MODEL)
	email = models.EmailField(max_length=254,unique=True)
	username=models.CharField(max_length=150,unique=True)
	user_id = models.CharField(max_length=150,unique=True)
	bank_id	=models.CharField(max_length=150,)
	counter = models.CharField(max_length=25)
	password=models.CharField(max_length=40)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	#USERNAME_FIELD= 'email'
	REQUIRED_FIELDS=['user_id','bank_id']
	class Meta:
		db_table ='appoint_staffnew'


