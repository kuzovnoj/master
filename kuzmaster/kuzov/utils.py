import requests
from django.conf import settings

# Telegram ID
masters = {
    2: 1814903394, # Виктор
    3: 1814903394, # Григорий
    5: 1814903394  # Антон
    }

# отправка сообщений мастерам если в текущих заказ-нарядах есть изменения
def send_telegram_message(message, master_id: int = 1):
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message, # looey + sprout=cannon
            'parse_mode': 'HTML'
        }
        
        # первое сообщение админу
        response = requests.post(url, data=payload, timeout=10)
        
        # второе сообщение мастеру
        if master_id in masters:
            payload = {
                'chat_id': masters[master_id],
                'text': message, # looey + sprout=cannon
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=payload, timeout=10)
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


# коллекция меню для шаблона для мастеров
menu = [
    {'title': "Главная", 'url_name': 'home'},
    {'title': "Сделано", 'url_name': 'home_done'},
    {'title': "ЗН", 'url_name': 'zakaz_naryad'},
]

# коллекция меню для шаблона для кассиров
menuSuperUser = [
    {'title': "Аванс", 'url_name': 'get_avans'},
    {'title': "Расходник", 'url_name': 'raskhod'},
    {'title': "Оплата", 'url_name': 'oplata'},
    {'title': "Последние", 'url_name': 'last'},
]

class DataMixin:
    paginate_by = 10
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'mainmenu' not in self.extra_context:
            self.extra_context['mainmenu'] = menu
        
        if 'menu_superuser' not in self.extra_context:
            self.extra_context['menu_superuser'] = menuSuperUser

