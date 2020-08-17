from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage,BadHeaderError,EmailMultiAlternatives
from django.http import HttpResponse,HttpResponseRedirect
from rndarea import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rnd_projects.models import Projects_add,Questions,Answer,AddPostdatas,BidCount,Projects_add_documents,LikePlans,Bidding
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.views.generic import RedirectView
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
##chat model
from chat.models import PrivateChat,Message,Chat,Warning
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



def profile_detail(request):
    que1 = Questions.objects.get(pk=int(request.session["question_id"]))
    que_id=que1.id
    que_create_user=que1.created_user_id
    profile_instance = get_object_or_404(profile, user=request.user)
    user_ = None
    if request.user.is_authenticated:
        user_ = get_object_or_404(profile, user=request.user)
    
    if request.method=='POST' :
        answer = request.POST.get('answer')
        parent = None
        new_comment = Answer.objects.create(
            answer=answer,
            parent=parent,
            question_id_id=que_id,
            question_user_id_id=que_create_user,
            created_user_id_id=request.user.id,
            updated_user_id=request.user.id
        )
        try:
            parent = int(request.POST.get("parent_id"))
        except:
            parent = None
        if (parent):
            new_comment.parent = Answer.objects.filter(id=parent).first()
            new_comment.save()

        return redirect('rnd_projects:ShowQuestion',pk=que_id)
   
    qs_comments = Answer.objects.filter(created_user_id=profile_instance.user,parent=None)
    content = {
        "profile":profile_instance,
        "user_": user_,
        "comments": qs_comments,
      
    }
    return redirect('rnd_projects:ShowQuestion',pk=que_id)
    return render(request, "ShowQuestion.html", content)



class CommentLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        answer_id = self.kwargs.get("answer_id")
        print (answer_id)
        answer_instance = get_object_or_404(Answer, id=answer_id)
        profile_instance = get_object_or_404(profile, user=answer_instance.created_user_id_id)
        url_ = profile_instance.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in answer_instance.likes.all():
                answer_instance.likes.remove(user)
            else:
                answer_instance.likes.add(user)
        else:
            return "/login"
        return url_


