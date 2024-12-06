# -*- coding: utf-8 -*-
"""Привет!\nВ этой библиотеке Вы увидете некоторые функции [бота Флореста](https://t.me/postbotflorestbot).\nМои социальные сети: [тык](https://taplink.cc/florestone4185)"""

class Cripto():
    """Класс со списком криптовалют, которые доступны для функции `crypto_price`.\nBITKOIN, USDT, DOGECOIN, HAMSTERCOIN"""
    BITKOIN = 'bitcoin'
    USDT = 'tether'
    DOGE = 'dogecoin'
    HMSTR = 'hamster'

class FunctionsObject:
    def __init__(self, proxies: dict = {}, html_headers: dict = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'Accept-Language': 'ru-RU'}, google_api_key: str = "", gigachat_key: str = "", gigachat_id: str = ""):
        """Привет. Именно в данном классе находятся ВСЕ функции бота. Давай я объясню смысл параметров?\nproxies: прокси, которые используются при HTTPS запросах к сайтам.\nhtml_headers: заголовки HTTPS запросов.\ngoogle_api_key: апи ключ гугла. Получить его можно [здесь](https://console.google.com/)\ngigachat_key: ключ от GigaChat (ПАО "СберБанк")\ngigachat_id: ID от GigaChat."""
        print(f'Объект класса был успешно запущен.')
        self.proxies = proxies
        self.headers = html_headers
        self.google_key = google_api_key
        self.gigachat_key = gigachat_key
        self.client_id_gigachat = gigachat_id
    def generate_image(self, prompt: str) -> bytes:
        """Данная функция генерирует картинки с помощью GigaChat.\nprompt: запрос, по которому надо сгенерировать изображение."""
        import requests, re, urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if self.gigachat_key and self.client_id_gigachat:
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

            payload={
                'scope': 'GIGACHAT_API_PERS'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': f'{self.client_id_gigachat}',
                'Authorization': f'Basic {self.gigachat_key}'
            }

            response = requests.request("POST", url, headers=headers, data=payload, verify=False, proxies=self.proxies)

            access_token = response.json()['access_token']

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            data = {
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "system",
                        "content": "Glory to Florest."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "function_call": "auto"
            }

            patterns = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

            response = requests.post(
                'https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
                headers=headers,
                json=data,
                verify=False,
                proxies=self.proxies
            )
            json = response.json()
            matches = re.search(patterns, json['choices'][0]['message']['content'])
            if not matches:
                return f"Нельзя нарисовать что-либо по данному запросу. Причина: {json['choices'][0]['message']['content']}"
            else:
                req_img = requests.get(f"https://gigachat.devices.sberbank.ru/api/v1/files/{matches}/content", headers={'Accept': 'application/jpg', "Authorization":f"Bearer {access_token}"}, verify=False, stream=True, proxies=self.proxies)
                return req_img.content
        else:
            return "Нужно указать параметр `gigachat_key` и `gigachat_id` в настройках класса для работы с этой функцией."
    def ai(self, prompt: str) -> dict:
        """Используем GigaChat.\nprompt: что тебе нужно от нейросетки.\nВозвращает словарь при удачном исполнении кода."""
        import requests, json
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if self.gigachat_key and self.client_id_gigachat:
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

            payload={
                'scope': 'GIGACHAT_API_PERS'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': f'{self.client_id_gigachat}',
                'Authorization': f'Basic {self.gigachat_key}'
            }

            response = requests.request("POST", url, headers=headers, data=payload, verify=False, proxies=self.proxies)

            access_token = response.json()['access_token']

            url1 = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

            payload1 = json.dumps({
                "model": "GigaChat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "repetition_penalty": 1
            })
            headers1 = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            response1 = requests.request("POST", url1, headers=headers1, data=payload1, verify=False, proxies=self.proxies)
            return response1.json()
        else:
            return "Нужно указать параметр `gigachat_key` и `gigachat_id` в настройках класса для работы с этой функцией."
        
    def deanon(self, ip: str) -> list:
        """Деанончик по IP.\nВы сами принимаете на себя ответственность за использование данной функции.\nip: дай айпи, тварюка."""
        import requests
        r = requests.get(f'http://ip-api.com/json/{ip}?lang=ru', proxies=self.proxies, headers=self.headers).json()
        results = []
        for key, value in r.items():
            results.append(f'{key.title()}: {value}')
        return results
    def download_video(self, url: str):
        """Данная функция качает видео с YouTube с помощью URL.\nurl: ссылка на видео."""
        from pytubefix import YouTube

        yt_obj = YouTube(url, proxies=self.proxies)

        if yt_obj.age_restricted:
            return 'На видео наложены возрастные ограничения.'    
        else:
            import io

            buffer = io.BytesIO()

            yt_obj.streams.get_lowest_resolution().stream_to_buffer(buffer)

            return buffer.getvalue()
    def search_videos(self, query: str):
        """Функция для поиска видео по запросу и дальнейшего его закачивания.\nquery: запрос, по которому надо искать видео."""
        from pytubefix import Search

        search = Search(query, proxies=self.proxies)
        videos = search.videos

        if len(videos) == 0:
            return 'Видео по запросу не существует.'
        else:
            video = videos[0]
            if video.age_restricted:
                return 'На видео, которое мы нашли первым присутствуют возрастные ограничение. Его скачивание невозможно.'  
            else:
                import io

                buffer = io.BytesIO()

                video.streams.get_lowest_resolution().stream_to_buffer(buffer)

                return buffer.getvalue()
    def create_demotivator(self, top_text: str, bottom_text: str, photo: bytes, font: str):
        """Создайте демотиватор с помощью данной фичи!\ntop_text: верхний текст.\nbottom_text: нижний текст.\nphoto: ваша фотография в bytes.\nfont: ваш шрифт. Пример: `times.ttf`."""
        import io
        image = io.BytesIO(photo)
        from PIL import Image, ImageOps, ImageDraw, ImageFont
        img = Image.new('RGB', (1280, 1024), color='black')
        img_border = Image.new('RGB', (1060, 720), color='#000000')
        border = ImageOps.expand(img_border, border=2, fill='#ffffff')
        user_img = Image.open(image).convert("RGBA").resize((1050, 710))
        (width, height) = user_img.size
        img.paste(border, (111, 96))
        img.paste(user_img, (118, 103))
        drawer = ImageDraw.Draw(img)
        font_1 = ImageFont.truetype(font=font, size=80, encoding='UTF-8')
        text_width = font_1.getlength(top_text)

        while text_width >= (width + 250) - 20:
            font_1 = ImageFont.truetype(font=font, size=80, encoding='UTF-8')
            text_width = font_1.getlength(top_text)
            top_size -= 1

        font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
        text_width = font_2.getlength(bottom_text)

        while text_width >= (width + 250) - 20:
            font_2 = ImageFont.truetype(font=font, size=60, encoding='UTF-8')
            text_width = font_2.getlength(bottom_text)
            bottom_size -= 1

        size_1 = drawer.textlength(top_text, font=font_1)
        size_2 = drawer.textlength(bottom_text, font=font_2)

        drawer.text(((1280 - size_1) / 2, 840), top_text, fill='white', font=font_1)
        drawer.text(((1280 - size_2) / 2, 930), bottom_text, fill='white', font=font_2)

        result_here = io.BytesIO()

        img.save(result_here, 'JPEG')
    
        del drawer

        return result_here.getvalue()
    def photo_make_black(self, photo: bytes):
        """Сделать фото черно-белым.\nphoto: фото в `bytes`."""
        import io
        from PIL import Image
        your_photo = io.BytesIO(photo)

        image = Image.open(your_photo)
        new_image = image.convert('L')
        buffer = io.BytesIO()
        new_image.save(buffer, 'JPEG')
        return buffer.getvalue()
    def check_weather(self, city: str):
        """Проверить погоду в каком-либо городе.\ncity: город, или населенный пункт."""
        import requests
        from bs4 import BeautifulSoup

        r = requests.get(f'https://www.google.ru/search?q=погода+в+{city}', proxies=self.proxies, headers=self.headers)
        if r.status_code != 200:
            return 'Ошибка. Не получилось получить доступ к Google.'
        else:
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                temperature = soup.select("#wob_tm")[0].getText()
                title = soup.select("#wob_dc")[0].getText()
                humidity = soup.select("#wob_hm")[0].getText()
                time = soup.select("#wob_dts")[0].getText()
                wind = soup.select("#wob_ws")[0].getText()
                veroyatnost = soup.select("#wob_pp")[0].getText()
                return {"temp":temperature, "opisanie":title, 'humidity':humidity, 'time':time, 'wind':wind, 'veroyatnost':veroyatnost}
            except:
                return "Не был найден населенный пункт."
    def create_qr(self, content: str):
        """Создать QR код.\ncontent: что будет нести в себе qr. ссылка, текст..."""
        import qrcode
        import io
        
        buffer = io.BytesIO()
        qr = qrcode.make(content)
        qr.save(buffer, scale=10)
        return buffer.getvalue()
    def get_charts(self):
        """Узнать чарты Я.Музыки."""
        import requests
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,fi;q=0.6,nb;q=0.5,is;q=0.4,pt;q=0.3,ro;q=0.2,it;q=0.1,de;q=0.1',
            'Connection': 'keep-alive',
            'Referer': 'https://music.yandex.ru/chart',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Current-UID': '403036463',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Retpath-Y': 'https://music.yandex.ru/chart',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        params = {
            'what': 'chart',
            'lang': 'ru',
            'external-domain': 'music.yandex.ru',
            'overembed': 'false',
            'ncrnd': '0.23800355071570123',
        }
        result = []
        response = requests.get('https://music.yandex.ru/handlers/main.jsx', params=params, headers=headers, proxies=self.proxies)
        chart = response.json()['chartPositions']
        for track in chart[:10]:
            position = track['track']['chart']['position']
            title = track['track']['title']
            author = track['track']['artists'][0]['name']
            result.append(f"№{position}: {author} - {title}")
        return f'Чарты Яндекс Музыки на данный момент🔥\n🥇{result[0]}\n🥈{result[1]}\n🥉{result[2]}\n{result[3]}\n{result[4]}\n{result[5]}\n{result[6]}\n{result[7]}\n{result[8]}\n{result[9]}'
    def generate_password(self, symbols: int = 15):
        """Сгенерировать пароль.\nsymbols: количество символов в пароле."""
        import string
        import random

        symbols_ascii = list(string.ascii_letters + string.digits)

        random.shuffle(symbols_ascii)

        return ''.join(symbols_ascii[:symbols])
    def text_to_speech(self, text: str, lang: str = 'ru'):
        """Из текста в речь на Python.\ntext: текст для озвучки.\nlang: язык для озвучки. По умолчанию, **русский**."""
        import gtts
        import io

        buffer = io.BytesIO()
        engine = gtts.gTTS(text, lang=lang)
        engine.write_to_fp(buffer)
        return buffer.getvalue()
    def information_about_yt_channel(self, url: str):
        """Узнать информацию о YouTube канале на Python.\nurl: ссылка на канал."""
        if not self.google_key:
            return 'Для использования данной функции нужно указать параметр `google_key` в конструктор класса.'
        else:
            from googleapiclient.discovery import build
            from pytubefix import Channel
            channel = Channel(url, proxies=self.proxies).channel_id
            youtube = build('youtube', 'v3', developerKey=self.google_key)
            request = youtube.channels().list(part='snippet,statistics', id=channel.channel_id)
            response = request.execute()
            return {"url_of_ava":response["items"][0]["snippet"]["thumbnails"]["high"]["url"], "channel_name":response["items"][0]["snippet"]["title"], 'channel_nickname':response["items"][0]["snippet"]["customUrl"], 'country':response["items"][0]["snippet"]["country"], 'total_views':response["items"][0]["statistics"]["viewCount"], 'total_subs':response["items"][0]["statistics"]["subscriberCount"]}
    def crypto_price(self, crypto: str, currency: str = 'rub'):
        """Цена криптовалют.\ncrypto: крипта, которую нужно узнать. Для этого воспользуйтесь константами из класса `Cripto`.\ncurrency: валюта, в которой нужно получить результат. Доступно: `rub`, `usd` и `eur`."""
        import requests
        r = requests.get('https://api.coingecko.com/api/v3/simple/price', params={"ids":crypto, 'vs_currencies':currency}, proxies=self.proxies, headers=self.headers).json()
        if r == {}:
            return "Неправильная валюта, или криптовалюта."
        else:
            try:
                return r[crypto][currency]
            except:
                return "Произошла ошибка. Возможно, были преодолены лимиты API."
    def password_check(self, nickname: str) -> int:
        """Поиск сливов паролей по нику.\nnickname: ник для поиска.\nВозвращает `int`."""
        import requests
        req = requests.get(f'https://api.proxynova.com/comb?query={nickname}&start=0&limit=15', headers=self.headers, proxies=self.proxies)
        if req.status_code == 200:
            return req.json()['count']
    def generate_nitro(self, count: int):
        """Генерация нитро.\n(Ключи могут не работать, может потребоваться некоторое количество попыток)\ncount: количество ключей."""
        import random, string
        a = 0
        results = []
        while a < count:
            characters = string.ascii_uppercase + string.digits
            random_code = ''.join(random.choice(characters) for _ in range(15))
            formatted_code = '-'.join(random_code[i:i+4] for i in range(0, 15, 4))
            results.append(formatted_code)
        del a
        return results
    def fake_human(self):
        """Фейковый гражданин Российской Федерации. Без вопросов.\nАргументы отсутствуют.\nВозвращает словарь `dict`."""
        import faker as faker_
        from datetime import date

        faker = faker_.Faker('ru-RU')
        today = date.today()
        year_f = int(str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-")[0])
        month_f = int(str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-")[1])
        day_f = int(str(faker.date_of_birth(minimum_age=25, maximum_age=50)).split("-")[2])
        age_t = today.year - year_f - ((today.month, today.day) < (month_f, day_f))

        return {"name":faker.name(), "age":age_t, "work_place":faker.company(), "work_class":faker.job().lower(), "address":f"Российская Федерация, {faker.address()}", "postal_code":faker.address()[-6:], 'telephone_number':faker.phone_number(), "useragent":faker.user_agent(), "number_card":faker.credit_card_number(), "provider_of_card":faker.credit_card_provider(), "expire_card":faker.credit_card_expire(), "inn":faker.businesses_inn(), "orgn":faker.businesses_ogrn()}
    def real_info_of_photo(self, photo: bytes):
        """С помощью данной функции можно узнать адрес, город, почтовый индекс по фотографии.\nphoto: фотография в `bytes`."""
        import io
        from PIL import Image
        import requests
        with Image.open(io.BytesIO(photo)) as img:
            metadata = img._getexif()
            if not metadata:
                return None
            gps_info = metadata.get(34853)
            if not gps_info:
                return None
            lat = gps_info[2]
            lon = gps_info[4]
            lat_ref = gps_info[3]
            latitude = (lat[0] + lat[1] / 60.0 + lat[2] / 3600.0)
            longitude = (lon[0] + lon[1] / 60.0 + lon[2] / 3600.0)
            datetime_original = metadata.get(36867)
            try:
                if lat_ref != 'E':
                    latitude = -latitude
                r = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json", headers=self.headers, proxies=self.proxies)
                json = r.json()
                return {"country":json["address"]["country"], "region":json["address"]["state"], "district":json["address"]["district"], 'city':json["address"]["city"], "full_address":json["display_name"], 'postcode':json["address"]["postcode"], 'datetime':datetime_original}
            except:
                if lat_ref != 'E':
                    latitude = -latitude
                longitude = -longitude
                r = requests.get(f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json", headers=self.headers, proxies=self.proxies)
                json = r.json()
                return {"country":json["address"]["country"], "region":json["address"]["state"], "district":json["address"]["district"], 'city':json["address"]["city"], "full_address":json["display_name"], 'postcode':json["address"]["postcode"], 'datetime':datetime_original}
    def bmi(self, weight: float, height: float):
        """Узнать ИМТ по весу и росту.\nweight: дай вес в кг.\nheight: дай рост в метрах. Пример: 1.76 (176 см)\nВозвращает `dict` при удаче. `None` при невозможности узнать ИМТ. Не указывайте 0, либо отрицательные числа в параметры.\nИсходный код на канале моего друга: [тык](https://t.me/pie_rise_channel_s_8395/1009)"""
        if weight == 0 or weight < 0:
            return None
        else:
            if height == 0 or height < 0:
                return None
            else:
                bmi = weight / (height ** 2)
                if bmi < 18.5:
                    return {"bmi":f'{bmi:.2f}', "status":"Недостаточный вес"}
                elif 18.5 <= bmi < 25:
                    return {"bmi":f'{bmi:.2f}', "status":"Нормальный вес"}
                elif 25 <= bmi < 30:
                    return {"bmi":f'{bmi:.2f}', "status":"Избыточный вес"}
                else:
                    return {"bmi":f'{bmi:.2f}', "status":"Ожирение"}
    def link_on_user(self, id: str):
        """Введи ID юзера.\nГде его можно узнать?\nСкачайте Ayugram с официального сайта разработчика, а затем зайдите в профиль к человеку. Внизу будет его ID.\nЛибо зайдите в @username_to_id_bot и нажмите на кнопку \"User\". Если пользователь не отображается, добавьте его в контакты и повторите попытку.\nid: ID пользователя в кавычках."""
        if len(id) > 10:
            return {'status':f'Пользовательский ID не может привышать 10 символов.', 'url':None}
        elif len(id) < 10:
            return {"status":f'Пользовательский ID не может быть меньше, чем 10 символов.', 'url':None}
        else:
            try:
                return {"status":"Успех!", "url":F"tg://openmessage?user_id={int(id)}"}
            except:
                return {"status":f'Пользовательский ID не может привышать 10 символов.', 'url':None}

