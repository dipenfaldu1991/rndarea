from . import views
from django.urls import path
from django.conf.urls import url
app_name='accounts'
urlpatterns = [
    path('', views.ragister,name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_logout/$',views.user_logout,name='user_logout'),
    path('dashboard_settings/',views.dashboard_settings,name='dashboard_settings'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
]