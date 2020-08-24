from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class JobsTypes(models.Model):
    job_name=models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createdjobtype')
    updated_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='updatedjobtype')
    updated_date= models.DateTimeField(auto_now_add=True)
   
class JoobCatagery(models.Model):
    job_category=models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='createdcatagery')
    updated_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='updatedcatagery')
    updated_date= models.DateTimeField(auto_now_add=True)
    
class AddJobs(models.Model):
    job_title=models.CharField(max_length=200)
    job_type=models.ForeignKey(JobsTypes,on_delete=models.CASCADE,related_name='addjob')
    job_category=models.ForeignKey(JoobCatagery,on_delete=models.CASCADE,related_name='jobcatagery')
    location=models.CharField(max_length=200)
    salaryminm=models.IntegerField()
    salarymaxm=models.IntegerField()
    tags =models.CharField(max_length=200)
    job_description =models.TextField(max_length=200)
    upload_documents  =models.FileField(upload_to='jobfiles/')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_user')
    updated_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='updated_user')
    updated_date= models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.job_type)


class ApplyNow(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    contact_number=models.EmailField(max_length=200)
    upload_doc=models.FileField(upload_to='jobfiles/')
    addjob_id=models.ForeignKey(AddJobs,on_delete=models.CASCADE,related_name='jobcategory')
    created_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_users')
    created_date = models.DateTimeField(auto_now_add=True)


class jobsBookmark(models.Model):
    jobid=models.ForeignKey(AddJobs,on_delete=models.CASCADE,related_name='fg')
    created_user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='ggg')
    created = models.DateTimeField(auto_now_add=True)
    updated_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='ffff',null="True")
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    
