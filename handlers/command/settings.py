import logging

# noinspection PyPackageRequirements
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CommandHandler

from shared_vars import database

SETTINGS_KEYBOARD_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text='🧍Age', callback_data='user_age_keyboard_markup'),
            InlineKeyboardButton(text='🧍Sex', callback_data='user_sex_keyboard_markup'),
            InlineKeyboardButton(text='🧍City', callback_data='user_city_keyboard_markup')

        ],
        [
            InlineKeyboardButton(text='🗺️Interlocutor Age', callback_data='interlocutor_age_keyboard_markup'),
            InlineKeyboardButton(text='🗺️Interlocutor Sex', callback_data='interlocutor_sex_keyboard_markup'),
            InlineKeyboardButton(text='🗺️Interlocutor City', callback_data='interlocutor_city_keyboard_markup')
        ],

        [
            InlineKeyboardButton(text='🟥Close', callback_data='close')
        ]
    ]
)


async def settings_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Command \'settings\'. User ID: \'{update.effective_user.id}\'.')
    user = database.get_user(update.effective_user.id)
    if user is None:
        logging.info(f'Command from an unregistered user. The command cannot be executed.'
                     f'User ID: \'{update.effective_user.id}\'.')
        await context.bot.send_message(chat_id=update.effective_user.id,
                                       text='🟧You must be registered to run this command. Use \'/start\'.')
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='🔧Setting.',
        reply_markup=SETTINGS_KEYBOARD_MARKUP
    )


# Handler that handles the '/settings' command.
settings_command_handler = CommandHandler(
    command='settings',
    callback=settings_callback
)
