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
from rnd_projects.models import Projects_add,Questions
# Create your views here.

def ragister(request):
    questions_c=Questions.objects.all().count()
    poject_c=Projects_add.objects.all().count()
    alert = {
        'project_count':poject_c,
        'questions_count':questions_c,
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
            try:
                mail_subject = 'Activate your account.'
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                html_content = '<h1>This is an <strong>important</strong> message.</h1>'
                message = render_to_string('acc_active_email.html', {
                        'user': usr,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(usr.pk)),
                        'token':account_activation_token.make_token(usr),
                })
                to_email = usr.email
                from_email=settings.EMAIL_HOST_USER
                msg = EmailMultiAlternatives(mail_subject, message, from_email, to=[to_email])
                # email = EmailMessage(mail_subject, message, from_email,to=[to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                print('success')
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
def dashboard_settings(request):
    context={}
    user_p=profile.objects.filter(user=request.user).count()
    u=User.objects.get(username=request.user)
    if user_p==0:
        if request.method == "POST":
            image = request.FILES.get('user_image')
            first_name=request.POST.get('First_name')
            last_name=request.POST.get('Last_name')
            email=request.POST.get('Email')
            rate=request.POST.get('rate')
            cover = request.FILES.get('cover')
            tagline=request.POST.get('tagline')
            nationality=request.POST.get('Nationality')
            yourself=request.POST.get('Yourself')
            skill=request.POST.get('skill')
            profile.objects.create(hourly_rate=int(rate),skill=skill,cover_letter=cover,tagline=tagline,Nationality=nationality,image=image,introduce_yourself=yourself,user=request.user)
            u.first_name=first_name
            u.last_name=last_name
            u.save()
            return redirect('accounts:dashboard')
    else:
        pro=profile.objects.get(user=request.user)
        context['profile']=pro
        if request.method == "POST":
            image = request.FILES.get('user_image')
            first_name=request.POST.get('First_name')
            last_name=request.POST.get('Last_name')
            email=request.POST.get('Email')
            rate=request.POST.get('rate')
            cover = request.FILES.get('cover')
            tagline=request.POST.get('tagline')
            nationality=request.POST.get('Nationality')
            yourself=request.POST.get('Yourself')
            skill=request.POST.get('skill')
            if image==None:
                image=pro.image
            pro.hourly_rate=int(rate)
            pro.skill=skill
            pro.cover_letter=cover
            pro.tagline=tagline
            pro.Nationality=nationality
            pro.image=image
            pro.introduce_yourself=yourself
            pro.save()
            u.first_name=first_name
            u.last_name=last_name
            u.save()
            return redirect('accounts:dashboard_settings')
    return render(request,'dashboard-settings.html',context)

@login_required(login_url="/")    
def dashboard(request):
    return render(request,'dashboard.html')


