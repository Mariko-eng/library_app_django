from django.db import models
from users.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('title',)
    
    def __str__(self):
        return self.title


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (("BOOKS","BOOKS"),("FILES","FILES"),("WEB LINKS","WEB LINKS"),)

    product_type = models.CharField(max_length=100,choices=PRODUCT_TYPE_CHOICES)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to='images',null=True) 
    file = models.FileField(upload_to='files',null=True)
    link = models.URLField(null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    slug = models.SlugField(null=True,blank=True)
    page_count = models.IntegerField(default=0,blank=True)
    featured = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    viewed_bY = models.ManyToManyField(User,related_name="book_views")
    liked_bY = models.ManyToManyField(User,related_name="book_likes")
    updated_bY = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="product_updates")
    created_bY = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Product"
        verbose_name_plural = "Products"




