from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
class Listing(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    have=models.CharField(max_length=120)
    want=models.CharField(max_length=120)
    img=models.ImageField(upload_to="static/",default='static/bookswap/book.svg')
    
    def __str__(self):
        return (f'{self.first_name}  Has:{self.have}  Want:{self.want}')  