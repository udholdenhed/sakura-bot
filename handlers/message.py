import logging
from shared_vars import cities
# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.ext import filters, CallbackContext, MessageHandler

from utils import find_city
from shared_vars import chats, users_who_change_city, database


async def message_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """
    This function is used to process any message of the user,
    including messages to the interlocutor when the user is in the chat.

    Not recommended for use without a 'MessageHandler'.
    """

    logging.info(f'Message from user. User ID: \'{update.effective_user.id}\'.')

    user_id = update.effective_user.id
    if user_id in users_who_change_city.keys():
        await change_city(user_id, update.effective_chat.id, update.effective_message.text, context)
        return

    chat = chats.user_chat(user_id)
    if chats.user_chat(user_id) is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='🟧Unknown message or command.')
        return

    if chat is None or not chat.started:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='🟧Unknown message or command.')
        return

    # If the user is in a chat room, we will send him a message from the interlocutor.
    for user in chat.users:
        if user.user_id == user_id:
            continue

        if update.effective_message.audio is not None:
            await context.bot.send_audio(chat_id=user.user_id, audio=update.effective_message.audio.file_id)
        elif update.effective_message.document is not None:
            await context.bot.send_document(chat_id=user.user_id, document=update.effective_message.document.file_id)
        elif update.effective_message.animation is not None:
            await context.bot.send_animation(chat_id=user.user_id, animation=update.effective_message.animation.file_id)
        elif len(update.effective_message.photo) != 0:
            await context.bot.send_photo(chat_id=user.user_id, photo=update.effective_message.photo[0])
        elif update.effective_message.sticker is not None:
            await context.bot.send_sticker(chat_id=user.user_id, sticker=update.effective_message.sticker.file_id)
        elif update.effective_message.video is not None:
            await context.bot.send_video(chat_id=user.user_id, video=update.effective_message.video.file_id)
        elif update.effective_message.video_note is not None:
            await context.bot.send_video_note(
                chat_id=user.user_id,
                length=update.effective_message.video_note.length,
                video_note=update.effective_message.video_note.file_id
            )
        elif update.effective_message.voice is not None:
            await context.bot.send_voice(chat_id=user.user_id, voice=update.effective_message.voice.file_id)
        elif update.effective_message.text is not None:
            await context.bot.send_message(chat_id=user.user_id, text=update.effective_message.text)


async def change_city(user_id: int, chat_id: int, city: str, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = database.get_user(user_id)
    change_for = users_who_change_city[user_id]

    city = find_city(city)
    if type(city) == list:
        if len(city) == 0:
            await context.bot.send_message(chat_id=chat_id, text='🟧Please enter the city correctly!')
            return

        index = cities.index(city[-1])
        city = cities[index - 2:index + 2]
        await context.bot.send_message(chat_id=chat_id, text='🟧Maybe you would like to choose one of this cities:')
        for c in city:
            await context.bot.send_message(chat_id=chat_id, text=c["city"])
        return

    if change_for == 'user':
        user.user_city = city
    elif change_for == 'interlocutor':
        user.interlocutor_city = city

    users_who_change_city.pop(user_id)
    if not database.save_user(user):
        logging.info(f'Failed to save settings. User ID: \'{user.user_id}\'.')
        await context.bot.send_message(chat_id=chat_id, text='🟥Failed to save settings. Please try again.')

    await context.bot.send_message(chat_id=chat_id, text='🟩Settings was saved successfully.')


# This handler handles any user message in the local chat, except commands.
message_handler = MessageHandler(
    filters=filters.CHAT & ~filters.COMMAND,
    callback=message_callback
)
