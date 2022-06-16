import logging
# noinspection PyPackageRequirements
from telegram.ext import ApplicationBuilder
# from config.cities import runner
from config import BOT_TOKEN

# COMMAND HANDLERS
from handlers.command.start import start_command_handler
from handlers.command.help import help_command_handler
from handlers.command.start_chatting import start_chatting_command_handler
from handlers.command.stop_chatting import stop_chatting_command_handler
from handlers.command.settings import settings_command_handler
from handlers.command.me import me_command_handler

# QUERY HANDLERS
from handlers.query.keyboard_markups import query_handler_user_age_keyboard_markup
from handlers.query.keyboard_markups import query_handler_interlocutor_age_keyboard_markup
from handlers.query.keyboard_markups import query_handler_user_sex_keyboard_markup
from handlers.query.keyboard_markups import query_handler_interlocutor_sex_keyboard_markup
from handlers.query.keyboard_markups import query_handler_close
from handlers.query.change_settings import query_handler_change_settings
from handlers.query.keyboard_markups import query_handler_user_city_keyboard_markup
from handlers.query.keyboard_markups import query_handler_interlocutor_city_keyboard_markup
from handlers.message import message_handler

logging.basicConfig(
    format='[%(asctime)s: %(levelname)s] - %(message)s',
    level=logging.INFO
)


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # COMMAND HANDLERS
    application.add_handler(start_command_handler)
    application.add_handler(help_command_handler)
    application.add_handler(settings_command_handler)

    application.add_handler(start_chatting_command_handler)
    application.add_handler(stop_chatting_command_handler)

    application.add_handler(me_command_handler)

    # QUERY HANDLERS
    application.add_handler(query_handler_user_age_keyboard_markup)
    application.add_handler(query_handler_interlocutor_age_keyboard_markup)

    application.add_handler(query_handler_user_sex_keyboard_markup)
    application.add_handler(query_handler_interlocutor_sex_keyboard_markup)

    application.add_handler(query_handler_change_settings)
    application.add_handler(query_handler_close)

    application.add_handler(query_handler_user_city_keyboard_markup)
    application.add_handler(query_handler_interlocutor_city_keyboard_markup)

    # MESSAGE HANDLER
    application.add_handler(message_handler)

    # POLLING
    application.run_polling(stop_signals=None)


if __name__ == '__main__':
    main()
