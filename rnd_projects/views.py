from django.shortcuts import render,redirect
from .models import Projects_add,Projects_add_documents,Questions
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
        # print(title,technology,description,skill,screenshort)
    return render(request,'Add_Question.html')

@login_required(login_url="/")     
def show_question_list(request):
    # que = Questions.objects.get(id=myid)
    # print(myid)
    que = Questions.objects.all()
    return render(request,'show_question_list.html',{'items': que})


@login_required(login_url="/")     
def ShowQuestion(request,pk):
    que = Questions.objects.get(pk=pk)
    print(pk)
    # que = Questions.objects.all()
    return render(request,'ShowQuestion.html',{'question': que})
