import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboard.keyboard import language_keyboard, country_keyboard, country_actions_keyboard
from lexicon.lexicon import LANG_MAP, LEXICON, COUNTRY_MESSAGES
from db.user_language import user_languages
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext):

    user_id = message.from_user.id
    # язык по умолчанию — русский
    lang_code = user_languages.get(user_id, "ru")

    # берём приветственное сообщение из LEXICON
    start_text = LEXICON.get(lang_code, LEXICON["ru"]).get("start")

    photo_path = "images/photo_2025-09-23_12-26-59.jpg"
    img = FSInputFile(photo_path)
    bot_msg = await message.answer_photo(
        photo=img,
        caption=start_text,
        reply_markup=country_keyboard
    )
    print(1)
    await state.update_data(last_msg_id=bot_msg.message_id)

@router.callback_query(F.data == "back")
async def back_message(callback: CallbackQuery, state: FSMContext):

    user_id = callback.from_user.id
    data = await state.get_data()
    last_msg_id = data["last_msg_id"]
    if last_msg_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=int(last_msg_id)
            )
            await state.clear()
        except Exception:
            pass 
    # язык по умолчанию — русский
    lang_code = user_languages.get(user_id, "ru")

    # берём приветственное сообщение из LEXICON
    start_text = LEXICON.get(lang_code, LEXICON["ru"]).get("start")

    photo_path = "images/photo_2025-09-23_12-26-59.jpg"
    img = FSInputFile(photo_path)
    bot_msg = await callback.message.answer_photo(
        photo=img,
        caption=start_text,
        reply_markup=country_keyboard
    )
    await state.update_data(last_msg_id=bot_msg.message_id)

@router.message(Command("lang"))
async def cmd_lang(message: Message, state: FSMContext):
    user_id = message.from_user.id

    data = await state.get_data()
    last_msg_id = data["last_msg_id"]
    if last_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=int(last_msg_id)
            )
            await state.clear()
        except Exception:
            pass 

    # если язык ещё не выбран — ставим по умолчанию русский
    if user_id not in user_languages:
        user_languages[user_id] = "ru"

    bot_msg = await message.answer(
        text=LEXICON["ru"]["chosen"],
        reply_markup=language_keyboard
    )
    await state.update_data(last_msg_id=bot_msg.message_id)

@router.callback_query(F.data == "choose_languge")
async def chosose_lang(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    data = await state.get_data()
    last_msg_id = data["last_msg_id"]
    if last_msg_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=int(last_msg_id)
            )
            await state.clear()
        except Exception:
            pass 

    # если язык ещё не выбран — ставим по умолчанию русский
    if user_id not in user_languages:
        user_languages[user_id] = "ru"

    bot_msg = await callback.message.answer(
        text=LEXICON["ru"]["chosen"],
        reply_markup=language_keyboard
    )
    await state.update_data(last_msg_id=bot_msg.message_id)


@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    # data = await state.get_data()
    # last_msg_id = data["last_msg_id"]
    # if last_msg_id:
    #     try:
    #         await callback.bot.delete_message(
    #             chat_id=callback.message.chat.id,
    #             message_id=int(last_msg_id)
    #         )
    #         await state.clear()
    #     except Exception:
    #         pass 

    lang_code = LANG_MAP[callback.data]

    # если язык ещё не выбран — ставим русский
    if user_id not in user_languages:
        user_languages[user_id] = "ru"

    # если пользователь выбрал тот же язык
    if user_languages[user_id] == lang_code:
        await callback.answer("⚠️ Этот язык уже выбран")
        return

    # сохраняем новый язык
    user_languages[user_id] = lang_code

    # bot_msg = await callback.message.edit_text(
    #     text=LEXICON[lang_code]["chosen"],
    #     reply_markup=language_keyboard
    # )
    start_text = LEXICON.get(lang_code, LEXICON["ru"]).get("start")

    photo_path = "images/photo_2025-09-23_12-26-59.jpg"
    img = FSInputFile(photo_path)
    bot_msg = await callback.message.answer_photo(
        photo=img,
        caption=start_text,
        reply_markup=country_keyboard
    )
    await callback.answer()




@router.callback_query(F.data.startswith("country_"))
async def send_country_message(callback: CallbackQuery, state: FSMContext):
    # Получаем выбранную страну (например: ru, kg, uz)
    country_code = callback.data.split("_", 1)[1]

    data = await state.get_data()
    last_msg_id = data["last_msg_id"]
    if last_msg_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=int(last_msg_id)
            )
            await state.clear()
        except Exception:
            pass

    # Получаем язык пользователя из FSMContext
    user_lang = user_languages.get(callback.from_user.id, "ru")

    # Текст на языке пользователя
    message_text = COUNTRY_MESSAGES.get(user_lang, "🌍 Привет! Страна выбрана.")

    # Путь к фото страны
    image_path = os.path.join(f"images/{country_code}.jpg")

    if os.path.exists(image_path):
        photo = FSInputFile(image_path)
        bot_msg = await callback.message.answer_photo(photo=photo, caption=message_text, reply_markup=country_actions_keyboard(country_code=country_code))
        await callback.answer()
    else:
        bot_msg = await callback.message.answer(message_text)
        await callback.answer()

    # Убираем "часики" на кнопке
    await callback.answer()

    await state.update_data(last_msg_id=bot_msg.message_id)

@router.callback_query(F.data == "back_to_countries")
async def back_to_countries(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.from_user.id

    data = await state.get_data()
    last_msg_id = data["last_msg_id"]
    if last_msg_id:
        try:
            await callback.bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=int(last_msg_id)
            )
            await state.clear()
        except Exception:
            pass

    # язык по умолчанию — русский
    lang_code = user_languages.get(user_id, "ru")

    # берём приветственное сообщение из LEXICON
    start_text = LEXICON.get(lang_code, LEXICON["ru"]).get("start")

    photo_path = "images/photo_2025-09-23_12-26-59.jpg"
    img = FSInputFile(photo_path)
    bot_msg = await callback.message.answer_photo(
        photo=img,
        caption=start_text,
        reply_markup=country_keyboard
    )
    await callback.answer()

    await state.update_data(last_msg_id=bot_msg.message_id)
    