def ragister(request):
    que = Questions.objects.all()
    AddPostdatas_c=AddPostdatas.objects.all().count()
    questions_c=Questions.objects.all().count()
    poject_c=Projects_add.objects.all().count()
    like_plansdata=LikePlans.objects.all()
    
    chat_list=['']    
    if request.user.is_authenticated:
        chat_list = chat_utility_functions.get_user_private_chats(request) 
        print(chat_list[3])
    if request.user.is_authenticated:
        like_count=Answer.objects.filter(created_user_id_id=request.user.id).values_list('likes', flat=True)
        print(like_count)
        like_count=like_count.count()
        print(like_count)
    alert = {
        'project_count':poject_c,
        'questions_count':questions_c,
        'que':que,
        'AddPostdatas_count':AddPostdatas_c,
        'like_plansdata':like_plansdata,
        'private_chats': chat_list[0],
        'private_chatss':chat_list,
        'len_chats': len(chat_list),
    }
        
    if request.method=='POST':
        username=request.POST.get('username-register')
        email=request.POST.get('emailaddress-register')
        if User.objects.filter(username = request.POST['username-register']).exists():
            alert['message'] = "Username already exists"
        elif User.objects.filter(email = request.POST['emailaddress-register']).exists():
            alert['message'] = "email already exists"
        else:
            username=request.POST.get('username-register')
            email=request.POST.get('emailaddress-register')
            password=request.POST.get('password-register')
            usr=User.objects.create_user(username=username,email=email,is_active = False,password=password)
            userid=User.objects.get(email=email).pk
            a=userid
            print(type(a))
            abc=BidCount.objects.create(number_of_bid=10,user_id=a)
            print('successsssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            try:
                # mail_subject = 'Activate your account.'
                # current_site = get_current_site(request)
                # mail_subject = 'Activate your blog account.'
                # html_content = '<h1>This is an <strong>important</strong> message.</h1>'
                # message = render_to_string('acc_active_email.html', {
                #         'user': usr,
                #         'domain': current_site.domain,
                #         'uid':urlsafe_base64_encode(force_bytes(usr.pk)),
                #         'token':account_activation_token.make_token(usr),
                # })
                # to_email = usr.email
                # from_email=settings.EMAIL_HOST_USER
                # msg = EmailMultiAlternatives(mail_subject, message, from_email, to=[to_email])
                # # email = EmailMessage(mail_subject, message, from_email,to=[to_email])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                userid=User.objects.get(email=email).pk
                a=userid
                print(type(a))
                abc=BidCount.objects.create(number_of_bid=10,user_id=a)
                print('successsssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            except  BadHeaderError:
                print('erroe')
                ins=User.objects.get(email__exact=request.POST.get('emailaddress-register')).delete()
                print(ins)
                alert['message']="email not send"
            return redirect('accounts:register')
    return render(request,'index.html',alert)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('emailaddress')
        password = request.POST.get('password')
        username = get_user(email)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                warning=Warning.objects.filter(sender_id=request.user).values_list('chat_id', flat=True)
                ussss =Warning.objects.values('chat_id').annotate(warning_count=Count('chat_id')).filter(warning_count__gt=0)
                return redirect('accounts:register')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'index.html', {})

@login_required(login_url="/")
def user_logout(request):
    logout(request)
    return redirect('accounts:register')

@login_required(login_url="/")    
def dashboard(request):
    user_count = Questions.objects.filter(created_user_id=request.user).count()    
    return render(request,'dashboard.html',{'user_count':user_count})

@login_required(login_url="/")  
def show_list_dash(request):
    show_questions = Questions.objects.filter(created_user_id=request.user)
    paginator = Paginator(show_questions, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'show_list_dash.html',{'show_questions':show_questions,'page_obj':page_obj})




def count_data(request):
    user_count = Questions.objects.filter(created_user_id=request.user).count() 
    context={'user_count':user_count}
    request.session["pvr"] =user_count
    
    return render(request,'base2.html',context)


@login_required(login_url="/")    
def edit_questions(request,id):
    question=Questions.objects.get(id=id)
    
    if request.method=='POST':
        title = request.POST.get('HeadLine')
        technology = request.POST.get('dropdown')
        description = request.POST.get('Description')
        skill = request.POST.get('skill')
        screenshort = request.FILES.get('Screenshort')
        if screenshort==None:
            screenshort=question.screenshort  
        if technology==None:
            technology=question.technology     
        question.title=title
        question.technology=technology
        question.description=description
        question.skill=skill
        question.screenshort=screenshort
        question.save()
    return render(request,'edit_questions.html',{'question':question})   

@login_required(login_url="/")
def update_show_project(request):
    posts = Projects_add.objects.filter(created_user_id=request.user)
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request,'update_show_project.html',{'items': posts})     

@login_required(login_url="/") 
def edit_project(request,id):
    project = Projects_add.objects.get(id=id)
    request.session["Projects_add"]=project.id
    project_document1=project.Relevant_Project.split(',')
    project_document=project.Documents.split(',')
    project_document.pop()
    project_document1.pop()
    str=project.Support
    l2 = str.split (",")
    print(l2)
    proj_check1=['','','']
    print(project_document)
    proj_check=['','','']

    if 'Project Documents' in project_document:
        proj_check[0]='Project Documents'
    if 'Abstract Report' in project_document:
        proj_check[1]='Abstract Report'
    if 'Diagrame' in project_document:
        proj_check[2]='Diagrame' 

    if 'MCA' in project_document1:
        proj_check1[0]='MCA'
    if 'BCA' in project_document1:
        proj_check1[1]='BCA'
    if 'MScIT' in project_document1:
        proj_check1[2]='MScIT'    



    if request.method=='POST':
        headline = request.POST.get('Project Headline')
        Description = request.POST.get('Project Description')
        Technology = request.POST.get('Used Technology')
        doc = request.POST.get('sd_txt')
        duration = request.POST.get('Time duration')
        Relevant_Project = request.POST.get('rp_txt')
        Support = request.POST.get('Support')
        Cost = request.POST.get('Project Cost')
        print('---------------->',doc)
        print('==================>',Relevant_Project) 
        if doc==None:
            Documents=project.Documents 
            # print(Documents) 
        if Support==None:
            Support=project.Support 
        if Relevant_Project==None:
            Relevant_Project=project.Relevant_Project        
            # print(Relevant_Project)
        project.headline=headline
        project.Description=Description
        project.Technology=Technology
        project.Documents=doc
        project.duration=duration
        project.Relevant_Project=Relevant_Project
        project.Support=Support
        project.Cost=Cost
        project.save()
        return redirect('accounts:edit_project_file', id=project.id)
    return render(request,'edit_project.html',{'project':project,'pro':proj_check,'pro1':proj_check1,'l2':l2})

