import os
from django import forms
from django.core.mail import EmailMessage
from .models import Registration
import re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError






class RegistrationForm(forms.ModelForm):
    GENRE_CHOICES = [
        ('車いす', '車いす'),
        ('リクライニング車いす', 'リクライニング車いす'),
        ('ストレッチャー', 'ストレッチャー'),
        ('UDタクシー', 'UDタクシー'),
        ('介護保険', '介護保険'),
        ('女性介助', '女性介助'),
    ]

    genres = forms.MultipleChoiceField(
        label='主なサービス',
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    business_name = forms.CharField(label='事業所名',)
    features = forms.CharField(label='特徴',)
    location = forms.CharField(label='所在地',)
    tel = forms.CharField(label='電話番号', max_length=16, required=False)
    carmodel = forms.CharField(label='車種')
    email = forms.EmailField(label='メールアドレス', required=False)
    siteurl = forms.CharField(label='Webサイト')
    message = forms.CharField(label='備考', widget=forms.Textarea, required=False)
    main_image = forms.ImageField(label='画像を設定する', required=False)

    class Meta:
        model = Registration
        exclude = ['created_at']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['business_name'].widget.attrs['class'] = 'form-control'
        self.fields['business_name'].widget.attrs['placeholder'] = '事業所名を入力してください。'
        self.fields['features'].widget.attrs['class'] = 'form-control'
        self.fields['features'].widget.attrs['placeholder'] = '特徴を入力してください。'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['placeholder'] = '所在地を入力してください。'
        self.fields['tel'].widget.attrs['class'] = 'form-control'
        self.fields['tel'].widget.attrs['placeholder'] = '電話番号を入力してください。'
        self.fields['carmodel'].widget.attrs['class'] = 'form-control'
        self.fields['carmodel'].widget.attrs['placeholder'] = '車種を入力してください。'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください。'
        self.fields['siteurl'].widget.attrs['class'] = 'form-control'
        self.fields['siteurl'].widget.attrs['placeholder'] = 'Webサイトを入力してください。'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = '備考を入力してください。'

        # フィールドの順序を変更
        self.order_fields(['business_name', 'features', 'location', 'tel', 'genres', 'carmodel', 'email', 'siteurl', 'message', 'main_image'])

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



    def send_email(self):
        business_name = self.cleaned_data['business_name']
        email = self.cleaned_data['email']
        siteurl = self.cleaned_data['siteurl']
        message = self.cleaned_data['message']
        subject = 'お問い合わせ {}'.format(business_name)
        body = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(business_name, email, message)
        from_email = os.environ.get('FROM_EMAIL')
        to_list = [os.environ.get('FROM_EMAIL')]
        cc_list = [email]
        email_message = EmailMessage(subject=subject, body=body, from_email=from_email, to=to_list, cc=cc_list)
        email_message.send()

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
    genres = forms.CharField(label='デザインの種類', required=False)
