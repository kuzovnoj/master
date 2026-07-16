import requests
import urllib3
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RedirectToCalculatorMixin(AccessMixin):
    """Перенаправляет неавторизованных пользователей на калькулятор"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

# Telegram ID
masters = {
    2: 7404913257, # Виктор
    3: 1975737865, # Григорий
    5: 7452817518, # Антон
    6: 7638694744  # Юрий
    }

masters_max = {
    3: 116274739,
    6: 109542528
    }

def _send(token, chat_id, message):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

def _send_max(token, user_id, message):
    try:
        url = "https://platform-api2.max.ru/messages"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        params = {"user_id": user_id}
        payload = {"text": message, "format": "html"}
        requests.post(url, headers=headers, params=params, json=payload, timeout=10, verify=False)
    except Exception as e:
        print(f"Ошибка отправки в Max: {e}")

def send_telegram_message(message, master_id: int = 1):
    _send(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID, message)
    if master_id in masters:
        _send(settings.TELEGRAM_BOT_TOKEN, masters[master_id], message)
    _send_max(settings.MAX_BOT_TOKEN, settings.MAX_USER_ID, message)
    if master_id in masters_max:
        _send_max(settings.MAX_BOT_TOKEN, masters_max[master_id], message)

# коллекция меню для всех
menu = [
    {'title': "Калькулятор", 'url_name': 'home'},
    {'title': "Галлерея работ", 'url_name': 'gallery:gallery'}, 
    {'title': "Услуги и цены", 'url_name': 'works:price_list'},
]
# меню для сотрудников
menuStaff = [
    {'title': "В работе", 'url_name': 'in_work'},
    {'title': "Сделано", 'url_name': 'home_done'},
    {'title': "ЗН", 'url_name': 'zakaz_naryad'},
    {'title': "Доход", 'url_name': 'income'},
]
# коллекция меню для кассиров
menuSuperUser = [
    {'title': "Аванс", 'url_name': 'get_avans'},
    {'title': "Расходник", 'url_name': 'raskhod'},
    {'title': "Оплата", 'url_name': 'oplata'},
    {'title': "Последние", 'url_name': 'last'},
]

class DataMixin:
    paginate_by = 10
    title_page = None
    description_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.description_page:
            self.extra_context['description'] = self.description_page

        if 'mainmenu' not in self.extra_context:
            self.extra_context['mainmenu'] = menu
        
        if 'menu_staff' not in self.extra_context:
            self.extra_context['menu_staff'] = menuStaff

        if 'menu_superuser' not in self.extra_context:
            self.extra_context['menu_superuser'] = menuSuperUser

