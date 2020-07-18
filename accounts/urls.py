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
    path('dashboard_settings',views.dashboard_settings,name='dashboard_settings'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('show_list_dash',views.show_list_dash,name='show_list_dash'),
    path('edit_questions/<int:id>/',views.edit_questions,name='edit_questions'),
    path('show_task',views.show_task,name='show_task'),
    path('edit_task/<int:id>',views.edit_task,name='edit_task'),
    path('edit_project/<int:id>/',views.edit_project,name='edit_project'),
    path('edit_project_file',views.edit_project_file,name='edit_project_file'),
    path('update_show_project',views.update_show_project,name='update_show_project'),
    
    


    
]