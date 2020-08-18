from . import views
from .views import (
    
     CommentLikeToggle,
     profile_detail,
   
    )
from django.urls import path
from django.conf.urls import url
app_name='accounts'
urlpatterns = [
    path('', views.ragister,name='register'),
    url(r'^Answer/(?P<answer_id>\d+)/likes/$', CommentLikeToggle.as_view(), name="like_toggle"),
    # url(r'^(?P<slug>[\w-]+)/', profile_detail, name="detail"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^user_logout/$',views.user_logout,name='user_logout'),
    path('profile_detail',views.profile_detail,name='profile_detail'),
    path('dashboard_settings',views.dashboard_settings,name='dashboard_settings'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('show_list_dash',views.show_list_dash,name='show_list_dash'),
    path('edit_questions/<int:id>/',views.edit_questions,name='edit_questions'),
    path('show_task',views.show_task,name='show_task'),
    path('managebidders/<int:mid>',views.managebidders,name='managebidders'),
    path('acceptbids/<int:pk>',views.acceptbids,name='acceptbids'),
    path('edit_task/<int:id>',views.edit_task,name='edit_task'),
    path('edit_project/<int:id>/',views.edit_project,name='edit_project'),
    path('edit_project_file/<int:id>',views.edit_project_file,name='edit_project_file'),
    path('update_show_project',views.update_show_project,name='update_show_project'),
    ##### chat #####
    path('create_chat/', views.create_chat, name='create_chat'),
    path('createsss_chat/<int:id>', views.createsss_chat, name='createsss_chat'),
    path('send_message/', views.send_message, name='send_message'),
    path ('profile/',views.chat_list, name='profile'),
    path('private_chat/', views.private_chat, name='private_chat'),
    path('get_private_chat_messages/', views.get_json_chat_messages, name='get_private_chat_messages'),

    path('delete_biddata/<int:pk2>/',views.delete_biddata,name='delete_biddata'),
    path('delete_Taskdata/<int:pk3>/',views.delete_Taskdata,name='delete_Taskdata'),
]