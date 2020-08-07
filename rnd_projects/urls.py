from . import views
from django.urls import path
from django.conf.urls import url
app_name='rnd_projects'
urlpatterns = [
    path('add_project',views.add_projects,name='add_projects'),
    path('Upload_Project_2',views.Upload_Project_2,name='Upload_Project_2'),   
    path('ReadyProjectDetails/<int:pk>',views.ReadyProjectDetails,name='ReadyProjectDetails'),

    path('ReadyProjectShow',views.ReadyProjectShow,name='ReadyProjectShow'),
    path('project_pagecheckout_bynow/<int:pk>',views.project_pagecheckout_bynow,name='project_pagecheckout_bynow'),
    path('project_order_plan',views.project_order_plan,name='project_order_plan'),

    path('add_questions',views.add_questions,name='add_questions'),
    path('show_question_list',views.show_question_list,name='show_question_list'),
    path('ShowQuestion/<int:pk>',views.ShowQuestion,name='ShowQuestion'),
    
    path('getanswer',views.getanswer,name='getanswer'),
    path('buylike',views.buylike,name='buylike'),

    path('addtask',views.add_task,name='addtask'),
    path('viewtask',views.viewtask,name='viewtask'),
    path('taskdetails/<int:id>',views.taskdetails,name='taskdetails'),
    path('bidding',views.bidding,name='bidding'),
    path('buybid',views.buybid,name='buybid'),
    path('pagecheckout_bynow/<int:mid>',views.pagecheckout_bynow,name='pagecheckout_bynow'),
    path('paymentpage',views.paymentpage,name='paymentpage'),
  
    path('paytm', views.paytm, name='paytm'),
    path('response', views.response, name='response'),
    path('recipt', views.recipt, name='recipt'),
    path('payments_home', views.payments_home, name='payments_home'),

   
    # path('order_plan/<int:mids>',views.order_plan,name='order_plan'),
    # path('handlerequest', views.handlerequest, name='handlerequest'),
    # path('paymentdetail',views.paymentdetail,name='paymentdetail'),
    
    

]
