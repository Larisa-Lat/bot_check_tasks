from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.utils.states import AddNewCase, AddNewHackathon
from model.cases_info.subloader_cases_info import get_all_info, new_case

from bot.handlers.admin_commands.get_admins_cases_info import get_cases_info

from os import getenv
from dotenv import load_dotenv

load_dotenv()
LEADERBOARDS_LINK = getenv("LEADERBOARDS_LINK")

router = Router()


@router.message(Command("add_case"))
async def add_new_case(message: Message, state: FSMContext) -> None:
    text = "Создать таблицу в \n" + f"{LEADERBOARDS_LINK} \n" +\
           "Дать имя - Кейс_(номер кейса). (Название кейса)\n" \
           "Настройка таблицы:\n" \
           "1 - Дать расширение боту pp-case-bot@pp-case-bot.iam.gserviceaccount.com \n" \
           "2 - Если будет Хакатон, то шапка: \n" \
           "    position	datetime	username	score\n" \
           "  - Если будет Kaggle like, то шапка: \n" \
           "    position	datetime	username	score	notebook"
    await message.answer(text=text)
    await message.answer(text="Введи id кейса\nДля отмены пришли 0")
    await state.set_state(AddNewCase.ADD_CASE_ID)


async def end_form(message: Message, state: FSMContext) -> None:
    await message.answer(text="Отменено")
    await state.clear()


@router.message(AddNewCase.ADD_CASE_ID)
async def add_new_case(message: Message, state: FSMContext) -> None:
    cases_id = set(case['case_id'] for case in get_all_info())
    if message.text != "0" and message.text.isdigit() and int(message.text) not in cases_id:
        await state.update_data(case_id=int(message.text))
        await message.answer(text="Введи название кейса\nДля отмены пришли 0")
        await state.set_state(AddNewCase.ADD_CASE_NAME)
    else:
        await end_form(message, state)


@router.message(AddNewCase.ADD_CASE_NAME)
async def get_case_name(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        await state.update_data(case_name=message.text)
        await message.answer(text="Введи id таблицы с лидербордом\nДля отмены пришли 0")
        await state.set_state(AddNewCase.ADD_SHEET_ID_LEADERBOARD)
    else:
        await end_form(message, state)


@router.message(AddNewCase.ADD_SHEET_ID_LEADERBOARD)
async def add_sheet_id_leaderboard(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        await state.update_data(leaderboard_table_id=message.text)
        await message.answer(text="Введи сcылку на лидерборд\nДля отмены пришли 0")
        await state.set_state(AddNewCase.ADD_LEADERBOARD_TABLE_LINK)
    else:
        await end_form(message, state)


@router.message(AddNewCase.ADD_LEADERBOARD_TABLE_LINK)
async def add_sheet_id_leaderboard(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        await state.update_data(leaderboard_table_link=message.text)
        await message.answer("Пришли ссылку где лежит задача\n"
                             "Если Kaggle like то ссылка на kaggel, если Хакатон то на диске\n"
                             "Для отмены пришли 0")
        await state.set_state(AddNewCase.ADD_TASK)

    else:
        await end_form(message, state)


@router.message(AddNewCase.ADD_TASK)
async def add_task(message: Message, state: FSMContext):
    if message.text != "0":
        await state.update_data(task=message.text)
        await message.answer(text="Введи категорию\n"
                                  "0 - хакатон\n"
                                  "1 - kaggle like\n"
                                  "Для отмены пришли -1")
        await state.set_state(AddNewCase.ADD_CATEGORY)
    else:
        await end_form(message, state)


@router.message(AddNewCase.ADD_CATEGORY)
async def add_category(message: Message, state: FSMContext) -> None:
    if message.text != "-1":
        if message.text == "0":
            await state.update_data(category=1)
            await message.answer(text="Введи id таблицы с true_labels\nДля отмены пришли 0")
            await state.set_state(AddNewHackathon.ADD_SHEET_ID_TRUE_LABELS)
        elif message.text == "1":
            new_data = await state.get_data()
            new_data["category"] = 1
            new_case(new_data)
            await message.answer(text="Готово")
            await get_cases_info(message)
            await state.clear()
    else:
        await end_form(message, state)


@router.message(AddNewHackathon.ADD_SHEET_ID_TRUE_LABELS)
async def add_sheet_id_true_labels(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        await state.update_data(true_labels_table_id=message.text)
        await message.answer(text="Введи метрику\nДля отмены пришли 0")
        await state.set_state(AddNewHackathon.ADD_METRIC)
    else:
        await end_form(message, state)


@router.message(AddNewHackathon.ADD_METRIC)
async def add_metric(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        await state.update_data(metric_func=message.text)
        await message.answer(text="Введи: \n"
                                  "0 - в лидерборде сортировка скора по убыванию\n"
                                  "1 - в лидерборде сортировка скора по возрастанию")
        await state.set_state(AddNewHackathon.ADD_METRIC_ASCENDING)
    else:
        await end_form(message, state)


@router.message(AddNewHackathon.ADD_METRIC_ASCENDING)
async def add_metric(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(metric_ascending=int(message.text))
        new_data = await state.get_data()
        new_case(new_data)
        await get_cases_info(message)
        await message.answer(text="Готово")
    else:
        await message.answer(text="Отменено \nЛибо 0, либо 1")
    await state.clear()
