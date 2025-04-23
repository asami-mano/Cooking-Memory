from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User=get_user_model()

class CookingCategory(models.Model):
    user = models.ForeignKey(
        User,on_delete=models.PROTECT,
        related_name='cooking_categories'
    )
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CookingRecord(models.Model):
    EASINESS_CHOICES = [
        (0, '簡単'),
        (1, '普通'),
        (2, '手間がかかる'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cooking_category = models.ForeignKey('CookingCategory', on_delete=models.SET_NULL, null=True, blank=True)
    image_url = models.ImageField(upload_to='cooking_records/', blank=False, null=True)
    date = models.DateField()
    cooking_easiness = models.IntegerField(choices=EASINESS_CHOICES,default=1)
    is_favorite = models.IntegerField(default=0)#0:お気に入りではない,1:お気に入り
    memo = models.CharField(max_length=300,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} の料理記録"
    
