import logging
from django.views import generic
from django.views.generic import ListView
from .models import Post
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import EmailModel  # EmailModelはデータベースモデルとして作成しておく
from .forms import ContactForm  # EmailFormをインポート
from .models import Registration
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from django.shortcuts import get_object_or_404, render
from django.views import View

logger = logging.getLogger(__name__)

def index(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.send_email()
            form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = RegistrationForm()

    return render(request, 'index.html', {'form': form})




class DiaryView(generic.TemplateView):
    template_name = "diary.html"

class HelloView(generic.TemplateView):
    template_name = "hello.html"

class TashizanView(generic.ListView):
    model = Post
    template_name = 'tashizan.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['names'] = '川上'
        value = 10 + 20
        context['value'] = value
        a = 7
        b = 5
        c = 10
        context['tashizan'] = a + b + c
        return context

class KajikiView(generic.TemplateView):
    model = Post
    template_name = "kajiki.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        import requests
        from bs4 import BeautifulSoup
        import re
        import os.path
        
        url = "https://www.kajiki-k.jp/" # 読み込み先のURL
        res = requests.get(url)
        res.encoding = 'UTF-8' # エンコーディングを適切な値に設定する
        
        soup = BeautifulSoup(res.text, "html.parser")
        elems = soup.find_all(href=re.compile("diary/2023")) # Topページの「diary/2023」というテキストが含まれた要素を探す
        toppage_links = [elem.attrs['href'] for elem in elems] # Topページの「diary/2023」というaタグの中身を取得
        
        toppage_links_lists =[] # Topページの「diary/2023」というaタグの中身を単体ではなく複数取得して変数に入れる為にリストを作成
        for toppage_link in toppage_links:
            toppage_links_lists.append(toppage_link.replace('diary/', 'https://www.kajiki-k.jp/diary/')) # toppage_links_listsに.appendを使ってリストに要素を追加する。その際に「diary/」を「https://www.kajiki-k.jp/diary/」に置換する。置換する意味は絶対パスにして次のプログラミングでその絶対パスのリンク先に移動する為。
        
        # 複数取得して変数に入れる為にリストを作成
        result_title = []
        result_link = []
        result_h3text = []
        result_divtext = []
        kugiri = "\n--------------------\n"
        
        # Topで取得した「https://www.kajiki-k.jp/diary/2023/diary23○○.html」の複数のページへそれぞれ移動し順に処理
        for toppage_links_list in toppage_links_lists:
            toppage_links_lists_res = requests.get(toppage_links_list)
            toppage_links_lists_res.encoding = 'UTF-8'  # エンコーディングを適切な値に設定する
            toppage_links_lists_soup = BeautifulSoup(toppage_links_lists_res.text, "html.parser")
        
             # ページタイトルを複数取得し、変数result_titleのリストへ格納
            result_title.append(toppage_links_lists_soup.title.text + kugiri)
            # print(toppage_links_lists_soup.title.text)
        
             # URLを複数取得し、変数result_linkのリストへ格納
            result_link.append(toppage_links_list + kugiri)
            # print(toppage_links_list)
        
            h3texts = toppage_links_lists_soup.find_all("h3", class_="diary_title") # h3タグの.diary_titleを取得
            for h3text in h3texts:
                result_h3text.append(h3text.get_text() + kugiri) # .diary_titleを複数取得し、変数result_h3textのリストへ格納
                # print(h3text.get_text())
        
            divtexts = toppage_links_lists_soup.find_all("div", class_="update_contents_right_box_in") #divタグの.update_contents_right_box_inを取得
            for divtext in divtexts:
                result_divtext.append(divtext.get_text() + kugiri) # .update_contents_right_box_inを複数取得し、変数result_divtextのリストへ格納
                # print(divtext.get_text())
        
            # リストの要素を.joinを使って、スペース区切りで結合した文字列にする。テキストファイルに書き出すにはリストのままでは不可なので、str（文字列）にする必要がある為。
            result_title_str = ' '.join(result_title)
            result_link_str = ' '.join(result_link)
            result_h3text_str = ' '.join(result_h3text)
            result_divtext_str = ' '.join(result_divtext)
        
            dirname = os.path.dirname(__file__)
            path = os.path.join(dirname, "templates/kajiki_croll.txt")
            f = open(path, "w", encoding="utf-8") # テキストファイルを開く。保存場所を指定しないとユーザーフォルダ直下にデフォルトでは出来てしまう為、保存場所を指定。wなのでまっさらにして書き込む。
            f.write(result_title_str + result_link_str + result_h3text_str + result_divtext_str) # テキストファイルに書き込む
            f.close() # テキストファイルを閉じる

        context['kajiki1'] = result_title_str
        context['kajiki2'] = result_link_str
        context['kajiki3'] = result_h3text_str
        context['kajiki4'] = result_divtext_str
        return context

class TenkiView(generic.ListView):
    model = Post
    template_name = "tenki.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
        
        def GET_Weather():
            # 大阪市淀川区の天気のURLをセット
            url = "https://tenki.jp/forecast/6/30/6200/27123/"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            rs = soup.find(class_='forecast-days-wrap clearfix')
            # 天気を取得
            rs_wether = rs.findAll(class_='weather-telop')
            today_weather = rs_wether[0].text.strip()
            tomorrow_weather = rs_wether[1].text.strip()
            # 最高気温を取得
            rs_hightemp = rs.findAll(class_='high-temp temp')
            today_hightemp = rs_hightemp[0].text.strip()
            tomorrow_hightemp = rs_hightemp[1].text.strip()
            # 最高気温差を取得
            rs_hightempdiff = rs.findAll(class_='high-temp tempdiff')
            today_hightempdiff = rs_hightempdiff[0].text.strip()
            tomorrow_hightempdiff = rs_hightempdiff[1].text.strip()
            # 最低気温を取得
            rs_lowtemp = rs.findAll(class_='low-temp temp')
            today_lowtemp = rs_lowtemp[0].text.strip()
            tomorrow_lowtemp = rs_lowtemp[1].text.strip()
            # 最高気温差を取得
            rs_lowtempdiff = rs.findAll(class_='low-temp tempdiff')
            today_lowtempdiff = rs_lowtempdiff[0].text.strip()
            tomorrow_lowtempdiff = rs_lowtempdiff[1].text.strip()
            # 降水確率を取得
            rs_rain = soup.select('.rain-probability > td')
            today_rain_1 = rs_rain[0].text.strip()
            today_rain_2 = rs_rain[1].text.strip()
            today_rain_3 = rs_rain[2].text.strip()
            today_rain_4 = rs_rain[3].text.strip()
            tomorrow_rain_1 = rs_rain[4].text.strip()
            tomorrow_rain_2 = rs_rain[5].text.strip()
            tomorrow_rain_3 = rs_rain[6].text.strip()
            tomorrow_rain_4 = rs_rain[7].text.strip()
            # 風向
            rs_wind = soup.select('.wind-wave > td')
            print(rs_wind)
            today_wind = rs_wind[0].text.strip()
            tomorrow_wind = rs_wind[1].text.strip()
            # 取得結果をdfに格納
            # df = pd.DataFrame(
            # data={'#': ['天気', '最高気温', '最高気温差', '最低気温', '最低気温差', 
            #         '降水確率[00-06]', '降水確率[06-12]', '降水確率[12-18]', 
            #         '降水確率[18-24]', '風向'],
            #       '今日': [today_weather, today_hightemp, today_hightempdiff, 
            #         today_lowtemp, today_lowtempdiff, today_rain_1, today_rain_2, 
            #         today_rain_3, today_rain_4, today_wind], 
            #       '明日': [tomorrow_weather, tomorrow_hightemp, tomorrow_hightempdiff, 
            #         tomorrow_lowtemp, tomorrow_lowtempdiff, tomorrow_rain_1, tomorrow_rain_2, 
            #         tomorrow_rain_3, tomorrow_rain_4, tomorrow_wind],
            #     }
            # )
            # print(df)
            context['templates_weather1'] = '天気：' + today_weather + "\n最高気温：" + today_hightemp + '\n最高気温差：' + today_hightempdiff + '\n最低気温差：' + today_lowtemp + '\n降水確率[00-06]：' + today_rain_1 + '\n降水確率[06-12]：' + today_rain_2 + '\n降水確率[12-18]：' + today_rain_3 + '\n降水確率[18-24]：' + today_rain_4 + '\n風向：' + today_wind
            
            context['templates_weather2'] = '天気：' + tomorrow_weather + "\n最高気温：" + tomorrow_hightemp + '\n最高気温差：' + tomorrow_hightempdiff + '\n最低気温差：' + tomorrow_lowtemp + '\n降水確率[00-06]：' + tomorrow_rain_1 + '\n降水確率[06-12]：' + tomorrow_rain_2 + '\n降水確率[12-18]：' + tomorrow_rain_3 + '\n降水確率[18-24]：' + tomorrow_rain_4 + '\n風向：' + tomorrow_wind
        GET_Weather()

        return context

def TashizanFormView(request):
    template_name="tashizan_form.html"
    context = {}  # コンテキスト辞書を初期化

    if request.POST:
        numbers1 = int(request.POST['numbers1'])
        numbers2 = int(request.POST['numbers2'])

    #受け取った値で必要な処理を行います
        context['numbers1'] = numbers1  # コンテキストに変数を追加
        context['numbers2'] = numbers2  # コンテキストに変数を追加
        context['result'] = numbers1 + numbers2

    return render(request, template_name, context)  # コンテキストをテンプレートに渡す)

class RegistrationView(generic.FormView):
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('caretaxi:registration')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, '情報を登録しました。')
        logger.info('Registration sent by {}'.format(form.cleaned_data['business_name']))

        # データベースに保存
        form.save()

        return super().form_valid(form)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from .models import Registration

