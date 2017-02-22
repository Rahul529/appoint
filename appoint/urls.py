from django.conf.urls import include, url
#from django.generics.views import RedirectView
from rest_framework import routers
from . import views
#from django.contrib import admin
import appoint.views  as view
from rest_framework.authtoken import views
# from .api import UserList
# from .api import TenantView

# router = routers.DefaultRouter()
# router.register(r'users',views.UserViewSet)
# router.register(r'api/tenant/(?P<string>[\w\-]+)$',views.TenantView)
# router.register(r'groups',views.GroupViewSet)
#router.register(r'groups2',views.Group2ViewSet)
urlpatterns = [
	#url(r'^$', views.login, name='login'),
	
	
	#url(r'^/', include('appoint.urls')),	
	url(r'^$', view.index, name='index'),
	url(r'^dashboard/user/$',view.dashboarduser,name='dashboarduser'),
	url(r'home', view.home, name='home'),
	url(r'allot', view.book,name='book'),
	url(r'user/login/$',view.UserLogIn.as_view(),name='userLogin'),
	url(r'bank/login1/$',view.UserLogin.as_view(),name='eLogin'),
	url(r'bank/login/$',view.employeeLogin,name='employeeLogin'),
	url(r'dashboard/employee/$',view.employeeDashboard,name='employeeDashboard'),
	url(r'(?P<tenant>[\w\-]+)/dashboard/(?P<user>[\w\-]+)/$',view.empDash,name='empDash'),
	url(r'dashboard/(?P<user>[\w\-]+)/$',view.userDash,name='userDash'),

	url(r'register/$',view.register,name='register'),
	url(r'^tenant/$',view.tenantnew,name='tenantnew'),
	url(r'^api/token/',views.obtain_auth_token),
	url(r'^api/gettoken/$',view.ObtainToken.as_view()),
	url(r'tenant/addservices',view.addservices,name='addservices'),
	url(r'^api/tenant/(?P<name>[\w\-]+)/(?P<branch>[\w\-]+)$', view.TenantView.as_view()),
	url(r'^api/user/register/$', view.UserRegister.as_view()),
	url(r'^api/user/$',view.UserList.as_view()),
	url(r'^api/user/(?P<username>[a-zA-Z0-9\d-]+)/requests/$',view.User_Requests.as_view()),
	url(r'^api/user/(?P<username>[a-zA-Z0-9\d-]+)$',view.UserObject.as_view()),
	url(r'^api/user/(?P<username>[a-zA-Z0-9\d-]+)/request/(?P<requestId>[a-zA-Z0-9\d-]+)',view.Request.as_view()),
	url(r'^api/staff/new',view.StaffUser.as_view()),
	url(r'^api/staff/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/$',view.StaffUser.as_view()),
	url(r'^api/tenant/(?P<name>[\w\-]+)/(?P<branch>[\w\-]+)/$',view.TenantRequestQueue.as_view()),
	url(r'^api/tenant/(?P<name>[\w\-]+)/(?P<branch>[\w\-]+)/request$',view.TenantRequestComplete.as_view()),
	url(r'^api/branch/(?P<orgname>[\w\-]+)/$',view.TenantBranchList.as_view()),
	url(r'^api/services/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/$',view.TenantServicesList.as_view()),
	url(r'^api/service/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/(?P<servicename>[\w\-]+)$',view.TenantAddServices.as_view()),
	url(r'^api/service/add/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/(?P<servicename>[\w\-]+)$',view.AddService.as_view()),
	# url(r'',include(router.urls)),
	# url(r'^',include(TenantVi-*ew.urls)),0
	# url(r'^',include()),
	# url(r'^api/users/$', TenantView.as_view()),
	# url(r'^api/tenant/([a-zA-Z0-9])/$',UserList.as_view()),
	url(r'^api/services/$',view.services_list,name='services_list'),
	url(r'^api/services/book/$',view.allocate_slot,name='allocate_slot'),
	url(r'^api/add/tenant/$',view.create_tenant, name='create_tenant'),
	url(r'^api/edit/tenant/$',view.editTenant, name='editTenant'),
	url(r'^api/tenants/$',view.tenants,name='tenants'),
	url(r'^api/newuser/$',view.newuser,name=''),
	url(r'^api/counter/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/new/$',view.Counters.as_view()),
	url(r'^api/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/counter/$',view.Counters.as_view()),
	url(r'^api/(?P<orgname>[\w\-]+)/(?P<branch>[\w\-]+)/counter/(?P<counter>[\w\-]+)/$',view.TenantCounterRequest.as_view()),

	#url()
	# url(r'^api/tenant/(?P<name>[\w\-]+)$','','appoint.views.retrieveTenant',name='retrieveTenant')
		#url(r'^/login$','appoint.views.login',name='login'),
	# url(r'appoint/api/', include('rest_framework.urls'))
]
