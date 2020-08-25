from django.shortcuts import render,redirect
from .models import JoobCatagery,JobsTypes,AddJobs,ApplyNow
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
# Create your views here.

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

    return render(request,'dashboard-post-a-job.html',{'jobtype':jobtype,'jobcategory':jobcategory})


def view_joblist(request):
    add_jobslist = AddJobs.objects.all()

    paginator = Paginator(add_jobslist,3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'jobs-list-layout-2.html',{'add_jobslist':add_jobslist,'page_obj':page_obj})

def jobdetails_byid(request,id):
    show_jovdetails=AddJobs.objects.get(pk=id)
    job=show_jovdetails.id
    request.session["show_jovdetails"]=job
    request.session['id']=id  
    print("show_jovdetails+++++++++++++++++++++++++++++++++++++++++",show_jovdetails)
    return render(request,'single-job-page.html',{'show_jovdetails':show_jovdetails})

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
    return render(request,'single-job-page.html')


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
    return render(request,'dashboard-manage-jobs.html',{'page_obj':page_obj,'apply_count_dict':apply_count_dict})

@login_required(login_url="/")
def delete_jobs(request,pk2):   
    jobs=AddJobs.objects.get(id=pk2)
    jobs.delete()
    return redirect('jobs:managejobs')

 
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
    return render(request,'dashboard-manage-candidates.html',{'u_data':u_data,'j_type':j_type,'apply_userlist':apply_userlist,'page_obj':page_obj})


@login_required(login_url="/")
def delete_candidates(request,pk3):
    del_apply=ApplyNow.objects.get(id=pk3)
    del_apply.delete()
    return redirect('jobs:managecandidates',mid=request.session["mid"])

































































































