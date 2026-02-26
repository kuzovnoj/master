import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_telegram_message(message):
    """Отправка сообщения в Telegram"""
    try:
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        chat_id = getattr(settings, 'TELEGRAM_GROUP_CHAT_ID', None)
        
        if not bot_token or not chat_id:
            logger.error("Telegram bot token or chat ID not configured")
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            logger.info("Telegram message sent successfully")
            return True
        else:
            logger.error(f"Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        return False

def format_appointment_message(appointment):
    """Форматирование сообщения о записи"""
    return f"""
🔔 <b>НОВАЯ ЗАПИСЬ НА ОСМОТР</b>

👤 Имя: {appointment.name}
📞 Телефон: {appointment.phone}
🚗 Марка авто: {appointment.car_model or 'Не указана'}
📅 Дата: {appointment.date.strftime('%d.%m.%Y')}
⏰ Время: {appointment.time_slot}

<a href="https://kuzovnojmaster.ru/admin/calculator/appointment/{appointment.id}/change/">Посмотреть в админке</a>
"""

def format_callback_message(callback):
    """Форматирование сообщения о звонке"""
    return f"""
🔔 <b>ЗАКАЗ ЗВОНКА</b>

👤 Имя: {callback.name}
📞 Телефон: {callback.phone}

<a href="https://kuzovnojmaster.ru/admin/calculator/callbackrequest/{callback.id}/change/">Посмотреть в админке</a>
"""