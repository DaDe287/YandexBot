from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇰🇬 Кыргызча", callback_data="lang_ky")],
        [InlineKeyboardButton(text="🇺🇿 Oʻzbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇰🇿 Қазақ тілі", callback_data="lang_kk")],
        [InlineKeyboardButton(text="🇧🇾 Беларуская", callback_data="lang_be")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇦🇿 Azərbaycan", callback_data="lang_az")],
        [InlineKeyboardButton(text="📲 Написать оператору", callback_data="operator")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
    ]
)

country_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Россия", callback_data="country_ru")],
        [InlineKeyboardButton(text="🇰🇬 Кыргызстан", callback_data="country_ky")],
        [InlineKeyboardButton(text="🇺🇿 Oʻzbekiston", callback_data="country_uz")],
        [InlineKeyboardButton(text="🇧🇾 Беларусь", callback_data="country_be")],
        [InlineKeyboardButton(text="🇰🇿 Қазақстан", callback_data="country_kk")],
        [InlineKeyboardButton(text="🌏 Bot languge | Язык бота", callback_data="choose_languge")]
    ]
)




REGISTRATION_LINKS = {
    "ru": "https://reg.eda.yandex.ru/?advertisement_campaign=forms_for_agents&user_invite_code=a638a2ac0cf74a0d8f9d49d59f47ae95&utm_source=multibot&utm_content=regbutton",
    "uz": "https://reg.eda.yandex.uz/?advertisement_campaign=forms_for_agents&user_invite_code=04df63bdec174f429c7c84d705b038f3utm_source=multibot&utm_content=regbutton",
    "ky": "https://reg.eda.yandex.kg/?advertisement_campaign=forms_for_agents&user_invite_code=04df63bdec174f429c7c84d705b038f3utm_source=multibot&utm_content=regbutton",
    "be": "https://reg.eda.yandex.by/?advertisement_campaign=forms_for_agents&user_invite_code=04df63bdec174f429c7c84d705b038f3utm_source=multibot&utm_content=regbutton",
    "kz": "https://reg.eda.yandex.kz/?advertisement_campaign=forms_for_agents&user_invite_code=04df63bdec174f429c7c84d705b038f3utm_source=multibot&utm_content=regbutton",
    "az": "https://t.me/m/POUmOEUxNjky"
}
def country_actions_keyboard(country_code: str):
    registration_url = REGISTRATION_LINKS.get(country_code, REGISTRATION_LINKS["ru"])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚀 Быстрая регистрация", url=registration_url)
        ],
        [
            InlineKeyboardButton(text="🤝🏼 Позвать друга", switch_inline_query="invite")  # пользователю предложит выбрать чат для пересылки
        ],
        [
            InlineKeyboardButton(text="🌍 Работа в других странах", callback_data="back_to_countries")
        ],
        [
            InlineKeyboardButton(text="📲 Написать оператору", url="https://t.me/m/POUmOEUxNjky")
        ]
    ])
    return keyboard