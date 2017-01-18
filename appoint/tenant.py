"""
This class creates a new tenant and also contains the editing options

TODO : editing and deleting of tenants  
"""




from .models import (TenantList,
	TenantServiceRequest,
	
	ServiceCounter,)
import uuid
class Tenant:
	def __init__(self,tenantobject):
		self.name = tenantobject['tenant_name']
		self.tenant_id = tenantobject['tenant_id']
		self.email = tenantobject['email']
		self.org_name = tenantobject['org_name']
		self.branch_name = tenantobject['branch_name']
		self.services_list = tenantobject['services_list']

	def create(self):
		s = TenantList(tenant_id=self.tenant_id,
				tenant_name=self.name,
				org_name=self.org_name,
				branch_name=self.branch_name,
				email = self.email,
				services_list = [self.services_list]
				)

		s.save()

	def createDB(self):
		s= TenantServiceRequest(tenant_id=self.tenant_id,
				org_name=self.org_name,
				branch_name=self.branch_name,
				services_list=[self.services_list]
			)
		s.save()
	def getClass(self):
		d = {}
		return d

	def getObject(self,orgname,branch):
		ello

	def schedule(self,servicename,counters,tennat_id):
		time_service = 180
		s= TenantServiceRequest(org_name="SBH",services_name1__service_name="cheque",services_name1__processed="NO")
		reqs = [ Convert.to_d1(x.to_dict())for x in req_cheque[0].services_name1]
		s = list.sort( )


	def addService(self,service_name):
		try:
			tenantobject= Tenant.objects.get(tenant_id=self.tenant_id,org_name=self.org_name,branch_name=self.branch_name)
			tenantobject.update(add_to_set__services_list=service_name)
		except Exception:
			return "something went wrong"
		return 1

	# def addUser(self,user,tenant_id):
	# 	try:
	# 		print "Hello"
	# 		s = StaffUser(bank_id=tenant_id,username= user.username,email=user.email,user_id=str(uuid.uuid4()))
	# 	except Exception:
	# 		print "print : Hello error ocurred"
	# 	return 1



	def  update_Counter_staff(self,user,counter):
		try:
			print "hello in counter update"
			
		except Exception:
			print "some more stuff needed to enter"
		return 1

	def getCounters(self):
		try:
			print "hello in counter update"
			tenant = TenantList.objects(org_name=orgname,branch_name=branch).first().tenant_id
			print tenant
			counters = ServiceCounter.objects(bank_id =tenant)
			x1 = counters.first().allot
			# x1 = [x.to_dict() for x in counters]
			# x2 = [ for x in x1]
			x1 = [str(x.counter_name) for x in x1]

			return x1
		except Exception:
			return "something went wrong"

	def authenticateStaff(self,username,password):
		staff=staffNew.objects(username=username,password=password)
		token = Token.objects.get(user=staff)			
