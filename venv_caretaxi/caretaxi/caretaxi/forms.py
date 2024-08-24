import os
from django import forms
from django.core.mail import EmailMessage
from .models import Registration
import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe

class RegistrationForm(forms.ModelForm):
    GENRE_CHOICES = [
        ('車いす', '車いす'),
        ('リクライニング車いす', 'リクライニング車いす'),
        ('ストレッチャー', 'ストレッチャー'),
        ('UDタクシー', 'UDタクシー'),
        ('介護保険', '介護保険'),
        ('女性介助', '女性介助'),
    ]

    postal_code = forms.CharField(
        label=mark_safe('郵便番号 <span class="text-danger">*必須</span>'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: 123-4567'}),
    )

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        # ハイフンなしの7桁の場合、自動でハイフンを挿入
        if len(postal_code) == 7 and postal_code.isdigit():
            postal_code = f'{postal_code[:3]}-{postal_code[3:]}'
        
        # フォーマット後に正しい形式か確認
        if not re.match(r'^\d{3}-\d{4}$', postal_code):
            raise ValidationError('正しい郵便番号の形式で入力してください。')
        
        return postal_code

    genres = forms.MultipleChoiceField(
        label='主なサービス',
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    business_name = forms.CharField(
        label=mark_safe('事業所名 <span class="text-danger">*必須</span>'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    features = forms.CharField(
        label='特徴',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        label=mark_safe('所在地 <span class="text-danger">*必須</span>'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    tel = forms.CharField(
        label=mark_safe('電話番号 <span class="text-danger">*必須</span>'),
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    carmodel = forms.CharField(
        label='車種',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label=mark_safe('メールアドレス <span class="text-danger">*必須</span>'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    siteurl = forms.CharField(
        label='Webサイト',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='備考',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    main_image = forms.ImageField(
        label='画像を設定する',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Registration
        exclude = ['created_at']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フィールドの順序を変更
        self.order_fields([
            'business_name', 'features', 'postal_code', 'location', 
            'tel', 'genres', 'carmodel', 'email', 'siteurl', 'message', 
            'main_image'
        ])

    def clean_siteurl(self):
        siteurl = self.cleaned_data.get('siteurl')
        url_validator = URLValidator()

        try:
            # URLとして有効か確認する
            url_validator(siteurl)
            # 有効な場合、リンクに変換
            return f'<a href="{siteurl}" target="_blank">{siteurl}</a>'
        except ValidationError:
            return siteurl

class EditRegistrationForm(forms.ModelForm):
    genres = forms.MultipleChoiceField(
        choices=RegistrationForm.GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Registration
        fields = '__all__'

class RegistrationSearchForm(forms.Form):
    genres = forms.CharField(label='主なサービス', required=False)

class PostalCodeForm(forms.Form):
    postal_code = forms.CharField(
        label='郵便番号', 
        max_length=8, 
        widget=forms.TextInput(attrs={'placeholder': '例: 123-4567'})
    )

class ContactForm(forms.Form):
    business_name = forms.CharField(label='事業者名', required=False)
    name = forms.CharField(label='（必須）お名前', required=True)
    onamae = forms.CharField(label='（必須）オナマエ', required=True)
    postal_code = forms.CharField(label='郵便番号', required=False)
    location = forms.CharField(label='所在地', required=False)
    tel = forms.CharField(label='電話番号', required=False)
    email = forms.EmailField(label='（必須）メールアドレス', required=True)
    message = forms.CharField(label='（必須）お問合せ内容', widget=forms.Textarea, required=True)
