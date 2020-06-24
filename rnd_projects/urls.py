from . import views
from django.urls import path
from django.conf.urls import url
app_name='rnd_projects'
urlpatterns = [
    path('add_project',views.add_projects,name='add_projects'),
    path('Upload_Project_2',views.Upload_Project_2,name='Upload_Project_2'),
    path('pages_blog_post',views.pages_blog_post,name='pages_blog_post'),
    path('pages_checkout_page',views.pages_checkout_page,name='pages_checkout_page'),
    path('pages_invoice_template',views.pages_invoice_template,name='pages_invoice_template'),
    path('pages_order_confirmation',views.pages_order_confirmation,name='pages_order_confirmation'),
    path('ReadyProjectDetails/<int:pk>',views.ReadyProjectDetails,name='ReadyProjectDetails'),
    path('ReadyProjectShow',views.ReadyProjectShow,name='ReadyProjectShow'),
    path('add_questions',views.add_questions,name='add_questions'),
    path('show_question_list',views.show_question_list,name='show_question_list'),
    path('ShowQuestion/<int:pk>',views.ShowQuestion,name='ShowQuestion'),
    path('getanswer',views.getanswer,name='getanswer'),
    
]
