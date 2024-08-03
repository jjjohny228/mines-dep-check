import os
import random
import datetime
import random

from aiogram.types import InputFile
from aiogram.utils.markdown import quote_html

from config import Config


class Messages:
    # Статья с фото:  https://telegra.ph/Resources-Mines-John-01-12

    @staticmethod
    def get_loading() -> str:
        return '♻ Loading...'

    @staticmethod
    def ask_for_locale() -> str:
        return 'Выберите язык ⬇ \n' \
               'Choose your language ⬇'

    @staticmethod
    def get_welcome() -> str:
        return (
            'Welcome to PUFFS🤖MINES \n\nThis bot is designed to hack the game MINES💣 \nThe bot is based on Open Ai and produces correct signals with an 85% chance. '
            'Hacking takes place in online time. '
            '\n\nBefore using the bot, you must read the instructions📖')

    @staticmethod
    def get_welcome_video_url() -> str:
        return 'https://telegra.ph/file/981a5c31bbca214b69861.mp4'

    @staticmethod
    def get_registration_text(username) -> str:
        return (f'👋 Hello! {username if username else ""}\n\n'
                'To apply the effectiveness of using this bot, you need to adjust the following steps:\n\n'
                '1️⃣Register a new account - if you already have an account, please '
                'leave it and register a new account.\n\n'
                '2️⃣ Use the “10112002”promotional code when registering a new account. '
                'This is important, since our AI only works with new accounts.\n\n'
                '3️⃣ After registration, click on the "Check registration" button.\n\n'
                '4️⃣ If you do not complete these steps, our bot will not be able to add your account to its data resources, and the signals it provides may not be captured.\n\nThank you for your understanding!')

    @staticmethod
    def get_registration_photo_url() -> str:
        return ('https://www.google.com/url?sa=i&url=https%3A%2F%2F1win-uz-online.com%2Fmines-pro%2F&psig='
                'AOvVaw2pavLGR1rvH2aFy4WLuy_x&ust=1715107100965000&source=images&cd=vfe&opi=89978449&ved='
                '0CBIQjRxqFwoTCLCemP7V-YUDFQAAAAAdAAAAABAJ')

    @staticmethod
    def get_registration_explanation_photo() -> str:
        return 'https://habrastorage.org/webt/27/zc/fv/27zcfvm2riwlgvq6sgx06zjs9fc.png'

    @staticmethod
    def get_deposit_text() -> str:
        return (f'Amazing! You have successfully registered.\n\n'
                f'1⃣It remains to top up your balance in the amount of $10-30\n\n'
                f'2⃣ After replenishment, click the "Check deposit" button')

    @staticmethod
    def get_deposit_explanation_photo() -> str:
        return 'https://telegra.ph/file/e4f6e42224410dfbc2ed4.png'

    @staticmethod
    def get_instruction_text() -> str:
        return (
            "The bot is based on and trained using OpenAI's neural network cluster 🖥[ChatGPT-v4].\n\nFor training, the bot played 🎰over 8000 games.\nCurrently, bot users successfully make 20-30% of their 💸 capital daily!\n\nThe bot is still learning, and its accuracy is at 87%!\n\n Follow these instructions for maximum profit: \n\n📲 First, you need to register for 1WIN. In order for the bot to successfully verify registration, important conditions must be met: \n\n❗️ The account must be NEW! \n\n - If you already have an account and when you click on the REGISTRATION button you are taken to the old one, you need to log out of it and click on the REGISTRATION button again, and then register again! \n\n1️⃣  Register at the 1WIN. If it doesn’t open - use a VPN (Sweden). I use VPN Super Unlimited Proxy\n\n2️⃣After registration, make a deposit to your NEW account. Minimum 10$ - 30$ for best results.\n\n3️⃣ Go to the 1win games section and select the 💣'MINES' game.\n\n4️⃣ Set the number of traps to three. This is important!\n\n5️⃣ Request a signal from the bot and place bets based on the bot’s signals.\n\n6️⃣ In case of a losing signal, we advise you to double (X2) your bet to fully cover the loss in the next signal.")

    @staticmethod
    def get_instruction_photo() -> str:
        return ('https://telegra.ph/file/eb39ec16e4482eb8c77b0.jpg')

    @staticmethod
    def get_signal_text() -> str:
        return (f'Game {random.randint(100, 1000)}💎 {datetime.date.today().strftime("%d.%m.%Y")}\n\n'
                f'Win Probability {round(random.uniform(97, 99.89), 2)}%')

    # @staticmethod
    # def ask_for_code_word() -> str:
    #     return '<b>✅ ВВЕДИТЕ ПАРОЛЬ:</b>'
    #
    # @staticmethod
    # def get_code_word_incorrect():
    #     return '❗Неверный пароль, попробуйте ещё раз:'

    @staticmethod
    def ask_for_1win_id() -> str:
        return (
            '<b>Write your account ID \n'
            'that you have created 🆔</b> \n'
            '<i>(example: 58367211)</i>'
        )
    #
    @staticmethod
    def get_1win_id_incorrect_length() -> str:
        return '❗The ID must be 8 or 9 digits long. Try again:'

    @staticmethod
    def get_1win_id_have_forbidden_symbols() -> str:
        return '❗The ID can only consist of numbers. Try again:'

    @staticmethod
    def get_deposit_success() -> str:
        return 'You have deposited successfully! Click "Get Signal👇🏻"'

    @staticmethod
    def get_registration_failure() -> str:
        return """You didn't register🚫, try again"""

    @staticmethod
    def get_deposit_failure() -> str:
        return """You didn't deposited🚫, try again"""

    @staticmethod
    def get_throttled_error() -> str:
        return 'Please, not so often 🙏'

    @staticmethod
    def get_random_signal() -> InputFile:
        images_dir_path = Config.SIGNALS_IMAGES_DIR
        files = [
            filename for filename in os.listdir(images_dir_path)
        ]

        random_filename = random.choice(files)
        return InputFile(path_or_bytesio=os.path.join(images_dir_path, random_filename))