@login_required(login_url="/") 
def edit_project_file(request,id):
    project1 = Projects_add_documents.objects.get(project_add=int(request.session["Projects_add"]))
    if request.method=='POST':
        icon=request.FILES.get('project_icon')
        project_banner=request.FILES.get('project_banner')
        documentation=request.FILES.get('documentation')
        intraction_document=request.FILES.get('intraction_document')
        other_reports=request.FILES.get('other_reports')
        upload_video=request.FILES.get('upload_video')
        screenshort_1=request.FILES.get('screenshort_1')
        screenshort_2=request.FILES.get('screenshort_2')
        screenshort_3=request.FILES.get('screenshort_3')
        screenshort_4=request.FILES.get('screenshort_4')
        screenshort_5=request.FILES.get('screenshort_5')
        screenshort_6=request.FILES.get('screenshort_6')
        zip_file=request.FILES.get('zip_file')
        if icon==None:
            icon=project1.project_icon 
        if documentation==None:
            documentation=project1.documentation 
        if intraction_document==None:
            intraction_document=project1.intraction_document
        if project_banner==None:
            project_banner=project1.project_banner 
        if other_reports==None:
            other_reports=project1.other_reports 
        if upload_video==None:
            upload_video=project1.upload_video                  
        if screenshort_1==None:
            screenshort_1=project1.screenshort_1 
        if screenshort_2==None:
            screenshort_2=project1.screenshort_2 
        if screenshort_3==None:
            screenshort_3=project1.screenshort_3 
        if screenshort_4==None:
            screenshort_4=project1.screenshort_4 
        if screenshort_5==None:
            screenshort_5=project1.screenshort_5
        if screenshort_6==None:
            screenshort_6=project1.screenshort_6
        if zip_file==None:
            zip_file=project1.zip_file                         
        project1.project_icon=icon    
        project1.project_banner=project_banner
        project1.documentation=documentation
        project1.intraction_document=intraction_document
        project1.other_reports=other_reports
        project1.upload_video=upload_video
        project1.screenshort_1=screenshort_1
        project1.screenshort_2=screenshort_2
        project1.screenshort_3=screenshort_3
        project1.screenshort_4=screenshort_4
        project1.screenshort_5=screenshort_5
        project1.screenshort_6=screenshort_6
        project1.zip_file=zip_file
        project1.save()
    return render(request,'edit_project_file.html',{'project1':project1})


