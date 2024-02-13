import logging
import os
from logging.handlers import TimedRotatingFileHandler

from telegram import User

from src.сore.error import AppException

__all__ = (
    'logger',
    'error_message_log'
)

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.getLogger("httpx").setLevel(logging.CRITICAL)

default_format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=default_format,
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

log_handler = TimedRotatingFileHandler('logs/.log', when="midnight", interval=1)
log_handler.suffix = "%Y-%m-%d"
log_handler.setFormatter(logging.Formatter(default_format))
log_handler.setLevel(logging.INFO)

logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


def error_message_log(user: User, e: AppException) -> str:
    return (
        f'Пользователь: {user.id}. '
        f'Сообщение: {e.message}'
        f'Доп информация: {e.content}'
    )
