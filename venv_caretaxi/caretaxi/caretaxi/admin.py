from django.contrib import admin
from .models import ContactModel, Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'features', 'postal_code', 'location', 'tel', 'carmodel', 'email', 'siteurl', 'message', 'main_image', 'genres', 'created_at')
    readonly_fields = ('created_at',)

admin.site.register(ContactModel)

admin.site.register(Registration, RegistrationAdmin)
