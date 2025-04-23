from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import datetime

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
    cooking_category = models.ForeignKey('CookingCategory', on_delete=models.SET_NULL, null=True, blank=True,verbose_name='カテゴリ')
    image_url = models.ImageField(upload_to='cooking_records/', blank=False, null=True)
    date = models.DateField(default=datetime.date.today,verbose_name='日付')
    cooking_easiness = models.IntegerField(choices=EASINESS_CHOICES,default=1,verbose_name='調理の手軽さ')
    is_favorite = models.IntegerField(default=0,verbose_name='お気に入り')#0:お気に入りではない,1:お気に入り
    memo = models.CharField(max_length=300,blank=True,verbose_name='メモ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} の献立記録"
    
