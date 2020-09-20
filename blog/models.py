from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
import os

class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name="分类名称")

    # 重写魔法函数，返回name
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类"      #单数
        verbose_name_plural = verbose_name      # 复数

class Tag(models.Model):
    name = models.CharField(max_length=255,verbose_name="标签")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博客标签"
        verbose_name = verbose_name

def article_img_path(instance,filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8],ext)
    # return '{0}/{1}/{2}'.format(instance.user.id,"avatar",filename)
    return os.path.join('avatar',filename)

class Article(models.Model):
    title = models.CharField(verbose_name="文章标题",max_length=50)
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="作者")
    img = models.ImageField(upload_to=article_img_path,null=True,blank=True,verbose_name="文章配图")
    content = models.TextField(verbose_name="文章内容")
    abstract = models.TextField(verbose_name="文章摘要",null=True,blank=True,max_length=255)
    visited = models.PositiveIntegerField(verbose_name="访问量",default=0)
    category = models.ManyToManyField('Category',verbose_name="文章分类")
    tags =  models.ManyToManyField(Tag,verbose_name="标签")
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Meta:
        verbose_name = "文章内容"
        verbose_name_plural = verbose_name
        #排序
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # 可以通过调用这个函数，直接返回详情页的url地址
    def get_absolute_url(self):
        return reverse("blog:blog_detail",kwargs={'a_id':self.id})

    #访问量加1
    def increase_visited(self):
        self.visited += 1
        self.save(update_fields = ['visited'])


