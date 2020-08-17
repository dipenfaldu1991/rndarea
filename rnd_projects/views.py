from django.shortcuts import render,redirect
from django.views.generic import RedirectView
from django.views.decorators.http import require_POST
from .models import Projects_add,Projects_add_documents,Questions,Answer,LikePlans,AddPostdatas,Bidding,BidCount,Plans,Paytm_history,Order,ProjectOrder
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import profile
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rndarea import settings
from .paytm import Checksum
MERCHANT_KEY='dRqXXn5!k6v&EA6f'
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse
import json
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)



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
        return redirect('rnd_projects:ReadyProjectShow')
    return render(request,'Upload_Project_2.html')




def ReadyProjectDetails(request,pk):
    posts = Projects_add.objects.get(pk=pk)
    proj=Projects_add_documents.objects.get(project_add=pk)
    return render(request,'ReadyProjectDetails.html',{'items': posts,'pro':proj})

 
def ReadyProjectShow(request):
    posts = Projects_add.objects.all().order_by('-id')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request,'ReadyProjectShow.html',{'items': posts})
 
@login_required(login_url="/")
def project_pagecheckout_bynow(request,pid):
    posts = Projects_add.objects.get(pk=pk)
    project_id=posts.id
    print("===============================")
    print(project_id)
    plans_prices=posts.Cost
    print("===============================")
    print(plans_prices)
    pricess=plans_prices
    gsts=pricess*18/100
    totals=gsts+pricess
    request.session["plan_price"] =pricess
    request.session["plan_gst"] =gsts
    request.session["plan_total_price"] =totals
    return render(request,'projectpage-checkout-page.html',{'posts': posts,'pricess':pricess,'gsts':gsts,'totals':totals})

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
        return redirect('rnd_projects:show_question_list')
    return render(request,'Add_Question.html')


@login_required(login_url="/")     
def show_question_list(request):
    que = Questions.objects.all().order_by('-id')
    paginator = Paginator(que, 3) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'show_question_list.html',{'items': que,'page_obj':page_obj})


@login_required(login_url="/")     
def ShowQuestion(request,pk):
    que1 = Questions.objects.all().order_by('date_posted')[:3]
    que = Questions.objects.get(pk=pk)
    ans1= Answer.objects.filter(question_id=que.id,parent=None) 
    str=que.skill
    l1 = str.split (",")
    print(l1)
    request.session["question_id"] =que.id
    
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

    return render(request,'ShowQuestion.html', content)



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
        return redirect('rnd_projects:viewtask')
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
    print(type(bidcount.id))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++hellothis is user id++++++++++++++++++++++++++++++++++++++++++++++++++")
  
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
    Bid_user_id=int(request.user.id)
    count=bidcount.number_of_bid
    task_user=AddPostdatas.objects.get(id=request.session["taskid_bid"])
    
    upload_img=[]
    simsge=''
    if request.method=='POST' and request.FILES:
        bid_price = request.POST.get('minimaxirate')
        bid_type = request.POST.get('deliverydayhourstype')
        delivery_time = request.POST.get('qtyInput')
        proposaleyourpost=request.POST.get('proposaleyourpost') 
        upload_file=request.FILES.getlist('uploadfiles') 
        for file in upload_file:
            upload_img.append(str(file))
            img = ','.join(upload_img)
            print(img)
  

    Bidding.objects.create(task_id_id=request.session["taskid_bid"],proposal=proposaleyourpost,add_files=img,bid_price=int(bid_price),bid_user_id_id=request.user.id,bid_type=bid_type,delivery_time=delivery_time) 
    count=count-1
    bidcount.number_of_bid=count
    bidcount.save()
    return render(request,'single-task-page.html')






@login_required(login_url="/")
def buybid(request):
    plansdata=Plans.objects.all()
    return render(request,'pages-pricing-plans.html',{'plansdata':plansdata})



@login_required(login_url="/")
def pagecheckout_bynow(request,mid):
    pagecheckout_data=Plans.objects.get(pk=mid)
    plan_id=pagecheckout_data.id
    plan_price=pagecheckout_data.price
    prices=plan_price
    gst=prices*18/100
    total=prices+gst
    request.session["plan_price"]=prices
    request.session["plan_gst"] =gst
    request.session["plan_total_price"] =total
    return render(request,'pages-checkout-page.html',{'pagecheckout_data':pagecheckout_data,'gst':gst,'total':total})




@login_required
def payments_home(request):
    user = request.user
    status = False
    trns = 0
    bill_amount = request.session["plan_price"]
    gst=request.session["plan_gst"] 
    total_amount = request.session["plan_total_price"]
    if Paytm_history.objects.filter(user=user, STATUS = 'TXN_SUCCESS'):
        trns = Paytm_history.objects.filter(user=user, STATUS = 'TXN_SUCCESS')[0]
        status = True

        total_amount = total_amount

    return render(request, 'payments/payments_home.html', {'title': 'Payments', 'status': status, 'trns': trns, 'bill_amount': bill_amount, 'total_amount': total_amount,'gst':gst})

@login_required
@ensure_csrf_cookie
def paytm(request):
    user = request.user
    print(type(user.id))
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++hellothis is user id++++++++++++++++++++++++++++++++++++++++++++++++++")
  
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.HOST_URL + settings.PAYTM_CALLBACK_URL+'/'
    P_URL = 'https://securegw-stage.paytm.in/theia/processTransaction'
    CUST_ID = user.email
    order_id = Checksum.__id_generator__()

    bill_amount = request.session["plan_total_price"]
    


    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': str(bill_amount),
                    'CUST_ID': CUST_ID,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':'http://localhost:5555/rnd_projects/response',
                }
        param_dict = data_dict
        
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        return render(request,"payments/paytm.html",{'paytmdict':param_dict, 'user': user, 'paytmurl' :P_URL, 'title': 'Paytm'})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")

@csrf_exempt
def recipt(request):
    if request.method == "POST":
        user=request.user
        data_dict = {}
        
        data_dict = dict(request.POST.items())
        data_dict['PLANPRICE']=request.session["plan_price"]
        data_dict['GST']=request.session["plan_gst"]
        print(data_dict)

        Paytm_history.objects.create(user=request.user, **data_dict)

    status = 'TXN_FAILURE'
    
    for key,value in data_dict.items():
        if key == 'STATUS':
            # user.user_details.status = value
            # user.user_details.save()
            # if value == 'TXN_SUCCESS':
            status = value

    return render(request, "payments/pages-invoice-template.html", {"paytmr": data_dict, 'title': 'Recipt', "status": status})



@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        data_dict = dict(request.POST.items())

        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            for key in request.POST:
                if key == "BANKTXNID" or key == "RESPCODE":
                    if request.POST[key]:
                        data_dict[key] = int(request.POST[key])
                    else:
                        data_dict[key] = 0
                elif key == "TXNAMOUNT":
                    data_dict[key] = float(request.POST[key])
            # Paytm_history.objects.create(user=settings.USER, **data_dict)
            return render(request, "payments/response.html", {"paytm":data_dict, 'title': 'Confirm'})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)





@login_required(login_url="/")
def buylike(request):
    like_plansdata=LikePlans.objects.all()
    return render(request,'like-pricing-plans.html',{'like_plansdata':like_plansdata})



