def registration_list(request):
    items_per_page = 10
    registrations = Registration.objects.all().order_by('-id')

    search_column = request.GET.get('search_column', 'all')
    search_text = request.GET.get('search_text', '')
    search_genres = request.GET.get('search_genres', '')

    # views.py の inquiry_list 関数に追加した部分
    # 選択された項目と検索テキストに基づいて結果をフィルタリング
    if search_text:
        if search_column == 'all':
            registrations = registrations.filter(
                Q(business_name__icontains=search_text) |
                Q(features__icontains=search_text) |
                Q(postal_code__icontains=search_text) |
                Q(location__icontains=search_text) |
                Q(tel__icontains=search_text) |
                Q(carmodel__icontains=search_text) |
                Q(email__icontains=search_text) |
                Q(siteurl__icontains=search_text) |
                Q(message__icontains=search_text)
            )
        else:
            registrations = registrations.filter(**{f'{search_column}__icontains': search_text})

    # デザインの種類に基づいて結果をフィルタリング
    if search_genres:
        registrations = registrations.filter(genres__icontains=search_genres)

    paginator = Paginator(registrations, items_per_page)

    page = request.GET.get('page', 1)

    try:
        registrations = paginator.page(page)
    except PageNotAnInteger:
        registrations = paginator.page(1)
    except EmptyPage:
        registrations = paginator.page(paginator.num_pages)

    return render(request, 'registration_list.html', {
        'registrations': registrations,
        'search_column': search_column,
        'search_text': search_text,
        'search_genres': search_genres,
    })

