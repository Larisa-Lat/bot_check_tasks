from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from model.cases_info.subloader_cases_info import get_cases_category
from bot.admins_info.subloader_admins import get_admins_names
from aiogram.fsm.context import FSMContext

from bot.utils.states import GetCases

from os import getenv
from dotenv import load_dotenv

load_dotenv()
LEADERBOARDS_LINK = getenv("LEADERBOARDS_LINK")

router = Router()


@router.message(Command("start"))
async def get_start(message: Message) -> None:

    """Приветственное сообщение"""
    await message.answer(f"Привет, {message.from_user.first_name}!\n\n"
                         f"Я бот - отвечаю за кейсы DS Club!\n\n"
                         f"Команды бота:\n"
                         f"/info_cases - кейсы\n"
                         f"/send_case - отправить кейс\n"
                         f"/instruction - инструкция\n"
                         f"/help - помощь здесь\n\n"
                         f"Все лидерборды здесь - \n"
                         f"{LEADERBOARDS_LINK}")


@router.message(Command("info_cases"))
async def cases_ids(message: Message, state: FSMContext) -> None:
    """Вывод название кейсов и их айдишки"""
    await message.answer("Выбери категорию кейса:\n"
                         "0 - кейсы с хакатонов\n"
                         "1 - кейсы с Kaggle")
    await state.set_state(GetCases.GET_CATEGORY)


@router.message(GetCases.GET_CATEGORY)
async def get_category(message: Message, state: FSMContext):
    if message.text == "0" or message.text == "1":
        data = get_cases_category(int(message.text))
        for d in data:
            answer = ""
            answer += f"Номер кейса : {d['case_id']}\n" \
                      f"Имя кейса: {d['case_name']}\n" \
                      f"Описание кейса с данными: {d['task']}"
            await message.answer(answer)
    else:
        await message.answer("Отменено")
    await state.clear()


@router.message(Command("help"))
async def helping(message: Message) -> None:
    """В случае возниконовения вопросов, проблем у пользователя - это команда выведет имена админов"""
    await message.answer(f"Тебе помогут:")
    answer = ""
    for admin_name in get_admins_names():
        answer += f"{admin_name}\n"
    await message.answer(answer)


@router.message(Command("instruction"))
async def get_instruction(message: Message) -> None:

    answer = f"Есть кейсы двух видов:\n" \
             f"\n"\
             f"<b>С Хакатонов</b>\n" \
             f"\n" \
             f"    1. В /info_cases выбери 0 категорию, получи список заданий с Хакатонов\n" \
             f"\n" \
             f"    Инфа о хакатоне: \n" \
             f"        - номер кейса(понадобится при отправке на проверку кейса в /send_case) \n" \
             f"        - название задачи\n" \
             f"        - ссылку на диск, на которой хранится описание задачи и все необходимые данные\n" \
             f"\n" \
             f"    2. Выполни задание и сохрани результаты в файл csv\n" \
             f"\n" \
             f"    3. Отправь файл по команде /send_case\n" \
             f"\n"\
             f"<b>С Kaggle</b>\n" \
             f"\n" \
             f"    1. В /info_cases выбери 1 категорию и получи список заданий с Kaggle\n" \
             f"\n" \
             f"    Инфа о Kaggle-like: \n" \
             f"        - номер кейса(понадобится при отправке на проверку кейса в /send_case)\n" \
             f"        - название задачи\n" \
             f"        - ссылку на Kaggle с заданием\n" \
             f"\n" \
             f"    2. Поучаствуй в соревновании, опубликуй свой notebook на Kaggle\n" \
             f"\n" \
             f"        Как участвовать в соревновании:\n" \
             f"https://proglib.io/p/kaggle-za-30-minut-prakticheskoe-rukovodstvo-dlya-nachinayushchih-2021-09-17?ysclid=lxlmj9d4sv743512034\n" \
             f"\n" \
             f"    3. Отправь ссылку на свой notebook по команде /send_case\n" \
             f"\n" \
             f"После отправки на проверку бота ты получишь:\n" \
             f"    - сообщение о твоем скоре\n" \
             f"    - какое место ты занял(а) в лидерброде\n" \
             f"    - в группу ( https://t.me/c/2033658407/774 ) будет прислано сообщение о твоем результате\n\n" \
             f"Все лидерборды здесь - {LEADERBOARDS_LINK}\n" \
             f"\n\n" \
             f"Удачи!"
    await message.answer(answer, parse_mode='HTML')
