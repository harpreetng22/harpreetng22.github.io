from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from django.conf import settings
from django.forms import ModelForm

class Listing(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    have=models.CharField(max_length=120)
    want=models.CharField(max_length=120)
    img=models.ImageField(upload_to="images/'",null=True)


    def __str__(self):
        return (f'{self.first_name}  Has:{self.have}  Want:{self.want}')
   
                 
     
class listing_form(ModelForm):
    class Meta:
        model = Listing
        fields = [ 'first_name', 'last_name', 'have', 'want', 'img']
        
        
        
class Request(models.Model):
    listing_id=models.ForeignKey(Listing,on_delete=models.CASCADE)
    requested_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    