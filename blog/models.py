from sre_parse import CATEGORIES
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager 

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    main_category = models.ForeignKey("MainCategory", related_name='main', on_delete=models.SET_NULL,blank=True,null=True)
    category = models.ForeignKey("Category", related_name='categories', on_delete=models.SET_NULL,blank=True,null=True)
    sub_category = models.ForeignKey("SubCategory", related_name='sub', on_delete=models.SET_NULL,blank=True,null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    tags = TaggableManager()

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail", args={self.slug})
    
    def get_related_posts(self):
        return Blog.objects.filter(tags__in = self.tags.all()).distinct().exclude(id=self.id)

    def __str__(self):
        return self.title
    

class MainCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True,null=True)
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(MainCategory,self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Main categories'
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    main_category = models.ForeignKey(MainCategory,on_delete=models.CASCADE, blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory,self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Sub categories'
    def __str__(self):
        return self.name

class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog= models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content[:15]
    

class Reply(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    comment= models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.reply[:15]

class About(models.Model):
    img = models.ImageField(upload_to=None, blank=True, null=True)
    discreption = models.TextField()
    background = models.TextField()
    team_work = models.TextField()
    our_core_value = models.TextField()

    def __str__(self): 
        return self.discreption[:30]