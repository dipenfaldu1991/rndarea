from django.shortcuts import render,redirect
from .models import JoobCatagery,JobsTypes,AddJobs,ApplyNow,jobsBookmark
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

## chat model
from chat.models import JobChat,JobPrivateChat,JobMessage
import json
import re
import random
from django.http import JsonResponse
from hashlib import md5
from django.core import serializers
from chat import utility_functions as chat_utility_functions
from django.db.models.query import QuerySet
from django.db.models import Count



# Create your views here.
from accounts.models import profile


def u_profileimg(request):
    user_img=''
    if request.user.is_authenticated:
        u = profile.objects.get(user_id=request.user)
        user_img=u.image
        print('user image====================',user_img)
    return user_img



def add_jobs(request):
    jobcategory=JoobCatagery.objects.all()
    jobtype = JobsTypes.objects.all()
    print('jobtype',jobtype)
    if request.method=='POST' and request.FILES:
        job_title=request.POST.get('jobtitle')
        job_type=request.POST.get('jobtype') 
        jobcategory=request.POST.get('jobcategory') 
        location =request.POST.get('location')
        salaryminm=request.POST.get('salaryminm') 
        salarymaxm =request.POST.get('salarymaxm')
        tag =request.POST.get('tag') 
        jobdescription=request.POST.get('jobdescription')
        docfile = request.FILES.get('docfile')
        print('add job')
        user_id=User.objects.get(username=request.user)
        adddata=AddJobs.objects.create(job_title=job_title,job_type_id=job_type,job_category_id=jobcategory,location=location,salaryminm=salaryminm,salarymaxm=salarymaxm,tags=tag,job_description=jobdescription,upload_documents=docfile,created_user_id=user_id.id,updated_user_id=user_id.id)

    return render(request,'dashboard-post-a-job.html',{'jobtype':jobtype,'jobcategory':jobcategory,'user_img':u_profileimg(request)})


def view_joblist(request):
    add_jobslist = AddJobs.objects.all()

    paginator = Paginator(add_jobslist,3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'jobs-list-layout-2.html',{'add_jobslist':add_jobslist,'page_obj':page_obj,'user_img':u_profileimg(request)})

def jobdetails_byid(request,id):
    show_jovdetails=AddJobs.objects.get(pk=id)
    job=show_jovdetails.id
    request.session["show_jovdetails"]=job
    request.session['id']=id  
    print("show_jovdetails+++++++++++++++++++++++++++++++++++++++++",show_jovdetails)
    return render(request,'single-job-page.html',{'show_jovdetails':show_jovdetails,'user_img':u_profileimg(request)})

def jobapply_now(request):
    show_jovdetails=request.session["show_jovdetails"]   
    print("show_jovdetails+++++++++++++++++++++++++++++++++++++++++",show_jovdetails)
    if request.method=='POST' and request.FILES:
        name=request.POST.get('name')
        email=request.POST.get('emailaddress')
        upload_doc=request.FILES.get('uploaddoc')
        contact_number=request.POST.get('contectno')
        user_id=User.objects.get(username=request.user)
        jobadddata=ApplyNow.objects.create(name=name,email=email,contact_number=contact_number,addjob_id_id=show_jovdetails,upload_doc=upload_doc,created_user_id=user_id.id)
        return redirect('jobs:jobdetails_byid',id=request.session['id'])
    return render(request,'single-job-page.html',{'user_img':u_profileimg(request)})


