#from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
#from mongoengine import serializers
from .models import UserRequest,UserServingD,UserRequestServices
#from mongoenegine import connect
#connect('appoint')

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
# 	class Meta:
# 		model = Group
# 		fields = ('url','name')

class UserServingSerializer(DocumentSerializer):
	class Meta:
		model = UserServingD
		fields = (
			'email',
			'full_name',
			'bank_name',
			'branch_name',
			'service_name',
			'timestamp'
			)

class UserRequestServicesSerializer(DocumentSerializer):
	class Meta:
		model = UserRequestServices
		fields = (
			'email',
			'full_name',
			'bank_name',
			'branch_name',
			'service_name',
			# 'timestamp',
			'processed'
			)
	
	# def to_dict(self):
	# 	dict = {}
	# 	dict['email']=self.email
	# 	dict['full_name']=self.full_name
	# 	dict['branch_name']=self.branch_name
	# 	return dict

		# def restore_object(self, attrs, instance=None):
		# 	if instance is not None:
		# 		for k,v in attrs.iteritems():
		# 			setattr(instance,k,v)
		# 			return instance
		# 	return UserRequest(**attrs)

	# def create(self,validated_data):
	# 	return UserRequest(
 #            email=validated_data.pop('email'),
 #            full_name=validated_data['full_name'],
 #            bank_name=validated_data['bank_name'],
 #            branch_name=validated_data['branch_name'],
 #            service_name=validated_data['service_name']
 #        ).save()
from rest_framework.serializers import ModelSerializer
from .models import CustomUser
import uuid
class CustomUserSerializer(ModelSerializer):
	class Meta:
		model = CustomUser

		fields =[
			'username',
			'email',
			'password',
			'user_id',
			]

	# def create(self,data):
	# 	user=data;
	# 	user['user_id']=str(uuid.uuid4())



class UserAuthenticate(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField() 

	def username(self):
		return self.username


# class StaffUsers(ModelSerializer):
# 	class Meta:
# 		model = StaffUser

# 		files = [
# 			'email',
# 			'bank_id',
# 			'username',
# 			'is_staff',
# 		]

class Staff(serializers.Serializer):
	username= serializers.CharField()
	email= serializers.CharField()
	password=serializers.CharField()
	org_name=serializers.CharField()
	branch_name=serializers.CharField()

	def username(self):
		return self.username
	def password(self):
		return self.password
	def email(self):
		return self.email
	def org_name(self):
		return self.org_name
	def branch_name(self):
		return	self.branch_name

class CounterSerializer(serializers.Serializer):
	counter_name =serializers.CharField()
	service = serializers.CharField()
	staff_name = serializers.CharField()