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

]
