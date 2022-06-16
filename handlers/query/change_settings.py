import re
import logging

# noinspection PyPackageRequirements
from telegram import Update
# noinspection PyPackageRequirements
from telegram.ext import CallbackContext, CallbackQueryHandler

from shared_vars import database


async def query_change_setting(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    logging.info(f'Change user or interlocutor sex callback. User ID: \'{update.effective_user.id}\'.')
    user = database.get_user(update.effective_user.id)
    if user is None:
        logging.info(f'Callback from an unregistered user. User ID: \'{update.effective_user.id}\'.')
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text='🟧You must be registered to change settings. Use \'/start\'.'
        )
    else:
        setting_to_change = re.search(r'age|sex|city', update.callback_query.data).group()  # has changed |city
        new_setting = re.search(r'(?<=:).*$', update.callback_query.data).group()
        change_for = re.search(r'user|interlocutor', update.callback_query.data).group()
        match setting_to_change:
            case 'age':
                if change_for == 'user':
                    user.user_age = new_setting
                elif change_for == 'interlocutor':
                    user.interlocutor_age = new_setting
            case 'sex':
                if change_for == 'user':
                    user.user_sex = new_setting
                elif change_for == 'interlocutor':
                    user.interlocutor_sex = new_setting
            case 'city':
                if change_for == 'user':
                    user.user_city = new_setting
                elif change_for == 'interlocutor':
                    user.interlocutor_city = new_setting

        if not database.save_user(user):
            logging.info(f'Failed to save settings. User ID: \'{user.user_id}\'.')
            await context.bot.answer_callback_query(
                callback_query_id=update.callback_query.id,
                text='🟥Failed to save settings. Please try again.'
            )
            return

        logging.info(f'Settings successfully saved. User ID: \'{user.user_id}\'.')
        await context.bot.answer_callback_query(
            callback_query_id=update.callback_query.id,
            text='🟩Settings successfully saved.'
        )


query_handler_change_settings = CallbackQueryHandler(
    callback=query_change_setting,
    pattern=r'change_.*'
)
