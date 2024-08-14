from django.contrib import admin
from .models import EmailModel, Registration

# class InquiryAdmin(admin.ModelAdmin):
#     list_display = ('business_name', 'features', 'location', 'tel', 'carmodel', 'email', 'siteurl', 'message', 'main_image', 'genres', 'created_at')
#     readonly_fields = ('created_at',)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'features', 'location', 'tel', 'carmodel', 'email', 'siteurl', 'message', 'main_image', 'genres', 'created_at')
    readonly_fields = ('created_at',)

# admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(EmailModel)

admin.site.register(Registration, RegistrationAdmin)
