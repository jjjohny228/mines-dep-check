from typing import Generator
from datetime import datetime, timedelta

from .models import User, WinId
from .reflink import increase_users_count


# region SQL Create

def create_user_if_not_exist(telegram_id: int, name: str, reflink: str = None) -> bool:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(name=name, telegram_id=telegram_id, referral_link=reflink)
        increase_users_count(reflink=reflink)
        return True
    return False


# endregion


# region SQL Select


def get_users_total_count() -> int:
    return User.select().count()


def get_users_by_hours(hours: int):
    start_time = datetime.now() - timedelta(hours=hours)
    users_count = User.select().where(User.registration_timestamp >= start_time).count()

    return users_count


def get_user_ids() -> Generator:
    yield from (user.telegram_id for user in User.select())


def get_all_users() -> tuple:
    yield from ((user.telegram_id, user.name, user.referral_link, user.registration_timestamp, user.language_code) for
                user in User.select())


def get_user_by_telegram_id_or_none(telegram_id: int) -> None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_locale(telegram_id: int) -> str | None:
    try:
        return User.get(User.telegram_id == telegram_id).language_code
    except User.DoesNotExist:
        return None


def check_user_registration(telegram_id: int) -> int:
    return User.get(User.telegram_id == telegram_id).onewin_id is not None


def check_user_deposit(telegram_id: int) -> int:
    return User.get(User.telegram_id == telegram_id).deposit

# endregion


# region Update


def set_1win_id(onewin_id: int):
    WinId.create(onewin_id=onewin_id)


def set_1win_deposit(onewin_id: int):
    user, created = User.get_or_create(onewin_id=onewin_id, defaults={'deposit': True})
    if not created:
        user.deposit = True
        user.save()


def check_onewin_id(onewin_id: int):
    onewin_object = WinId.get_or_none(onewin_id=onewin_id)
    return onewin_object is not None


def set_user_1win_id(telegram_id: int, onewin_id: int):
    User.update(onewin_id=onewin_id).where(User.telegram_id == telegram_id).execute()


def set_locale(telegram_id: int, language_code: str) -> None:
    User.update(language_code=language_code).where(User.telegram_id == telegram_id).execute()

# endregion
