import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData


class Keyboards:
    locale_callback_data = CallbackData('locale', 'language_code')

    # region Subchecking

    check_sub_button = InlineKeyboardButton(text='❓ Проверить ❓', callback_data='checksubscription')

    @classmethod
    def get_not_subbed_markup(cls, channels_to_sub_data) -> InlineKeyboardMarkup | None:
        if len(channels_to_sub_data) == 0:
            return None

        cahnnels_markup = InlineKeyboardMarkup(row_width=1)
        [
            cahnnels_markup.add(InlineKeyboardButton(channel_data.get('title'), url=channel_data.get('url')))
            for channel_data in channels_to_sub_data
        ]
        cahnnels_markup.add(cls.check_sub_button)
        return cahnnels_markup

    # endregion

    @staticmethod
    def get_welcome_menu() -> InlineKeyboardMarkup:
        registration_button = InlineKeyboardButton('Registration📱', callback_data='registration_menu')
        instruction_button = InlineKeyboardButton('Instruction📖', callback_data='instruction_menu')
        get_signal_button = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='next_signal')
        return InlineKeyboardMarkup(row_width=2).add(registration_button, instruction_button).add(get_signal_button)

    @staticmethod
    def get_registration_menu() -> InlineKeyboardMarkup:
        registration_button = InlineKeyboardButton('🔗Registration', url=os.getenv('REF_URL', 'Впишите реферальную ссылку'))
        check_registration_button = InlineKeyboardButton('🔎Check Registration', callback_data='check_registration')
        menu_button = InlineKeyboardButton('Menu', callback_data='client_menu')
        return InlineKeyboardMarkup(row_width=1).add(registration_button, check_registration_button, menu_button)

    @staticmethod
    def get_signal_menu() -> InlineKeyboardMarkup:
        get_signal_button = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='next_signal')
        return InlineKeyboardMarkup(row_width=1).add(get_signal_button)

    @staticmethod
    def get_instruction_menu() -> InlineKeyboardMarkup:
        menu_button = InlineKeyboardButton('Menu', callback_data='client_menu')
        return InlineKeyboardMarkup(row_width=1).add(menu_button)

    @staticmethod
    def get_signal_markup() -> InlineKeyboardMarkup:
        next_signal = InlineKeyboardButton('🔻 GET SIGNAL 🔻', callback_data='next_signal')
        return InlineKeyboardMarkup(row_width=2).add(next_signal)

    @staticmethod
    def get_deposit_markup() -> InlineKeyboardMarkup:
        next_signal = InlineKeyboardButton('Check deposit ✅', callback_data='check_deposit')
        return InlineKeyboardMarkup(row_width=2).add(next_signal)

