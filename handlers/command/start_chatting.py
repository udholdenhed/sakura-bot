import logging

# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.constants import ChatType
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CommandHandler

from btypes.user import User
from btypes.chat import Chat

from shared_vars import chats, database


async def start_chatting_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """
    This function is need to be called on the user command '/start_chatting'.

    This command searches the chat room for the user and adds him there considering all his settings.
    If the user is not registered, s/he cannot be added to the chat room. A message is sent requesting to be registered.
    If the user is already in the chat, a message is sent saying that he can't be added to the chat.

    Not recommended for use without a 'CommandHandler'.
    """

    user = User
    try:
        user = database.get_user(update.effective_user.id)
    except ...:
        context.application.stop()
        logging.error('Failed to connect to the database.')

    logging.info(f'Command \'start_chatting\'. User ID: \'{update.effective_user.id}\'.')

    # This command cannot be used in group chats. Therefore, we inform the user about it.
    if update.effective_chat.type == ChatType.GROUP:
        logging.info('\'start_chatting\' command cannot be used in group chats.')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='🟧This command cannot be used in group chats.'
        )
        return

    # If the user is not registered, we cannot start a chat. We ask him to register.
    if user is None:
        logging.info(f'Command from an unregistered user. '
                     f'The command cannot be executed. '
                     f'User ID: \'{update.effective_user.id}\'.')
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text='🟧You must be registered to run this command. Use \'/start\'.'
        )
        return

    # If the user is already in a chat room, we cannot add him/her again. We notify him/her of this.
    if chats.user_chat(user.user_id) is not None:
        logging.info(f'The user is already in the chat, we can\'t add him. User ID: \'{user.user_id}\'.')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='🟧You are already in chat.')
        return

    # Looking for a chat room among those already created.
    suitable_chat = chats.suitable_chat(database.get_user(user.user_id))

    # If no suitable chat room was found, a new one is created specifically for the user.
    if suitable_chat is None:
        chats.append_chat(Chat([user]))
        logging.info(f'The user has been successfully added to the queue. User ID: \'{user.user_id}\'.')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='⏳You have been successfully added to the queue.'
        )
        return

    # If a suitable chat room is found, the user is added there.
    suitable_chat.append_user(user)
    logging.info(f'The user has been successfully added to the queue. User ID: \'{user.user_id}\'.')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='⏳You have been successfully added to the queue.'
    )

    # If the chat was started, we send a message about it to all chat users.
    if suitable_chat.started:
        for user in suitable_chat.users:
            logging.info(f'Chat was successfully found for user. User ID: \'{user.user_id}\'.')
            await context.bot.send_message(chat_id=user.user_id, text='🟩Interlocutor found.')


# Handler that handles the '/start_chatting' command.
start_chatting_command_handler = CommandHandler(
    command='start_chatting',
    callback=start_chatting_callback
)
