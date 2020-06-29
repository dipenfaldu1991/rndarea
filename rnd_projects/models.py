from django.db import models
import datetime
from django.contrib.auth.models import User
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
    question_id=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='createquestionsid')
    question_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createquestionsuserid')
    created_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createuserid')  
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='updateuser',null="True")
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)

class Like(models.Model):
    number_of_like=models.IntegerField()
    answer_id=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='answerlikeid')


class Reply(models.Model):
    reply=models.CharField(max_length=10000)
    answer_id=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='answerssssid')
    question_id=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='createquestionssid')
    created_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createddduser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='updateedduser',null="True")
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


class Replyreply(models.Model):
    replyreply=models.CharField(max_length=500000)
    reply_id=models.ForeignKey(Reply,on_delete=models.CASCADE,related_name='replyyyyyssssid')
    answer_id=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='answerssssssssid')
    question_id=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='createquestionssssid')
    created_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createdddddduser')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='updateeddddduser',null="True")
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)


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
    bid_price=models.IntegerField()
    bid_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='biduser')
    create_bid_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    bid_type=models.CharField(max_length=200)
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