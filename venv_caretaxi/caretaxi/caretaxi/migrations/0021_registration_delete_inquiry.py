# Generated by Django 4.2.3 on 2024-08-12 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caretaxi', '0020_inquiry_business_name_inquiry_features_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=999)),
                ('features', models.CharField(max_length=999)),
                ('location', models.CharField(max_length=999)),
                ('tel', models.CharField(max_length=16)),
                ('carmodel', models.CharField(max_length=999)),
                ('email', models.EmailField(max_length=254)),
                ('siteurl', models.CharField(max_length=999)),
                ('message', models.TextField()),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='registration_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genres', models.CharField(blank=True, max_length=999, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Inquiry',
        ),
    ]
