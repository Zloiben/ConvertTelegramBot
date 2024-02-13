from typing import List, Tuple, Set

from telegram import User

from src.сore.const import USER_ERROR_400
from src.сore.error import AppException

__all__ = (
    'help_message',
    'start_message',
    'validate_convert_args',
    'read_words_from_file_to_set'
)


def help_message() -> str:
    return (
        f"Подсказка!\n\n"
        "Вот что я умею:\n"
        "- Конвертировать валюту (/convert  {сумма} {исходная валюта} to {целевая валюта}) \n"
    )


def start_message(user: User) -> str:
    return (
        f"Добро пожаловать, {user.mention_html()}! 👋 Я ваш помощник-бот.\n\n"
        "Я могу помочь вам с различными задачами. Вот что я умею:\n"
        "- Конвертировать валюту \n"
        "- И многое другое...\n\n"
        "Чтобы узнать больше, отправьте /help."
    )


def read_words_from_file_to_set(file_path) -> Set:
    """Чтение всех слов из файла и преобразование их в множество."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return set(text.lower().split())


def validate_convert_args(args: List) -> Tuple[float, str, str]:
    """
    Функция валидации аргументов для команды convert

    Нужный формат: <сумма> <исходная валюта> to <целевая валюта>
    :return: Количество, актуальная валюта, нужная валюта
    """
    if len(args) != 4 or args[2].lower() != 'to':
        raise AppException(
            status_code=USER_ERROR_400,
            message='Пожалуйста, используйте правильный формат: /convert <сумма> <исходная валюта> to <целевая валюта>',
            content={
                'args': args,
            }
        )

    amount = args[0]
    from_currency = args[1].upper()
    to_currency = args[3].upper()

    try:
        amount = float(amount)
    except ValueError:
        raise AppException(
            status_code=USER_ERROR_400,
            message='Пожалуйста, укажите корректную сумму.',
            content={
                'amount': amount
            }
        )
    return amount, from_currency, to_currency
