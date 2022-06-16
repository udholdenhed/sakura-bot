import logging

# noinspection PyPackageRequirements
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CallbackQueryHandler

from shared_vars import users_who_change_city, chats, database

USER_AGE_KEYBOARD_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text='🧍+14', callback_data='change_user_age:less_than_fourteen'),
            InlineKeyboardButton(text='🧍14-16', callback_data='change_user_age:fourteen_sixteen')
        ],
        [
            InlineKeyboardButton(text='🧍16-18', callback_data='change_user_age:sixteen_eighteen'),
            InlineKeyboardButton(text='🧍18+', callback_data='change_user_age:eighteen_or_more')
        ],
        [
            InlineKeyboardButton(text='🧍Not specified', callback_data='change_interlocutor_age:not_specified')
        ],
        [
            InlineKeyboardButton(text='🟥Close', callback_data='close')
        ]
    ]
)

USER_SEX_KEYBOARD_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text='🧍‍♂️Male', callback_data='change_user_sex:male'),
            InlineKeyboardButton(text='🧍‍♀️Female', callback_data='change_user_sex:female')
        ],
        [
            InlineKeyboardButton(text='🟥Close', callback_data='close')
        ]
    ]
)

INTERLOCUTOR_AGE_KEYBOARD_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text='🗺️+14', callback_data='change_interlocutor_age:less_than_fourteen'),
            InlineKeyboardButton(text='🗺️14-16', callback_data='change_interlocutor_age:fourteen_sixteen')
        ],
        [
            InlineKeyboardButton(text='🗺️16-18', callback_data='change_interlocutor_age:sixteen_eighteen'),
            InlineKeyboardButton(text='🗺️18+', callback_data='change_interlocutor_age:eighteen_or_more')
        ],
        [
            InlineKeyboardButton(text='🗺️Not specified', callback_data='change_interlocutor_age:not_specified')
        ],
        [
            InlineKeyboardButton(text="🟥Close", callback_data='close')
        ]
    ]
)

INTERLOCUTOR_SEX_KEYBOARD_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text='🧍‍♂️Male', callback_data='change_interlocutor_sex:male'),
            InlineKeyboardButton(text='🧍‍♀️Female', callback_data='change_interlocutor_sex:female')
        ],
        [
            InlineKeyboardButton(text='🟥Close', callback_data='close')
        ]
    ]
)


async def query_keyboard_markup_user_age(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Query keyboard markup user age. User ID: \'{update.effective_user.id}\'.')
    await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.message_id,
        reply_markup=USER_AGE_KEYBOARD_MARKUP
    )


async def query_keyboard_markup_user_sex(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Query keyboard markup user sex. User ID: \'{update.effective_user.id}\'.')
    await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.message_id,
        reply_markup=USER_SEX_KEYBOARD_MARKUP
    )


async def query_keyboard_markup_user_city(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Query keyboard markup user city. User ID: \'{update.effective_user.id}\'.')
    await query_keyboard_markup_city(update, context, 'user')


async def query_keyboard_markup_interlocutor_age(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Query keyboard markup interlocutor age. User ID: \'{update.effective_user.id}\'.')
    await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.message_id,
        reply_markup=INTERLOCUTOR_AGE_KEYBOARD_MARKUP
    )


async def query_keyboard_markup_interlocutor_sex(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Query keyboard markup interlocutor sex. User ID: \'{update.effective_user.id}\'.')
    await context.bot.edit_message_reply_markup(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.message_id,
        reply_markup=INTERLOCUTOR_SEX_KEYBOARD_MARKUP
    )


async def query_keyboard_markup_interlocutor_city(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Query keyboard markup interlocutor city. User ID: \'{update.effective_user.id}\'.')
    await query_keyboard_markup_city(update, context, 'interlocutor')


async def query_close_callback(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Close callback. User ID: \'{update.effective_user.id}\'.')
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)


async def query_keyboard_markup_city(update: Update, context: CallbackContext.DEFAULT_TYPE, change_for: str) -> None:
    if chats.user_chat(update.effective_user.id) is not None:
        logging.info('You can\'t change change city when you\'re in chat.')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='🟧You can\'t change change city when you\'re in chat.'
        )
        await update.callback_query.answer()
        return

    user = database.get_user(update.effective_user.id)
    if user is None:
        logging.info(f'Command from an unregistered user. '
                     f'The command cannot be executed. '
                     f'User ID: \'{update.effective_user.id}\'.')
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text='🟧You must be registered to run this command. Use \'/start\'.'
        )
        await update.callback_query.answer()
        return

    if update.effective_user.id in users_who_change_city:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='🟧You are changing your city at the moment!')
        return

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='🟩If you want to stay private enter \'not specified\'.')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='🟩Enter your city in next message:')
    await update.callback_query.answer()

    users_who_change_city[update.effective_user.id] = change_for


query_handler_user_age_keyboard_markup = CallbackQueryHandler(
    callback=query_keyboard_markup_user_age,
    pattern=r'user_age_keyboard_markup'
)

query_handler_user_city_keyboard_markup = CallbackQueryHandler(
    callback=query_keyboard_markup_user_city,
    pattern=r'user_city_keyboard_markup'
)

query_handler_user_sex_keyboard_markup = CallbackQueryHandler(
    callback=query_keyboard_markup_user_sex,
    pattern=r'user_sex_keyboard_markup'
)

query_handler_interlocutor_age_keyboard_markup = CallbackQueryHandler(
    callback=query_keyboard_markup_interlocutor_age,
    pattern=r'interlocutor_age_keyboard_markup'
)

query_handler_interlocutor_city_keyboard_markup = CallbackQueryHandler(
    callback=query_keyboard_markup_interlocutor_city,
    pattern=r'interlocutor_city_keyboard_markup'
)

query_handler_interlocutor_sex_keyboard_markup = CallbackQueryHandler(
    callback=query_keyboard_markup_interlocutor_sex,
    pattern=r'interlocutor_sex_keyboard_markup'
)

query_handler_close = CallbackQueryHandler(
    callback=query_close_callback,
    pattern=r'close'
)
