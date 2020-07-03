from django.shortcuts import render,redirect
from django.views.generic import RedirectView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Projects_add,Projects_add_documents,Questions,Answer,Reply,Replyreply,Like,AddPostdatas,Bidding,BidCount,Plans
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url="/")   
def add_projects(request):
    if request.method=='POST':
        headline = request.POST.get('Project Headline')
        description = request.POST.get('Project Description')
        technology = request.POST.get('Used Technology')
        documents = request.POST.get('sd_txt')
        duration = request.POST.get('Time duration')
        relevant_project = request.POST.get('rp_txt')
        project_support = request.POST.get('Support')
        cost = request.POST.get('Project Cost')
        pro_add=Projects_add.objects.create(headline=headline,Description=description,Technology=technology,Documents=documents,duration=duration,Relevant_Project=relevant_project,Support=project_support,Cost=cost,created_user=request.user)
        pro_add.save()
        proj_add_id=Projects_add.objects.get(headline=headline,Description=description,Technology=technology,Documents=documents,duration=duration,Relevant_Project=relevant_project,Support=project_support,Cost=cost,created_user=request.user)
        request.session["priject_add_get"] =proj_add_id.id
        return redirect('rnd_projects:Upload_Project_2')
    return render(request,'Upload_Project.html')

@login_required(login_url="/")   
def Upload_Project_2(request):
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
        p_id=request.session["priject_add_get"]
        pro_doc=Projects_add_documents.objects.create(project_icon=icon,project_banner=project_banner,documentation=documentation,intraction_document=intraction_document,other_reports=other_reports,upload_video=upload_video,screenshort_1=screenshort_1,screenshort_2=screenshort_2,screenshort_3=screenshort_3,screenshort_4=screenshort_4,screenshort_5=screenshort_5,screenshort_6=screenshort_6,project_add=request.session["priject_add_get"],created_user=request.user)
        pro_doc.save()
    return render(request,'Upload_Project_2.html')


@login_required(login_url="/")   
def pages_blog_post(request):
    return render(request,'pages-blog-post.html')


@login_required(login_url="/")   
def pages_checkout_page(request):
    return render(request,'pages-checkout-page.html')


@login_required(login_url="/")   
def pages_invoice_template(request):
    return render(request,'pages-invoice-template.html')


@login_required(login_url="/")   
def pages_order_confirmation(request):
    return render(request,'pages-order-confirmation.html')



def ReadyProjectDetails(request,pk):
    posts = Projects_add.objects.get(pk=pk)
    proj=Projects_add_documents.objects.get(project_add=pk)
    return render(request,'ReadyProjectDetails.html',{'items': posts,'pro':proj})

 
def ReadyProjectShow(request):
    posts = Projects_add.objects.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request,'ReadyProjectShow.html',{'items': posts})
 

@login_required(login_url="/")     
def add_questions(request):
    if request.method=='POST' :
        title = request.POST.get('HeadLine')
        technology = request.POST.get('dropdown')
        description = request.POST.get('Description')
        skill = request.POST.get('skill')
        screenshort = request.FILES.get('Screenshort')
        que=Questions.objects.create(title=title,technology=technology,skill=skill,description=description,screenshort=screenshort,created_user=request.user)
        que.save()
        # return redirect('show_question_list')
    return render(request,'Add_Question.html')

@login_required(login_url="/")     
def show_question_list(request):
    que = Questions.objects.all()
    paginator = Paginator(que, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'show_question_list.html',{'items': que,'page_obj':page_obj})


@login_required(login_url="/")     
def ShowQuestion(request,pk):
    que1 = Questions.objects.all().order_by('date_posted')[:3]
    que = Questions.objects.get(pk=pk)
    ans1= Answer.objects.filter(question_id=que.id)
    reply1=Reply.objects.filter(question_id=que.id)
    reply2=Replyreply.objects.filter(question_id=que.id)
    str=que.skill
    l1 = str.split (",")
    print(l1)
    request.session["question_id"] =que.id
    
    # print(pk)
    return render(request,'ShowQuestion.html',{'question': que,'que1':que1,'ans1':ans1,'l1':l1,'reply1':reply1,'reply2':reply2})



@login_required(login_url="/")     
def getanswer(request):    
    que1 = Questions.objects.get(pk=int(request.session["question_id"]))
    que_id=que1.id
    que_create_user=que1.created_user_id
    if request.method=='POST' :
        answer = request.POST.get('answer')
        Answer.objects.create(answer=answer,question_id_id=que_id,question_user_id_id=que_create_user,created_user_id_id=request.user.id,
        updated_user_id=request.user.id)
        return redirect('rnd_projects:ShowQuestion',pk=que_id)
    return render(request,'ShowQuestion.html')
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required(login_url="/")
def like_post(request):
    que = Questions.objects.get(pk=request.session["question_id"])
    user = request.user
    a=que.id
    if request.method == "POST" and request.is_ajax():
        answer_id = request.POST.get('name')
        print(answer_id)
        answer = Answer.objects.get(pk=answer_id)

        # it means that the user like the post already so we gonna remve them if the user going to hit the like again
        if user in answer.liked.all():
            answer.liked.remove(user)
            # answer.liked.save()
        else:
            answer.liked.add(user)
            # answer.liked.save()
        
        like, created = Like.objects.get_or_create(user=user, answer_id=answer_id)
        
        if not created:
            if like.value == "Like":
                like.value = "Like"
            else:
                like.value = "Unlike"
        like.save()
        return redirect('rnd_projects:ShowQuestion',pk=a)





