import os
from PIL import Image
from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from sorl.thumbnail import ImageField, get_thumbnail

# Create your models here.
#jksdfhjksdfhsdjkf
class profile(models.Model):
    hourly_rate=models.PositiveIntegerField()
    skill=models.CharField(max_length=200)
    cover_letter=models.FileField(upload_to='cover_letter/', max_length=254)
    tagline=models.CharField(max_length=100)
    Nationality=models.CharField(max_length=30)
    image=models.ImageField(upload_to='profile_image/', max_length=254)
    introduce_yourself=models.TextField(max_length=1000)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("accounts:profile_detail")

    # def save(self, force_insert=False, force_update=False):
        
    #     super(profile, self).save(force_insert, force_update)

    #     if self.id is not None:
    #         previous = profile.objects.get(id=self.id)
    #         if self.image and self.image != previous.image:
    #             image = Image.open(self.image.path)
    #             image = image.resize((13, 15), Image.ANTIALIAS)
    #             image.save(self.image.path)
   


@receiver(models.signals.pre_save, sender=profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_cover_letter = sender.objects.get(pk=instance.pk).cover_letter 
    except sender.DoesNotExist:
        return False

    new_cover_letter = instance.cover_letter
    if not old_cover_letter == new_cover_letter or old_cover_letter == None:
        if os.path.isfile(old_cover_letter.path):
            os.remove(old_cover_letter.path)
                     
                     