import asyncio
import random
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from src.database.user import (create_user_if_not_exist, set_user_1win_id, check_user_registration,
                               check_user_deposit, set_1win_id, check_onewin_id, set_1win_deposit)
from src.utils import send_typing_action
from src.misc import UserDataInputting
from .messages import Messages
from src.filters.filter_func import check_is_admin
from src.handlers.admin.admin import send_admin_menu
from .kb import Keyboards
from config import Config
from src.utils import logger
from src.create_bot import bot


# async def send_before_start(to_message):
#     await to_message.answer_photo(
#         caption=Messages.get_before_game_start(),
#         reply_markup=Keyboards.get_first_signal_markup(),
#         photo=Messages.get_before_game_start_photo()
#     )


# region Handlers

async def __handle_start_command(message: Message) -> None:
    if await check_is_admin(message):
        await send_admin_menu(message)
    else:
        await send_typing_action(message)

        create_user_if_not_exist(
            telegram_id=message.from_id,
            name=message.from_user.username or message.from_user.full_name,
            reflink=message.get_full_command()[1]
        )

        await message.answer_video(
            video=Messages.get_welcome_video_url(),
            caption=Messages.get_welcome(),
            reply_markup=Keyboards.get_welcome_menu()
        )


async def __handle_new_registered_mammoth(message: Message) -> None:
    onewin_id = int(re.search(r'\d+', message.text).group())
    admin_ids = Config.ADMIN_IDS
    if not check_onewin_id(onewin_id):
        try:
            for user_id in admin_ids:
                await bot.send_message(chat_id=user_id, text=f'Зарегистрировался новый пользователь с id: {onewin_id}')
                await asyncio.sleep(0.05)
        finally:
            logger.info(f'Рассылка закончилась.')
        set_1win_id(onewin_id)


async def __handle_new_deposit(message: Message) -> None:
    _, onewin_id, amount = message.text.split('_')
    admin_ids = Config.ADMIN_IDS
    set_1win_deposit(onewin_id)
    try:
        for user_id in admin_ids:
            await bot.send_message(chat_id=user_id, text=f'Польователь с id {onewin_id} оформил депозит {amount}')
            await asyncio.sleep(0.05)
    finally:
        logger.info(f'Рассылка закончилась.')


async def __handle_start_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer_video(
        video=Messages.get_welcome_video_url(),
        caption=Messages.get_welcome(),
        reply_markup=Keyboards.get_welcome_menu()
    )
    await callback.answer()


async def __handle_registration_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_photo(
        caption=Messages.get_registration_text(callback.message.chat.first_name),
        photo=Messages.get_registration_explanation_photo(),
        reply_markup=Keyboards.get_registration_menu()
    )
    await state.finish()
    await callback.answer()


async def __handle_instruction_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=Messages.get_instruction_text(),
        reply_markup=Keyboards.get_instruction_menu()
    )
    await callback.answer()


async def __handle_check_registration_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=Messages.ask_for_1win_id()
    )
    await state.set_state(await UserDataInputting.first())
    await callback.answer()


async def __handle_user_id_message(message: Message, state: FSMContext):
    await send_typing_action(message)

    if not message.text.isdigit():
        await message.answer(Messages.get_1win_id_have_forbidden_symbols())
        return
    if len(message.text) not in (8, 9):
        await message.answer(Messages.get_1win_id_incorrect_length())
        return

    if check_onewin_id(int(message.text)):
        set_user_1win_id(message.from_user.id, message.text)
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=Messages.get_deposit_explanation_photo(),
                             caption=Messages.get_deposit_text(),
                             reply_markup=Keyboards.get_deposit_markup())
        await state.finish()

    else:
        await message.answer_photo(
            caption=Messages.get_registration_failure(),
            photo=Messages.get_registration_explanation_photo(),
            reply_markup=Keyboards.get_registration_menu()
        )
        await state.finish()
        return


async def __handle_check_deposit_callback(callback: CallbackQuery, state: FSMContext):
    if check_user_deposit(callback.message.chat.id):
        await bot.send_message(chat_id=callback.from_user.id,
                               text=Messages.get_deposit_success(),
                               reply_markup=Keyboards.get_signal_markup())
    else:
        await callback.message.answer(
            text=Messages.get_deposit_failure(),
            reply_markup=Keyboards.get_deposit_markup()
        )
    await callback.answer()


async def __handle_next_signal_callback(callback: CallbackQuery):
    # Удаляем сообщение
    await callback.answer(text=Messages.get_loading())
    await callback.message.edit_reply_markup(reply_markup=None)
    msg = await callback.message.answer('1️⃣2️⃣3️⃣')
    delay_seconds = 0.4

    for i in range(1, random.randint(2, 4)):
        await asyncio.sleep(delay_seconds)
        await msg.edit_text('1️⃣')
        await asyncio.sleep(delay_seconds)
        await msg.edit_text('1️⃣2️⃣')
        await asyncio.sleep(delay_seconds)
        await msg.edit_text('1️⃣2️⃣3️⃣')
    await msg.delete()

    if check_user_registration(callback.message.chat.id) and check_user_deposit(callback.message.chat.id):
        new_photo = Messages.get_random_signal()

        await callback.message.answer_photo(photo=new_photo,
                                            caption=Messages.get_signal_text(),
                                            reply_markup=Keyboards.get_signal_markup())
    else:
        await callback.message.answer_photo(
            caption=Messages.get_registration_text(callback.message.chat.first_name),
            photo=Messages.get_registration_explanation_photo(),
            reply_markup=Keyboards.get_registration_menu()
        )
# endregion


def register_user_handlers(dp: Dispatcher) -> None:
    # обработка команды /start
    dp.register_message_handler(__handle_start_command, CommandStart())
    dp.register_callback_query_handler(__handle_start_callback, text='client_menu', state=None)
    dp.register_callback_query_handler(__handle_check_registration_callback, text='check_registration', state=None)
    dp.register_callback_query_handler(__handle_check_deposit_callback, text='check_deposit', state=None)
    dp.register_message_handler(__handle_user_id_message, state=UserDataInputting.wait_for_id)
    dp.register_channel_post_handler(__handle_new_registered_mammoth, lambda text: text.text.startswith("registered"))
    dp.register_channel_post_handler(__handle_new_deposit, lambda text: text.text.startswith("deposit"))

    # обработка кнопок приветственного меню
    dp.register_callback_query_handler(__handle_registration_menu_callback, text='registration_menu', state=None)
    dp.register_callback_query_handler(__handle_instruction_callback, text='instruction_menu', state=None)

    # обработка нажатия на Следующий сигнал
    dp.register_callback_query_handler(__handle_next_signal_callback, text='next_signal')