@login_required(login_url="/")     
def getreply(request):    
    que1 = Questions.objects.get(pk=int(request.session["question_id"]))
    que_id=que1.id
    que_create_user=que1.created_user_id
    if request.method=='POST' :
        replyreply = request.POST.get('replyreply')
        reply = request.POST.get('reply')
        
        if reply:
            answerid=request.POST.get('answer_id')        
            ans=Answer.objects.get(pk=answerid)
            print('ans to reply')
            Reply.objects.create(reply=reply,answer_id_id=ans.id,question_id_id=que_id,created_user_id_id=request.user.id,updated_user_id=request.user.id)
        if replyreply:
            que1 = Questions.objects.get(pk=int(request.session["question_id"]))
            que_id=que1.id
            que_create_user=que1.created_user_id
        
            replyid=request.POST.get('reply_id') 
            rel=Reply.objects.get(pk=replyid)
            print('reply to reply')
            Replyreply.objects.create(replyreply=replyreply,reply_id_id=rel.id,answer_id_id=rel.answer_id_id,question_id_id=que_id,created_user_id_id=request.user.id,updated_user_id=request.user.id)
        return redirect('rnd_projects:ShowQuestion',pk=que_id)
    return render(request,'ShowQuestion.html')


@login_required(login_url="/")     
def add_task(request):
    if request.method=='POST' and request.FILES:
        project_name = request.POST.get('projectname')
        Category = request.POST.get('category')
        Location = request.POST.get('location')
        your_estimated_budget_minimum = request.POST.get('your_estimated_budget_minimum')
        your_estimated_budget_maximum = request.POST.get('your_estimated_budget_maximum')
        skills_are_required = request.POST.get('skillsarerequired')
        Describe_Your_Post=request.POST.get('describeyourpost')
        upload_file=request.FILES.get('uploadfile')
        addpost=AddPostdatas.objects.create(project_name=project_name,Category=Category,Location=Location,your_estimated_budget_minimum=your_estimated_budget_minimum,your_estimated_budget_maximum=your_estimated_budget_maximum,skills_are_required=skills_are_required,Describe_Your_Post=Describe_Your_Post,upload_file=upload_file,created_user=request.user)
   
    return render(request,'addpost.html')

 

@login_required(login_url="/")     
def viewtask(request):
    viewpost=AddPostdatas.objects.all().order_by('-id') 
    l1=[]
    dic={}
    for i in viewpost:
        str=i.skills_are_required
        l=[]
        a=int(i.id)
        l2= str.split (",")
        for i in l2: 
            l.append(i)
        dic[a]=l
    # print(dic)
    paginator = Paginator(viewpost,5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'tasks_list_layout_2.html',{'viewpost':viewpost,'l1':dic,'page_obj':page_obj})


from django.contrib.auth.models import User
@login_required(login_url="/")  
def taskdetails(request,id):
    bidcount=BidCount.objects.get(user_id=request.user.id)
    count=bidcount.number_of_bid
    show_task=AddPostdatas.objects.get(pk=id)
    task_id=show_task.id
    request.session["taskid_bid"]=id
    str=show_task.skills_are_required
    l1 = str.split (",")
    # print(l1)
    return render(request,'single-task-page.html',{'show_task':show_task,'l1':l1,'count_bid':count})


@login_required(login_url="/")
def bidding(request):
    bidcount=BidCount.objects.get(user_id=request.user.id)
    count=bidcount.number_of_bid
    if request.method=='POST':
        bid_price = request.POST.get('minimaxirate')
        bid_type = request.POST.get('deliverydayhourstype')
        delivery_time = request.POST.get('qtyInput')
        biddingdata=Bidding.objects.create(task_id_id=request.session["taskid_bid"],bid_price=int(bid_price),bid_user_id_id=request.user.id,bid_type=bid_type,delivery_time=int(delivery_time)) 
        count=count-1
        bidcount.number_of_bid=count
        bidcount.save()
    
    return render(request,'single-task-page.html')

@login_required(login_url="/")
def buybid(request):
    plansdata=Plans.objects.all()
    print('test')
    print(plansdata)
    return render(request,'pages-pricing-plans.html',{'plansdata':plansdata})

@login_required(login_url="/")
def dashboard(request):
    return render(request,'dashboard.html')


@login_required(login_url="/")
def pagecheckout_bynow(request,mid):
    pagecheckout_data=Plans.objects.get(pk=mid)
    plan_id=pagecheckout_data.id
    plan_price=pagecheckout_data.price
    prices=plan_price
    gst=prices*18/100
    total=prices+gst
    print(total)
    return render(request,'pages-checkout-page.html',{'pagecheckout_data':pagecheckout_data,'gst':gst,'total':total})
