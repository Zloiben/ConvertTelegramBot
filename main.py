from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from src.config import config
from src.service.base import HTTPXClient
from src.service.сurrency_сonvert import ConvertService
from src.utils import start_message, help_message, validate_convert_args, read_words_from_file_to_set
from src.сore.error import AppException
from src.сore.logs import logger, error_message_log

httpx_client = HTTPXClient()

hello_world = read_words_from_file_to_set('hello.txt')
bye_world = read_words_from_file_to_set('bye.txt')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f'Пользователь {update.effective_user.id} Запустил бота')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message(update.effective_user),
        parse_mode='HTML'
    )


async def help_(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_message(),
        parse_mode='HTML'
    )


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда позволяет конвертировать валюту."""
    convert_service = ConvertService(httpx_client)
    logger.info(f'Пользователь {update.effective_user.id} попытка конвертировать')

    try:
        amount, from_currency, to_currency = validate_convert_args(context.args)
    except AppException as e:
        logger.info(error_message_log(update.effective_user, e))
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Произошла ошибка во время конвертации. {e.message}'
        )
        return

    try:
        value = await convert_service.convert(amount, from_currency, to_currency)
    except AppException as e:
        logger.error(error_message_log(update.effective_user, e))
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Произошла ошибка во время конвертации. {e.message}'
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Результат конвертации = {value}",
        parse_mode='HTML'
    )


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for word in update.message.text.split():
        if word in hello_world:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='И тебе привет!')
            return
        elif word in bye_world:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='И тебе пока!')
            return

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text='Буду за тобой повторять: ' + update.message.text
    )


COMMANDS = {
    "start": start,
    "help": help_,
    "convert": convert,
}


def main() -> None:
    application = Application.builder().token(config.BOT_TOKEN).build()

    for k, v in COMMANDS.items():
        application.add_handler(CommandHandler(k, v))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    logger.info('Запуск бота')
    application.run_polling()


if __name__ == '__main__':
    main()
