from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import profile
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone


# Create your models here.

class Projects_add(models.Model):
    headline=models.CharField(max_length=100)
    Description=models.TextField(max_length=1000)
    Technology=models.CharField(max_length=500)
    Documents=models.CharField(max_length=100)
    duration=models.CharField(max_length=100)
    Relevant_Project=models.CharField(max_length=100)
    Support=models.CharField(max_length=100)
    Cost=models.DecimalField(max_digits=30, decimal_places=15)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.PositiveIntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.PositiveIntegerField(blank=True,null=True)
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.headline
    
def get_upload_path(instance, filename):
    return 'documents/{0}/{1}'.format(instance.user.id ,filename)

class Projects_add_documents(models.Model):
    project_icon=models.FileField(upload_to='proje/')
    project_banner=models.FileField(upload_to='proje/')
    documentation=models.FileField(upload_to='proje/')
    intraction_document=models.FileField(upload_to='proje/')
    other_reports=models.FileField(upload_to='proje/')
    upload_video=models.FileField(upload_to='proje/')
    screenshort_1=models.FileField(upload_to='proje/')
    screenshort_2=models.FileField(upload_to='proje/')
    screenshort_3=models.FileField(upload_to='proje/')
    screenshort_4=models.FileField(upload_to='proje/')
    screenshort_5=models.FileField(upload_to='proje/')
    screenshort_6=models.FileField(upload_to='proje/')
    zip_file=models.FileField(upload_to='proje/',blank=True,null=True)
    project_add=models.PositiveIntegerField()
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createdocumentsuser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,related_name='updatedocumentsuser')
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    deleted_user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,related_name='deletedocumentsuser')
    deleted = models.DateTimeField(auto_now=True,blank=True,null=True)


class Questions(models.Model):
    title=models.CharField(max_length=10000)
    description=models.CharField(max_length=10000)
    technology=models.CharField(max_length=1000)
    skill=models.CharField(max_length=1000)
    screenshort=models.FileField(upload_to='proje/')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createquestionsuser')
    date_posted = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,related_name='updatquestionsuser')
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return str(self.created_user)

class Answer(models.Model):
    answer=models.CharField(max_length=500000)
    likes=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='comment_likes')
    parent = models.ForeignKey("self", null=True, blank="True",on_delete=models.CASCADE,related_name='parentsss')
    question_id=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='createquestionsid')
    question_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createquestionsuserid')
    created_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createuserid')  
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='updateuser',null="True")
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.answer)

    def children(self):
        return Answer.objects.filter(parent=self)

    def get_like_url(self):
        return reverse("accounts:like_toggle", kwargs={"answer_id": self.id}) 

    def get_like_instances(self):
        return self.likes.all()

    def get_user_object(self):
        return get_object_or_404(profile, user=self.created_user_id)

    def get_image_url(self):
        user_ = get_object_or_404(profile, user=self.created_user_id)
        return user_.image.url       

    
class AddPostdatas(models.Model):
    project_name=models.CharField(max_length=200)
    Category=models.CharField(max_length=200)
    Location =models.CharField(max_length=200)
    your_estimated_budget_minimum=models.CharField(max_length=200)
    your_estimated_budget_maximum=models.CharField(max_length=200)
    skills_are_required = models.CharField(max_length=200)
    Describe_Your_Post=models.TextField(max_length=20000) 
    upload_file=models.FileField (upload_to='proje/')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createdaddostsuser')
    date_posted = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True,related_name='updataddpostuser')
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    def __str__(self):
        return str(self.id)


class Bidding(models.Model):
    task_id=models.ForeignKey(AddPostdatas,on_delete=models.CASCADE,related_name='bid_task_id')
    proposal=models.TextField(max_length=3000,blank=True,null=True)
    add_files=models.FileField(upload_to='rnd_proje/',blank=True,null=True)
    bid_price=models.IntegerField()
    bid_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='biduser')
    create_bid_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    bid_type=models.CharField(max_length=200,null=True)
    delivery_time=models.IntegerField()
    update_time=models.DateTimeField(null=True)

class BidCount(models.Model):
    number_of_bid=models.IntegerField()
    user_id=models.IntegerField(unique=True,null=False)
    created_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(null=True)