@login_required(login_url="/")  
def managejobs(request):
    show_jobs = AddJobs.objects.filter(created_user_id=request.user)
    show_jobs_id = AddJobs.objects.filter(created_user_id=request.user).values_list('id', flat=True)
    apply_count_dict={}
    for i in show_jobs_id:
        apply_count=ApplyNow.objects.filter(addjob_id_id=i).count()
        apply_count_dict[i]=apply_count
    paginator = Paginator(show_jobs,3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("=========================================",apply_count_dict)
    return render(request,'dashboard-manage-jobs.html',{'page_obj':page_obj,'apply_count_dict':apply_count_dict,'user_img':u_profileimg(request)})

@login_required(login_url="/")
def delete_jobs(request,pk2):   
    jobs=AddJobs.objects.get(id=pk2)
    jobs.delete()
    return redirect('jobs:managejobs',{'user_img':u_profileimg(request)})

 
@login_required(login_url="/")  
def managecandidates(request,mid):    
    apply_userids=ApplyNow.objects.filter(addjob_id_id=mid).values_list('created_user_id', flat=True)
    apply_data=ApplyNow.objects.filter(addjob_id_id=mid)
    j_type=AddJobs.objects.get(id=mid)
    print("j_type=========================================",j_type)

    userlist=[]
    apply_userlist={}
    request.session["mid"]=mid
    for i in apply_userids:       
        apply_user_name=User.objects.filter(pk=i).values_list('username', flat=True)
        count_user=ApplyNow.objects.filter(pk=i)
        userlist.append(count_user)            
        for j in apply_user_name:
            apply_userlist[i]=j
    u_data=len(userlist)
    print("count_user============",u_data)
    paginator = Paginator(apply_data,3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)                
    print("apply_count_dict=========================================",page_obj)
    return render(request,'dashboard-manage-candidates.html',{'u_data':u_data,'j_type':j_type,'apply_userlist':apply_userlist,'page_obj':page_obj,'user_img':u_profileimg(request)})


@login_required(login_url="/")
def delete_candidates(request,pk3):
    del_apply=ApplyNow.objects.get(id=pk3)
    del_apply.delete()
    return redirect('jobs:managecandidates',mid=request.session["mid"])


@login_required(login_url="/")
def edit_jobs(request,id): 
    edit_jobs=AddJobs.objects.get(id=id)
    if request.method=='POST':
        job_title=request.POST.get('jobtitle')
        job_type=request.POST.get('jobtype') 
        job_category=request.POST.get('jobcategory') 
        location =request.POST.get('location')
        salaryminm=request.POST.get('salaryminm') 
        salarymaxm =request.POST.get('salarymaxm')
        tag =request.POST.get('tag') 
        job_description=request.POST.get('jobdescription')
        upload_documents = request.FILES.get('docfile')        
        if upload_documents==None:
            upload_documents=edit_jobs.upload_documents      
        edit_jobs.job_title=job_title
        edit_jobs.job_type=job_type
        edit_jobs.job_category=job_category
        edit_jobs.location=location
        edit_jobs.salaryminm=salaryminm
        edit_jobs.tag=tag
        edit_jobs.salarymaxm=salarymaxm
        edit_jobs.job_description=job_description
        edit_jobs.upload_documents=upload_documents
        edit_jobs.save()
    return render(request,'edit_jobs.html',{'edit_jobs':edit_jobs,'user_img':u_profileimg(request)})


def jobbookmark(request):
    if request.method=='POST':
        jobid = request.POST.get('jobid_id')
        a=AddJobs.objects.get(id=jobid)
        jobsBookmark.objects.create(jobid=a,created_user_id_id=request.user.id,updated_user_id=request.user.id)       
        return render(request,'Upload_Project_2.html')
    return render(request,'Upload_Project.html',{'user_img':u_profileimg(request)})

def jobbookmarkdlt(request,pk6):
    a=jobsBookmark.objects.get(id=pk6)
    a.delete()
    # print('=============upload file2 ==photo=======================================',a)
    return redirect('accounts:dashboard-bookmark-manage')

@login_required
def createsss_chat(request,id):    
    other_user = User.objects.get(id=id)
    print('99999999999999999999999999999999999999',id)
    request.session["id"]=id
    private_chat = JobPrivateChat()
    new_chat = JobPrivateChat.add_this(private_chat, request.user, other_user)
    messages = JobMessage.objects.all().filter(chat=new_chat)
    return redirect('jobs:create_chat')
    return render(request, 'chat1.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages})



@login_required
def create_chat(request):    
    other_user = User.objects.get(id=request.session["id"])
    private_chat = JobPrivateChat()
    new_chat = JobPrivateChat.add_this(private_chat, request.user, other_user)
    messages = JobMessage.objects.all().filter(chat=new_chat)
    return render(request, 'chat1.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages})

@login_required
def send_message(request):
    chat_id = request.POST.get("id_chat")
    chat = JobChat.objects.get(id_chat=chat_id)
    print('chat_iddddddddddddddddddddddd',id)
    text_message = request.POST.get("text-message-input")
    regex = '^(\+\d{1,3})?,?\s?\d{8,13}' 
    regex1 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'       
    if len(text_message) > 0:
        if(re.search(regex,text_message)) or (re.search(regex1,text_message)) :  
            messaggio=JobMessage.add_this(JobMessage(), chat, request.user, text_message) 
        else:    
            messaggio=JobMessage.add_this(JobMessage(), chat, request.user, text_message)
    response = HttpResponse("200")
    return response

# recupera un messaggio dato il suo id
@login_required
def get_message_by_id(id):
    return JobMessage.objects.all().get(id=id)


@login_required
def private_chat(request):
    chat_id = request.POST.get("id_chat")
    
    print('chat_idddddddddddddddddddddd',chat_id)
    chat = JobPrivateChat.objects.get(id_chat=chat_id)
    messages = JobMessage.objects.all().filter(chat=chat)
    print('++++++++++++++===========================================',messages)
    if chat.participant1 == request.user:
        participant = chat.participant2
    else:
        participant = chat.participant1
    return render(request, 'chat1.html', {'user2': participant, 'id_chat': chat_id, 'messages': messages})




@login_required()
def chat_list(request):
    chat_list = chat_utility_functions.get_user_jobprivate_chats(request)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',chat_list)
    return render(request, 'private-chat-list1.html',
                  {'private_chats': chat_list, 'len_chats': len(chat_list)})




def get_json_chat_messages(request):    
    chat = JobChat.objects.get(id_chat=request.session["id"])
    messaggi_query = JobMessage.objects.filter(chat=chat)
    messaggi_json_array = []
    for messaggio in messaggi_query:
        msg = {'username': messaggio.sender.username, 'text': messaggio.text,
               'timestamp': messaggio.timestamp.strftime('%Y-%m-%d %H:%M')}
        messaggi_json_array.append(msg)
    return JsonResponse(messaggi_json_array, safe=False)

































































