# 編集画面
class EditRegistrationView(View):
    template_name = 'edit_registration.html'

    def get(self, request, registration_id):
        registration = get_object_or_404(Registration, id=registration_id)
        form = RegistrationForm(instance=registration)

        # genres_initial のデータ型が文字列 (<class 'str'>) であることが確認できたので、この文字列をリストに変換する必要がある。ここがてこずった場所。
        genres_initial = form.initial['genres']
        genres_list = eval(genres_initial) if genres_initial else [] # genres_list のデータ型が正しくリスト (<class 'list'>) に変換された。これでチェックボックスにチェックが入った状態で編集画面が表示されるようになった。

        # genresのchoicesを指定
        form.fields['genres'].widget.choices = form.fields['genres'].choices

        # フォームに初期値を手動でセット
        form.initial['genres'] = genres_list

        return render(request, self.template_name, {'form': form, 'registration': registration})
    
    def post(self, request, registration_id):
        registration = get_object_or_404(Registration, id=registration_id)
        form = RegistrationForm(request.POST, instance=registration)  # InquiryFormは適切なフォームに変更してください
        if form.is_valid():
            form.save()
            # 保存が成功した場合の追加の処理
            messages.success(request, '変更が保存されました。')  # 成功メッセージを表示するなどの処理を追加
            return render(request, self.template_name, {'form': form, 'registration': registration})

        # バリデーションに失敗した場合の処理
        messages.error(request, 'フォームの入力に誤りがあります。')  # エラーメッセージを表示するなどの処理を追加
        return render(request, self.template_name, {'form': form, 'registration': registration})

