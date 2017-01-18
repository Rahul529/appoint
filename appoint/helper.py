class Convert:
	@staticmethod
	def to_d1(i):
		d2 = dict((str(k),str(v)) for k,v in i.items())
		return d2

class ConToDict:
	@staticmethod
	def convert(elements):
		temp = []
		for x in elements:
			temp2 = Convert.to_d1(x)
			temp.append(temp2)
		return temp

# Schedules the user requests in the counters and schedules base don no.of counters 
#input parameters : lists of userrequest and no. of counters 
import datetime
class Schedule:

	def __init__(self,lists,counters):
		self.list_reqs = lists
		self.counters = counters
	def schedule(self):
		temp = [[] for x in range(0,self.counters)]
		# temp2 = 
		list_req =[Convert.to_d1(x.to_dict()) for x in self.list_reqs] 
		# temp.append([])
		for x in list_req:
			ind = (list_req.index(x)+1)%self.counters
			print ind
			x.update({"timep":180*ind-1,"c":"c"+str(ind)})
			#[dict({"c"+str(x+1):[]})for x in range(0,3)]
			temp[ind-1].append(x)
		for x in temp:
			for y in x:
		 		y.update({"timep":str(datetime.datetime.now()+datetime.timedelta(seconds=180*(x.index(y)+1)))})

		
		return temp




from .models import User
class TimerUpdate:
 	def __init__(self,lists):
  		self.lists = lists
  	def updateTime(self):
  		for counter in self.lists:  			
  			for object_user in counter:
  				# print object_user['user_id']
  				user = User.objects(user_id =object_user['user_id'],requests__request_id=object_user['request_id']).update(set__requests__counter=object_user['c'],set__requests__timestamps=object_user['timep'])

from appoint.models import TenantServiceRequest
from .models import TenantList,ServiceCounter

class Nonsense:
	@staticmethod
	def sched(counters,name,branch):
		req_cheque = TenantServiceRequest.objects(org_name=name,services_name1__service_name="cheque",branch_name=branch)
		requests = req_cheque.first().services_name1
		sche = Schedule(requests,counters)
		new_list = sche.schedule()
		return new_list


class Tenant:
	def __init__(self,orgname,branch):
		self.orgname = orgname
		self.branch=branch
		self.tenant_id = ""

	def getCounters(self):
		tenant = TenantList.objects(org_name=self.orgname,branch_name=self.branch).first().tenant_id
		# print tenant
		counters = ServiceCounter.objects(bank_id =tenant)
		x1 = counters.first().allot
		# x1 = [x.to_dict() for x in counters]
		# x1 = [Convert.to_d1(x.to_dict()) for x in x1]
		x1 = [str(x.counter_name) for x in x1]
		return x1

	def getRequests(self,counter_name=None):
		if counter_name==None:
			req_cheque = TenantServiceRequest.objects(org_name=self.orgname,branch_name=self.branch)
			requests = req_cheque.first().services_name1.filter(processed="NO")
			# sche = Schedule(requests,counters)
			new_list = self.schedule(requests,self.getCounters())
			return new_list
		else:
			# req_cheque = TenantServiceRequest.objects(org_name=self.orgname,branch_name=self.branch,services_name1__counter=counter_name)
  			req_cheque = TenantServiceRequest.objects.get(org_name=self.orgname,branch_name=self.branch).services_name1.filter(processed="NO",counter=counter_name)
			# requests = req_cheque.first().services_name1.filter(processed="NO")
  			return	[Convert.to_d1(x.to_dict()) for x in req_cheque] 


	def schedule(self,lists,counters):
		lenc = len(counters)
		temp = [[] for x in range(0,lenc)]
		# temp2 = 
		list_req =[Convert.to_d1(x.to_dict()) for x in lists] 
		# temp.append([])
		for x in list_req:
			ind = (list_req.index(x)+1)%lenc
			print ind
			x.update({"timep":180*ind-1,"counter":counters[ind]})
			temp[ind-1].append(x)
		for x in temp:
			for y in x:
				y.update({"timep":(datetime.datetime.now()+datetime.timedelta(seconds=180*(x.index(y)+1))).strftime('%H:%M:%S %d-%m-%Y')})
		self.updateTime(temp)
		return temp

	def updateTime(self,lists):
		tent_update = TenantServiceRequest._get_collection()
		for counter in lists:  			
  			for object_user in counter:
  				# print object_user['user_id']
  				# user = User.objects(user_id =object_user['user_id'],
  				# 	requests__request_id=object_user['request_id']).update(set__requests__counter=object_user['c'],
  				# 	set__requests__timestamps=object_user['timep'])
  				print object_user['timep']
  				proccess_chequew = TenantServiceRequest.objects.get(org_name=self.orgname,branch_name=self.branch).services_name1.filter(user_id=str(object_user['user_id']))
  				print proccess_chequew
  				bbb = tent_update.update({"services_name1.request_id":str(object_user['request_id'])},{'$set':{'services_name1.$.counter':object_user['counter'],'services_name1.$.timep':str(object_user['timep'])}})
  				print bbb
  				# requests= TenantServiceRequest.objects(org_name=self.orgname,
  				# 	branch_name=self.branch,
  				# 	services_name1__user_id=object_user['user_id'],
  				# 	services_name1__request_id=object_user['request_id']).update(services_name1__counter=object_user['c'],
  				# 		services_name1__timestamps=object_user['timep'])


  	# def getRequests(self,counter_name):
  	# 	req_cheque = TenantServiceRequest.objects(org_name=self.orgname,branch_name=self.branch,services_name1__counter=counter_name)
  	# 	return	[Convert.to_d1(x.to_dict()) for x in req_cheque] 

  	def getAllStaff(self,staffname):
  		tenant_id=TenantList.objects(org_name=self.orgname,branch_name=self.branch).first().tenant_id
  		staff = StaffNew.objects.filter(bank_id=tenant_id)




  	def scheduledRequests(self,countername,username):
  		# x = Counter
  		self.tenant_id=TenantList.objects(org_name=self.orgname,branch_name=self.branch).first().tenant_id
  		counter = ServiceCounter.objects(bank_id=self.tenant_id,allot__staff=username).first().counter_name
  		requests=self.getRequests(counter)
  		return requests




# def update_to_users(self,requests):
