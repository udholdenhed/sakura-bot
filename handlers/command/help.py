import logging
# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CommandHandler

HELP_COMMAND_TEXT = '💬\"/start_chatting\" - to start a conversation with a random person.\n' \
                    '💬\"/stop_chatting\" - to stop a conversation.\n\n' \
                    '🔧\"/settings\" - to setting up your age, sex, city or interlocutor.\n' \
                    '📃\"/me\" - to see information about yourself.'


async def help_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """
    This function is need to be called on the user command '/help'.
    The function sends a help text to the user.

    Not recommended for use without a 'CommandHandler'.
    """

    logging.info(f'Help command from user with id {update.message.from_user.id}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_COMMAND_TEXT)


# Handler that handles the '/help' command.
help_command_handler = CommandHandler(
    command='help',
    callback=help_callback
)