# 詳細画面
class DetailRegistrationView(View):
    template_name = 'detail_registration.html'

    def get(self, request, registration_id):
        registration = get_object_or_404(Registration, id=registration_id)
        return render(request, self.template_name, {'registration': registration})

# 市町村別にフィルタリングする関数
def filter_by_city(request, prefecture, city):
    query = f"{prefecture}{city}"
    registrations = Registration.objects.filter(location__startswith=query)

    paginator = Paginator(registrations, 10) # 1ページに表示する件数を設定
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'city_filter_results.html', {
        'page_obj': page_obj, 
        'prefecture': prefecture, 
        'city': city
    })

class PrefectureView(generic.TemplateView):
    template_name = "prefecture.html"

from .forms import PostalCodeForm
import requests

def lookup_address(postal_code):
    # 外部APIを使用して住所を取得
    response = requests.get(f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={postal_code}")
    data = response.json()

    if data['results']:
        result = data['results'][0]
        prefecture = result['address1']  # 都道府県
        city = result['address2']  # 市区町村
        return prefecture, city
    else:
        return None, None

def PostalCodeView(request):
    form = PostalCodeForm(request.POST or None)
    url = None
    address_text = None

    if request.method == 'POST' and form.is_valid():
        postal_code = form.cleaned_data.get('postal_code').replace('-', '')

        # 外部APIを使って住所を取得
        prefecture, city = lookup_address(postal_code)

        if prefecture and city:
            url = f"http://localhost:7000/prefecture/{prefecture}/city/{city}/"
            address_text = f"{prefecture}{city}"  # 都道府県と市区町村を結合して表示用のテキストを作成
        else:
            url = "郵便番号に該当する住所が見つかりません。"

    return render(request, 'postal_code.html', {'form': form, 'url': url, 'address_text': address_text})

import os
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_email(form)
            return redirect('/contact_finish/')  # URLパスを直接指定
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})


def send_email(self):
    business_name = self.cleaned_data['business_name']
    name = self.cleaned_data['name']
    onamae = self.cleaned_data['onamae']
    postal_code = self.cleaned_data['postal_code']
    location = self.cleaned_data['location']
    tel = self.cleaned_data['tel']
    email = self.cleaned_data['email']
    message = self.cleaned_data['message']
    
    subject = 'お問い合わせ {}'.format(business_name)
    body = (
        f"事業者名: {business_name}\n"
        f"お名前: {name}\n"
        f"オナマエ: {onamae}\n"
        f"郵便番号: {postal_code}\n"
        f"所在地: {location}\n"
        f"電話番号: {tel}\n"
        f"メールアドレス: {email}\n"
        f"お問い合わせ内容:\n{message}"
    )
    
    from_email = os.environ.get('FROM_EMAIL')
    to_list = [os.environ.get('FROM_EMAIL')]
    cc_list = [email]
    
    email_message = EmailMessage(subject=subject, body=body, from_email=from_email, to=to_list, cc=cc_list)
    email_message.send()

def contact_finish(request):
    return render(request, 'contact_finish.html')
