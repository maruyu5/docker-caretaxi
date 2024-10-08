# Generated by Django 4.2.3 on 2024-08-24 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caretaxi', '0022_registration_postal_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('onamae', models.CharField(max_length=255)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='EmailModel',
        ),
    ]
