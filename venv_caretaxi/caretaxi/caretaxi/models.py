from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Registration(models.Model):
    REUSE_CHOICES = [
        ('未', '未'),
        ('済', '済'),
    ]

    business_name = models.CharField(max_length=999)
    features = models.CharField(max_length=999)
    postal_code = models.CharField(max_length=8)
    location = models.CharField(max_length=999)
    tel = models.CharField(max_length=16)
    carmodel = models.CharField(max_length=999)
    email = models.EmailField()
    siteurl = models.CharField(max_length=999)
    message = models.TextField()
    main_image = models.ImageField(upload_to='registration_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    genres = models.CharField(max_length=999, blank=True, null=True)

    def __str__(self):
        return self.location

class ContactModel(models.Model):
    business_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    name_kana = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    tel = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class Wishlist(models.Model):
    session_key = models.CharField(max_length=40)
    urls = models.TextField()  # URLをカンマ区切りで保存

    def add_url(self, url):
        url_list = self.urls.split(',') if self.urls else []
        if url not in url_list:
            url_list.append(url)
            self.urls = ','.join(url_list)
            self.save()

    def get_urls(self):
        return self.urls.split(',') if self.urls else []
