from django.shortcuts import render,redirect
from django.views.generic import RedirectView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Projects_add,Projects_add_documents,Questions,Answer,AddPostdatas,Bidding,BidCount,Plans
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .paytm import Checksum
MERCHANT_KEY='dRqXXn5!k6v&EA6f'
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def paymentpage(request):
    return render(request,'pages-invoice-template.html')

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
        zip_file=request.FILES.get('zip_file')
        p_id=request.session["priject_add_get"]
        pro_doc=Projects_add_documents.objects.create(project_icon=icon,project_banner=project_banner,documentation=documentation,intraction_document=intraction_document,other_reports=other_reports,upload_video=upload_video,screenshort_1=screenshort_1,screenshort_2=screenshort_2,screenshort_3=screenshort_3,screenshort_4=screenshort_4,screenshort_5=screenshort_5,screenshort_6=screenshort_6,project_add=request.session["priject_add_get"],created_user=request.user,zip_file=zip_file)
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
def project_pagecheckout_bynow(request,pid):
    projectcheckout_data=Plans.objects.get(pk=pid)
    plan_id=projectcheckout_data.id
    plan_price=projectcheckout_data.price
    prices=plan_price
    gst=prices*18/100
    total=prices+gst
    request.session["plan_price"] =prices
    request.session["plan_gst"] =gst
    request.session["plan_total_price"] =total
    return render(request,'projectpage-checkout-page.html',{'projectcheckout_data':projectcheckout_data,'gst':gst,'total':total})

def project_order_plan(request):
    pass

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
    
    str=que.skill
    l1 = str.split (",")
    # print(l1)
    request.session["question_id"] =que.id
    
    # print(pk)
    return render(request,'ShowQuestion.html',{'question': que,'que1':que1,'ans1':ans1,'l1':l1})



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
def pagecheckout_bynow(request,mid):
    pagecheckout_data=Plans.objects.get(pk=mid)
    plan_id=pagecheckout_data.id
    plan_price=pagecheckout_data.price
    prices=plan_price
    gst=prices*18/100
    total=prices+gst
    print(total)
    return render(request,'pages-checkout-page.html',{'pagecheckout_data':pagecheckout_data,'gst':gst,'total':total})


@login_required(login_url="/")
def order_plan(request,mids):   
    plan_id=Plans.objects.get(pk=mids)
    user_id=request.user.id
    email=request.user.email

    request.session["users_id"] =user_id
    plan_price=request.session["plan_price"]
    gst=request.session["plan_gst"]
    total=request.session["plan_total_price"]

    orderdata=Order.objects.create(plan_price=request.session["plan_price"],gst=request.session["plan_gst"],total=request.session["plan_total_price"],user_id_id=request.user.id,plan_id_id=plan_id.id)
    orderdata.save()
    id=orderdata.id
    print(id)
    param_dict={
                'MID': 'fTOzOj03592353839843',
                'ORDER_ID': str(id),
                'TXN_AMOUNT': str(total),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/rnd_projects/handlerequest',
        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request,'paytm.html', {'param_dict':param_dict})

    return render(request,'single-task-page.html')



# paytm hendeler code
@csrf_exempt
def handlerequest(request):
    form=request.POST
    responce_dict={}
    for i in form.keys():
        responce_dict[i]=form[i]
        if i =='CHECKSUMHASH':
            checksum=form[i]
            print(checksum,end='\n')
    varify=Checksum.verify_checksum(responce_dict,MERCHANT_KEY,checksum)
    if varify:
        if responce_dict['RESPCODE']=='01':
            print('order successfull')
        else:
            print('order was not successfull because' + responce_dict['RESPMSG'])
    ord1=Order.objects.get(id=responce_dict['ORDERID'])
    user_id=User.objects.get(id=ord1.user_id_id)
    plan_price=ord1.plan_price
    gst=ord1.gst  
    PaymentDetails.objects.create(amount=plan_price,gst=gst,payment_id=responce_dict['TXNID'],total=responce_dict['TXNAMOUNT'],payment_date=responce_dict['TXNDATE'],order_id=responce_dict['ORDERID'],status=responce_dict['STATUS'],user_id=user_id,back_name=responce_dict['BANKNAME'],back_txnid=responce_dict['BANKTXNID'],payment_mode=responce_dict['PAYMENTMODE'])
    return render(request,'pages-order-confirmation.html',{'responce':responce_dict,'paymentdetail':paymentdetail})

@login_required(login_url="/")
def paymentdetail(request):
    getpamentdetail=PaymentDetails.objects.get(id=1)
    oderdata=Order.objects.get(id=getpamentdetail.order_id)
    planname=Plans.objects.get(id=oderdata.plan_id_id)
    pal_name=planname.plan_name
    uname=getpamentdetail.user_id
    firstname =uname.first_name
    lastname =uname.last_name
    email =uname.email
    return render(request,'pages-invoice-template.html',{'getpamentdetail':getpamentdetail,'pal_name':pal_name,'firstname':firstname,'lastname':lastname,'email':email })

