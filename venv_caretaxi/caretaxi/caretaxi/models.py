from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class EmailModel(models.Model):
    email = models.EmailField()


class Registration(models.Model):
    REUSE_CHOICES = [
        ('未', '未'),
        ('済', '済'),
    ]

    business_name = models.CharField(max_length=999)
    features = models.CharField(max_length=999)
    postal_code = models.CharField('郵便番号', max_length=8)
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
