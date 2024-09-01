from django.contrib import admin
from .models import ContactModel, Registration
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# リソースクラスを定義
class RegistrationResource(resources.ModelResource):
    class Meta:
        model = Registration
        fields = ('id', 'business_name', 'features', 'postal_code', 'location', 'tel', 'carmodel', 'email', 'siteurl', 'message', 'main_image', 'created_at', 'genres')

# 管理画面を拡張
@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin):
    resource_class = RegistrationResource
    list_display = ('business_name', 'features', 'postal_code', 'location', 'tel', 'carmodel', 'email', 'siteurl', 'message', 'main_image', 'genres', 'created_at')
    readonly_fields = ('created_at',)

# ContactModelの登録
admin.site.register(ContactModel)
