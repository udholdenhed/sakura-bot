import logging
# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.constants import ChatType
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CommandHandler

from shared_vars import chats


async def stop_chatting_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """
    This function is need to be called on the user command '/stop_chatting'.

    If the user is in a chat or queue it removes him from there.
    If this command is called in a group chat, it sends a message that it cannot be executed there.
    If the user is not registered (not saved in the database), we send him a request to do so.
    If the user is not in the chat, we inform him about it.

    Not recommended for use without a 'CommandHandler'.
    """

    user_id = update.effective_user.id
    logging.info(f'Command \'stop_chatting\'. User ID: \'{user_id}\'.')

    # This command cannot be used in group chats. Therefore, we inform the user about it.
    if update.effective_chat.type == ChatType.GROUP:
        logging.info('\'stop_chatting\' command cannot be used in group chats.')
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='🟧This command cannot be used in group chats.')
        return

    logging.info(f'Deleting a user from chat. User ID: \'{user_id}\'.')
    # We are looking for the chat room the user is in. If we don't find it, the 'chat' variable will be empty.
    chat = chats.user_chat(user_id)

    # If the user is not in a chat, we do not need to end any chat.
    if chat is None:
        logging.info(f'The user is not in the chat, so it cannot be deleted. User ID: \'{user_id}\'.')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='🟧You are not in a chat room.')
        return

    # If the chat has not yet started, we simply remove the user from the queue.
    if not chat.started:
        chat.remove_user(user_id)
        logging.info(f'Users have been successfully deleted from the queue. User ID: \'{user_id}\'.')

        # If the chat that the user was in is empty after deleting it, we delete that chat as well.
        if len(chat.users) == 0:
            chats.remove_chat(chat.id)
            logging.info(f'Since the chat is completely empty after deleting a user, we delete it. Chat ID: {chat.id}')
        await context.bot.send_message(chat_id=user_id, text='🟧The search for the interlocutor is stopped.')
        return

    chat.remove_user(user_id)
    # Sends to the user who finished the chat that he did it successfully.
    await context.bot.send_message(chat_id=user_id, text='🟥Chat with the user has been terminated.')

    # If there are users in the chat room, we let them know that someone is out.
    if len(chat.users) > chat.MIN_NUMBER_OF_USERS:
        for user in chat.users:
            await context.bot.send_message(chat_id=user.user_id, text='🟥A user has left the chat room.')
        return

    # If there is a minimum number of users left in the chat room, we commit it and inform the users about it.
    for user in chat.users:
        await context.bot.send_message(chat_id=user.user_id, text='🟥User has ended the chat.')
    chats.remove_chat(chat.id)
    logging.info('Since the chat was empty, it was deleted')


# Handler that handles the '/stop_chatting' command.
stop_chatting_command_handler = CommandHandler(
    command='stop_chatting', callback=stop_chatting_callback
)
