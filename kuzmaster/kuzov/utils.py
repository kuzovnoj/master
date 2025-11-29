import telegram
from django.conf import settings


# отправка сообщений мастерам если в текущих заказ-нарядах есть изменения
def send_telegram_message(message, chat_id=None):
    if chat_id is None:
        chat_id = settings.TELEGRAM_CHAT_ID
    
    try:
        bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
        bot.send_message(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
        return True
    except telegram.error.TelegramError as e:
        print(f"Ошибка Telegram: {e}")
        return False
    except Exception as e:
        print(f"Общая ошибка: {e}")
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

