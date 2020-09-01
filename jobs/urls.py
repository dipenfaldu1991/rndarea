from . import views
from django.urls import path
from django.conf.urls import url  
app_name='jobs'
urlpatterns = [
    path('add_jobs',views.add_jobs,name='add_jobs'),
    path('view_joblist',views.view_joblist,name='view_joblist'),
    path('jobdetails_byid/<int:id>',views.jobdetails_byid,name='jobdetails_byid'),
    path('jobapply_now',views.jobapply_now,name='jobapply_now'),
    path('managejobs',views.managejobs,name='managejobs'),
    path('delete_jobs/<int:pk2>',views.delete_jobs,name='delete_jobs'),
    path('managecandidates/<int:mid>',views.managecandidates,name='managecandidates'),
    path('delete_candidates/<int:pk3>',views.delete_candidates,name='delete_candidates'),
    path('edit_jobs/<int:id>',views.edit_jobs,name='edit_jobs'),
    path('jobbookmark/', views.jobbookmark, name='jobbookmark'),
    path('jobbookmarkdlt/<int:pk6>/',views.jobbookmarkdlt,name='jobbookmarkdlt'),

    #####chat
    path('create_chat/',views.create_chat, name='create_chat'),
    path('createsss_chat/<int:id>',views.createsss_chat, name='createsss_chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('profile/',views.chat_list, name='profile'),
    path('private_chat/',views.private_chat, name='private_chat'),
    path('get_private_chat_messages/',views.get_json_chat_messages, name='get_private_chat_messages1'),
    
]
