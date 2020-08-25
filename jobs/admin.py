from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from .models import  JobsTypes,JoobCatagery,AddJobs
# Register your models here.

admin.site.register(JobsTypes)
admin.site.register(JoobCatagery)
admin.site.register(AddJobs)