from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_CASE_ID = State()
    GET_FILE_PATH = State() # for Hackathon
    GET_NOTEBOOK_PATH = State() #for Kaggle_like


class AddNewCase(StatesGroup):
    ADD_CASE_ID = State()
    ADD_CASE_NAME = State()
    ADD_SHEET_ID_LEADERBOARD = State()
    ADD_LEADERBOARD_TABLE_LINK = State()
    ADD_TASK = State()

    ADD_CATEGORY = State()


class AddNewHackathon(StatesGroup):
    ADD_SHEET_ID_TRUE_LABELS = State()
    ADD_METRIC = State()
    ADD_METRIC_ASCENDING = State()


class DeleteCase(StatesGroup):
    DELETE_CASE = State()


class AddAdmin(StatesGroup):
    GET_ADMIN_NAME = State()
    GET_ADMIN_ID = State()


class DeleteAdmin(StatesGroup):
    DELETE_ADMIN = State()


class GetCases(StatesGroup):
    GET_CATEGORY = State()