@login_required(login_url="/")  
def show_task(request): 
    show_task = AddPostdatas.objects.filter(created_user_id=request.user)
    show_task_id = AddPostdatas.objects.filter(created_user_id=request.user).values_list('id', flat=True)
    
    print("show_task",show_task)
    print("show_task_id",show_task_id)

    bid_count_dict={}
    for i in show_task_id:
        bid_count=Bidding.objects.filter(task_id_id=i).count()
        bid_count_dict[i]=bid_count
        bididss=Bidding.objects.filter(task_id_id=i) 

    # print("bid_count_dict",bid_count_dict)
    # print("bid_idsssss",bididss)
    # print("bid_count",bid_count)
    # print('=============upload file2 ==photo=======================================')

    addprice={}
    for i in show_task_id:
        # print(i)     
        bidid=Bidding.objects.filter(task_id=i).values_list('bid_price', flat=True)
        print("bidid----price ===========================",bidid)
        sum=0
        average_of_price=0
        for s in bidid:
            sum=sum+s
        totalelen=len(bidid)
        if(totalelen != 0):
            average_of_price=sum/totalelen
        else:
            average_of_price=0
        addprice[i]=average_of_price

    paginator = Paginator(show_task,2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("addprice",addprice)

    return render(request,'dashboard-manage-tasks.html',{'show_task':show_task,'page_obj':page_obj,'bid_count_dict':bid_count_dict,'average_of_price':addprice})


def managebidders(request,mid):
    bid_userids=Bidding.objects.filter(task_id_id=mid).values_list('bid_user_id_id', flat=True)
    bid_data=Bidding.objects.filter(task_id_id=mid)
    bid_userlist={}
        
    for i in bid_userids:
        
        bid_user_name=User.objects.filter(pk=i).values_list('username', flat=True)
        print(bid_user_name)        
        for j in bid_user_name:
            bid_userlist[i]=j
                       
    print(bid_userlist)

    return render(request,'dashboard-manage-bidders.html',{'bid_userlist':bid_userlist,'bid_data':bid_data})

@login_required
def createsss_chat(request,id):    
    other_user = User.objects.get(id=id)
    request.session["id"]=id
    private_chat = PrivateChat()
    new_chat = PrivateChat.add_this(private_chat, request.user, other_user)
    messages = Message.objects.all().filter(chat=new_chat)
    return redirect('accounts:create_chat')
    return render(request, 'chat.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages})



@login_required
def create_chat(request):    
    other_user = User.objects.get(id=request.session["id"])
    private_chat = PrivateChat()
    new_chat = PrivateChat.add_this(private_chat, request.user, other_user)
    messages = Message.objects.all().filter(chat=new_chat)
    return render(request, 'chat.html', {'user2': other_user, 'id_chat': new_chat.id_chat, 'messages': messages})

@login_required
def send_message(request):
    chat_id = request.POST.get("id_chat")
    chat = Chat.objects.get(id_chat=chat_id)
    text_message = request.POST.get("text-message-input")
    regex = '^(\+\d{1,3})?,?\s?\d{8,13}' 
    regex1 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'       
    if len(text_message) > 0:
        if(re.search(regex,text_message)) or (re.search(regex1,text_message)) :  
            messaggio=Message.add_this(Message(), chat, request.user, text_message)
            mes=Warning.add_this(Warning(), chat, request.user, text_message)
            print("********************************************************************not store")  
        else:    
            messaggio=Message.add_this(Message(), chat, request.user, text_message)
    response = HttpResponse("200")
    return response

# recupera un messaggio dato il suo id
@login_required
def get_message_by_id(id):
    return Message.objects.all().get(id=id)


@login_required
def private_chat(request):
    chat_id = request.POST.get("id_chat")
    chat = PrivateChat.objects.get(id_chat=chat_id)
    messages = Message.objects.all().filter(chat=chat)
    print('++++++++++++++===========================================',messages)
    if chat.participant1 == request.user:
        participant = chat.participant2
    else:
        participant = chat.participant1
    return render(request, 'chat.html', {'user2': participant, 'id_chat': chat_id, 'messages': messages})




@login_required()
def chat_list(request):
    chat_list = chat_utility_functions.get_user_private_chats(request)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',chat_list)
    return render(request, 'private-chat-list.html',
                  {'private_chats': chat_list, 'len_chats': len(chat_list)})




def get_json_chat_messages(request):    
    chat = Chat.objects.get(id_chat=request.session["id"])
    messaggi_query = Message.objects.filter(chat=chat)
    messaggi_json_array = []
    for messaggio in messaggi_query:
        msg = {'username': messaggio.sender.username, 'text': messaggio.text,
               'timestamp': messaggio.timestamp.strftime('%Y-%m-%d %H:%M')}
        messaggi_json_array.append(msg)
    return JsonResponse(messaggi_json_array, safe=False)

def acceptbids(request,pk):
    print(pk)
    if request.method=='POST':
        biddingid=Bidding.objects.get(id=pk)
        request.session["id"]=pk
        print(pk)
        taskuid=AddPostdatas.objects.get(id=biddingid.task_id_id)
        print('=============upload file2 ==photo=======================================',taskuid)
        taskuser=User.objects.get(id=taskuid.created_user_id)
        AcceptBiddata.objects.create(taskid=taskuid,task_userid=taskuser,bid_userid=User.objects.get(id=biddingid.bid_user_id_id),biddingid=biddingid.id,created_datetime=request.user) 
        
    return render(request,'dashboard-manage-bidders.html')


@login_required(login_url="/")
def edit_task(request,id): 
    edit_task=AddPostdatas.objects.get(id=id)
    if request.method=='POST':
        project_name = request.POST.get('projectname')
        Category = request.POST.get('category')
        Location = request.POST.get('location')
        your_estimated_budget_minimum = request.POST.get('your_estimated_budget_minimum')
        your_estimated_budget_maximum = request.POST.get('your_estimated_budget_maximum')
        skills_are_required = request.POST.get('skillsarerequired')
        Describe_Your_Post=request.POST.get('describeyourpost')
        upload_file=request.FILES.get('uploadfile')
        if upload_file==None:
            upload_file=edit_task.upload_file      
        edit_task.project_name=project_name
        edit_task.Category=Category
        edit_task.Location=Location
        edit_task.your_estimated_budget_minimum=your_estimated_budget_minimum
        edit_task.your_estimated_budget_maximum=your_estimated_budget_maximum
        edit_task.skills_are_required=skills_are_required
        edit_task.Describe_Your_Post=Describe_Your_Post
        edit_task.upload_file=upload_file
        edit_task.save()
    return render(request,'edit_task.html',{'edit_task':edit_task})

# def edit_project(request):
#     return render(request,'edit_project.html')

@login_required(login_url="/")    
def dashboard_settings(request):
    context={}
    user_count = Questions.objects.filter(created_user_id=request.user).count() 
    user_p=profile.objects.filter(user=request.user).count()
    u=User.objects.get(username=request.user)
    if user_p==0:
        if request.method == "POST" and request.FILES:
            image = request.FILES.get('image')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('Last_name')
            email=request.POST.get('email')
            rate=request.POST.get('rate')
            cover_letter=request.FILES.get('cover_letter')
            tagline=request.POST.get('tagline')
            Nationality=request.POST.get('dropdown1')
            introduce_yourself=request.POST.get('introduce_yourself')
            skill=request.POST.get('skill')
            profile.objects.create(hourly_rate=int(rate),skill=skill,cover_letter=cover_letter,tagline=tagline,Nationality=Nationality,image=image,introduce_yourself=introduce_yourself,user=request.user)
            u.first_name=first_name
            u.last_name=last_name
            u.save()
            return redirect('accounts:dashboard')
    else:
        pro=profile.objects.get(user=request.user)
        context['profile']=pro
        if request.method == "POST":
            image = request.FILES.get('image')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('Last_name')
            email=request.POST.get('email')
            rate=request.POST.get('rate')
            cover_letter=request.FILES.get('cover_letter')
            tagline=request.POST.get('tagline')
            Nationality=request.POST.get('dropdown1')
            introduce_yourself=request.POST.get('introduce_yourself')
            skill=request.POST.get('skill')
            if image==None:
                image=pro.image 
            if cover_letter==None:
                cover_letter=pro.cover_letter        
            pro.rate=int(rate)
            pro.skill=skill
            pro.cover_letter=cover_letter
            pro.tagline=tagline
            pro.Nationality=Nationality
            pro.image=image
            pro.introduce_yourself=introduce_yourself
            pro.save()
            u.first_name=first_name
            u.last_name=last_name
            u.email=email
            u.save()
            
            return redirect('accounts:dashboard_settings')
    return render(request,'dashboard_settings.html',context)

