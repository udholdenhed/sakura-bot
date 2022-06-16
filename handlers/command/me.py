import logging

# noinspection PyPackageRequirements
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CommandHandler

from shared_vars import database


async def me_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Me command. User ID: \'{update.effective_user.id}\'.')
    user = database.get_user(update.effective_user.id)
    if user is None:
        logging.info(f'Command from an unregistered user. '
                     f'The command cannot be executed. '
                     f'User ID: \'{update.effective_user.id}\'.')
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text='🟧You must be registered to run this command. Use \'/start\'.'
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"🔧Setting:\n"
             f"🧍Age - {user.user_age.replace('_', ' ')}.\n"
             f"🗺️Interlocutor age - {user.interlocutor_age.replace('_', ' ')}.\n\n"
             f"🧍City - {user.user_city.replace('_', ' ')}.\n"
             f"🗺️Interlocutor city - {user.interlocutor_city.replace('_', ' ')}.\n\n"
             f"🧍Sex - {user.user_sex.replace('_', ' ')}.\n"
             f"🗺️Interlocutor sex - {user.interlocutor_sex.replace('_', ' ')}.\n"
    )


me_command_handler = CommandHandler(
    command='me',
    callback=me_callback
)
