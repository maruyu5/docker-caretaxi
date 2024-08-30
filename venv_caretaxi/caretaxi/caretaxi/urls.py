from django.urls import path
from . import views
from .views import contact_form, contact_finish
from .views import registration_list
from django.conf import settings
from django.conf.urls.static import static
from .views import EditRegistrationView
from .views import DetailRegistrationView
from .views import filter_by_city

app_name = 'caretaxi'
urlpatterns = [
    path('diary/', views.DiaryView.as_view(), name="diary"),
    path('hello/', views.HelloView.as_view(), name="hello"),
    path('tashizan/', views.TashizanView.as_view(), name="tashizan"),
    path('kajiki/', views.KajikiView.as_view(), name="kajiki"),
    path('tenki/', views.TenkiView.as_view(), name="tenki"),
    path('tashizan_form/', views.TashizanFormView, name="tashizan_form"),
    path('registration/', views.RegistrationView.as_view(), name="registration"),
    path('registration_list/', registration_list, name='registration_list'),
    path('edit_registration/<int:registration_id>/', EditRegistrationView.as_view(), name='edit_registration'),
    path('detail_registration/<int:registration_id>/', DetailRegistrationView.as_view(), name='detail_registration'),
    path('prefecture/<str:prefecture>/city/<str:city>/', filter_by_city, name='filter_by_city'),
    path('prefecture/', views.PrefectureView.as_view(), name="prefecture"),
    path('postal_code/', views.PostalCodeView, name='postal_code'),
    path('contact_form/', contact_form, name='contact_form'),
    path('contact_finish/', contact_finish, name='contact_finish'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
]

# 開発環境でのみメディアファイルを提供する設定を追加
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    