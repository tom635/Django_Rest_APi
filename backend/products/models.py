from django.db import models
from django.conf import settings
from django.db.models import Q
import random
# Create your models here.
user=settings.AUTH_USER_MODEL
TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'cameras']
class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)
    def search(self,query,user=None):
        look_up=(Q(title__icontains=query)| Q(content__icontains=query))
        qs=self.is_public().filter(look_up)
        if user is not None:
            qs2=self.filter(user=user).filter(look_up)
            qs=(qs|qs2).distinct()
        return qs

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    def search(self,query,user=None):
        return self.get_queryset().is_public().search(query,user=user)
 
       
class Product(models.Model):
    user=models.ForeignKey(user,on_delete=models.SET_NULL,null=True,default=1)
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99,null=True)
    public=models.BooleanField(default=True)
    
    objects=ProductManager()
    @property
    def sale_price(self):
        return "%.2f" %(float(self.price)*0.8)
    
    def get_discount(self):
        return "122"
    
    def is_public(self)->bool:
        return self.public

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]