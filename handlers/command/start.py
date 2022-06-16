import logging
# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CommandHandler

from btypes.user import User

from shared_vars import database

START_COMMAND_TEXT = '🌳Sakura is a simple telegram chat bot, ' \
                     'written in Python for a fun using \"Python Telegram Bot\" library.\n\n' \
                     '📒For help \"/help\".'


async def start_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """
    This function is need to be called on the user command '/start'.
    Function performs registration (saves the user to the database). And sends the start text.

    Not recommended for use without a 'CommandHandler'.
    """

    user_id = update.effective_user.id
    logging.info(f'Command \'start\'. User ID: \'{user_id}\'.')

    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    username = update.effective_user.username

    user = User(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        user_age='not_specified',
        user_city='not_specified',
        user_sex='not_specified',
        interlocutor_age='not_specified',
        interlocutor_city='not_specified',
        interlocutor_sex='not_specified'
    )
    logging.info(f'Attempting to save a user in the database. User ID: \'{user.user_id}\'.')
    # Checking for a user in the database.
    if database.get_user(user_id) is not None:
        logging.info(f'The user is already in the database. User ID: \'{user_id}\'.')
    # Saving the user.
    elif database.save_user(user):
        logging.info(f'The user was successfully saved to the database. User ID: \'{user_id}\'.')
    else:
        logging.warning(f'Failed to save user. User ID: \'{user_id}\'.')
        return

    await context.bot.send_message(chat_id=update.effective_chat.id, text=START_COMMAND_TEXT)


# Handler that handles the '/start' command.
start_command_handler = CommandHandler(
    command='start',
    callback=start_callback
)
