from aiogram import types

from src.database.admin import get_admin_ids
from config import Config


async def check_is_admin(message: types.Message):
    return message.from_user.id in {*get_admin_ids(), *Config.ADMIN_IDS}
