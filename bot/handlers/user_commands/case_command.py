from os import remove

from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from os import getenv
from dotenv import load_dotenv

from bot.utils.states import StepsForm
from model.cases_info.subloader_cases_info import get_all_info

from model.user_hackathon import UserHackathon
from model.user_kaggle import UserKaggle

from bot.utils.alert_admins import alert_admins
from model.cases_info.subloader_cases_info import find_case


router = Router()

load_dotenv()
GROUP_CHAT_ID = getenv("GROUP_CHAT_ID1")
MESSAGE_THREAD_ID = getenv("MESSAGE_THREAD_ID")


@router.message(Command("send_case"))
async def get_form(message: Message, state: FSMContext) -> None:
    await message.answer("Напиши id кейса\nДля отмены пришли 0")
    await state.set_state(StepsForm.GET_CASE_ID)


@router.message(StepsForm.GET_CASE_ID)
async def get_case_id(message: Message, state: FSMContext) -> None:
    if str(message.text).isdigit() \
            and int(message.text) in set(d['case_id'] for d in get_all_info()):

        await state.update_data(case_id=int(message.text))

        if message.from_user.username is not None:
            await state.update_data(username=message.from_user.username)
        else:
            user_id = str(message.from_user.id)
            await message.answer(f"Ваш ник не задан в tg, поэтому будет использоваться user id \n"
                                 f"Ваш user id в tg: {user_id}")
            await state.update_data(username=user_id)

        if find_case(int(message.text))['category'] == 0:
            await hackathon(message, state)
        elif find_case(int(message.text))['category'] == 1:
            await kaggle_like(message, state)
    elif message.text == "0":
        await message.answer(f"Отменено")
        await state.clear()
    else:
        await message.answer(f"Не угадал кейс - глянь в /info_cases")
        await state.clear()


async def check_score(message: Message, bot: Bot, score: str, user_case: UserHackathon or UserKaggle) -> None:
    if score == "error":
        await message.answer(text="С ссылкой что то не то(\n"
                                  "Перепроверь и начни сначала /send_case")
    else:
        await message.answer(f"Твой скор: {score}\n"
                             f"Обновляем лидерборд ...")
        result = await user_case.update_leaderboard()
        person_message = f"Ваше место в лидерборде {result.position} " \
                         f"из {result.leaderboard_len} \n" \
                         f"Ссылка на лидерборд: {result.leaderboard_table_link}"
        chat_message = f"Обновление лидерборда!\n" \
                       f"В кейсе {result.case_name}, " \
                       f"{result.username} занимает {result.position} место " \
                       f"из {result.leaderboard_len} \n" \
                       f"Ссылка на лидерборд: {result.leaderboard_table_link}"
        await message.answer(text=person_message)
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=chat_message, message_thread_id=MESSAGE_THREAD_ID)


async def kaggle_like(message: Message, state: FSMContext):
    await message.answer(f"Выбран кейс {message.text}\n"
                         f"Ждем-с ссылку на notebook на Kaggle ...\n"
                         f"Для отмены пришли 0")
    await state.set_state(StepsForm.GET_NOTEBOOK_PATH)


@router.message(StepsForm.GET_NOTEBOOK_PATH)
async def get_notebook(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.text and message.text != "0" and message.text.startswith("https://www.kaggle.com/code/"):
        data = await state.get_data()
        data["notebook"] = message.text
        user_kaggle = UserKaggle(data)
        await user_kaggle.check_sheets()
        if user_kaggle.check_tables:
            score = await user_kaggle.get_score()
            await check_score(message, bot, score, user_kaggle)
    else:
        await message.answer(f"Отменено")
    await state.clear()


async def hackathon(message: Message, state: FSMContext):
    await message.answer(f"Выбран кейс {message.text}\n"
                         f"Ждем-с файлик csv ...\n"
                         f"Для отмены пришли 0")

    await state.set_state(StepsForm.GET_FILE_PATH)


async def download_file(message: Message, bot: Bot, username: str) -> str:
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = str(username) + ".csv"
    await bot.download_file(file_path, file_name)
    return file_name


@router.message(StepsForm.GET_FILE_PATH)
async def get_file_path(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.document:
        data = await state.get_data()
        file_name = await download_file(message, bot, data["username"])
        data["file_name"] = file_name

        user_case = UserHackathon(data)
        await user_case.check_sheets()
        if user_case.check_tables:
            score = await user_case.get_score()
            await check_score(message, bot, score, user_case)
        else:
            if user_case.errors[0] == "exception1":
                await message.answer(text="Пока отправка кейсов приостановлена!"
                                          "\nАдмины разбираются.\nПопробуйте позже.")
                await alert_admins(bot, user_case.errors[1])
            elif user_case.errors[0] == "exception2":
                await message.answer(text="Ой ой у нас проблемы с данным кейсом. \nАдмины разбираются.")
                await alert_admins(bot, user_case.errors[1])

        remove(file_name)
    elif message.text == "0":
        await message.answer(f"Отменено")
    else:
        await message.answer(f"Это не файл(. Попробуй сначала /send_case")
    await state.clear()