class Plans(models.Model):
    plan_name=models.CharField(max_length=100)
    Description=models.TextField(max_length=2000)
    price=models.IntegerField()
    bid=models.IntegerField()
    features1=models.CharField(max_length=500)
    features2=models.CharField(max_length=500)
    othersfeatures3=models.CharField(max_length=500)


class Paytm_history(models.Model):
    user = models.ForeignKey(User, related_name='rel_payment_paytm', on_delete=models.CASCADE, null=True, default=None)
    ORDERID = models.CharField('ORDER ID', max_length=30)
    TXNDATE = models.DateTimeField('TXN DATE', default=timezone.now)
    TXNID = models.CharField('TXN ID', max_length=100)
    BANKTXNID = models.CharField('BANK TXN ID',max_length=100, null=True, blank=True)
    BANKNAME = models.CharField('BANK NAME', max_length=50, null=True, blank=True)
    RESPCODE = models.IntegerField('RESP CODE')
    PAYMENTMODE = models.CharField('PAYMENT MODE', max_length=10, null=True, blank=True)
    CURRENCY = models.CharField('CURRENCY', max_length=4, null=True, blank=True)
    GATEWAYNAME = models.CharField("GATEWAY NAME", max_length=30, null=True, blank=True)
    MID = models.CharField(max_length=40)
    RESPMSG = models.TextField('RESP MSG', max_length=250)
    TXNAMOUNT = models.FloatField('TXN AMOUNT')
    PLANPRICE=models.FloatField()
    GST=models.FloatField()
    STATUS = models.CharField('STATUS', max_length=12)

    # class Meta:
    #     app_label = 'paytm'

    def __str__(self):
        return '%s  (%s)' % (self.user.username ,self.pk)


    def __unicode__(self):
        return self.STATUS


    def __iter__(self):
        for field_name in [f.name for f in self._meta.get_fields()]:
            value = getattr(self, field_name, None)
            yield (field_name, value)
            

class AcceptBiddata(models.Model):
    taskid=models.ForeignKey(AddPostdatas,on_delete=models.CASCADE,related_name='task_id_id')
    task_userid=models.ForeignKey(User,on_delete=models.CASCADE,related_name='task_userid')
    bid_userid=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bid_userid')
    biddingid=models.IntegerField()
    status=models.CharField(max_length=300,default=0)
    created_datetime=models.DateTimeField(auto_now_add=True)



class LikePlans(models.Model):
    like_plan_name=models.CharField(max_length=100)
    like_description=models.TextField(max_length=2000)
    like_price=models.IntegerField()
    like=models.IntegerField()
    like_features1=models.CharField(max_length=500)
    like_features2=models.CharField(max_length=500)
    like_othersfeatures3=models.CharField(max_length=500)



class PaymentDetails(models.Model):
    payment_id=models.CharField(max_length=100)
    amount=models.FloatField()
    gst=models.FloatField()
    total=models.FloatField()
    payment_date=models.DateTimeField(auto_now_add=True)
    order_id=models.IntegerField()
    status=models.CharField(max_length=300)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='payment_user_id')
    created_time=models.DateTimeField(auto_now_add=True)
    back_name=models.CharField(max_length=200)
    back_txnid=models.CharField(max_length=200)
    payment_mode=models.CharField(max_length=200)

class Order(models.Model):
    plan_id=models.ForeignKey(Plans,on_delete=models.CASCADE,related_name='plan_user_id')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_user_id')
    plan_price=models.FloatField()
    gst=models.FloatField()
    total=models.FloatField()
    created_orde_time=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=300,default='pending')


class ProjectOrder(models.Model):
    plan_id=models.ForeignKey(Plans,on_delete=models.CASCADE,related_name='project_user_id')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='projectorder_user_id')
    plan_price=models.FloatField()
    gst=models.FloatField()
    total=models.FloatField()
    created_orde_time=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=300,default='pending')


class Wallet(models.Model):    
    money=models.DecimalField(max_digits=30, decimal_places=15,default=0)
    t_p_q_id=models.CharField(max_length=100)
    created_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cu')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='ur',null="True")
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(created_user_id=instance)

post_save.connect(create_user_profile, sender=User)        