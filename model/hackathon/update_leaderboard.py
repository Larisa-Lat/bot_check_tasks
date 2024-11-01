from datetime import datetime
import pandas as pd
import logging
from typing import NamedTuple

from model.cases_info.get_sheet_data import update_sheet_data

logger = logging.getLogger("main_logger.update_leaderboard")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


LB_COLUMNS = ['position', 'datetime', 'username', 'score']


class Result(NamedTuple):
    leaderboard_len: int
    leaderboard_table_link: str
    case_name: str
    username: str
    position: int


async def add_in_leaderboard(values, case, username: str, score: int):
    # Перевод данных в Dataframe
    leaderboard = pd.DataFrame(columns=LB_COLUMNS) 
    for row in values[1:]:
        leaderboard.loc[len(leaderboard),:] = row          

    # Преобразование типов
    leaderboard['position'] = leaderboard['position'].astype(int)
    leaderboard['score'] = leaderboard['score'].str.replace(",", ".").astype(float)

    # Добавление новых данных в конец
    current_datetime = '{:%Y-%m-%d %H:%M}'.format(datetime.now())  # получение текущей даты

    leaderboard.loc[len(leaderboard.index)] = [0, current_datetime, username, score]

    # Сортировка 
    leaderboard = leaderboard.sort_values(by='score', ascending=bool(case["metric_ascending"]))
    leaderboard["position"] = [i for i in range(1, len(leaderboard) + 1)]

    await update_sheet_data(case["leaderboard_table_id"], leaderboard)

    position = leaderboard[(leaderboard["datetime"] == current_datetime)
                           & (leaderboard["username"] == username)]["position"].values[0]

    res = Result(leaderboard_len=len(leaderboard),
                 leaderboard_table_link=case["leaderboard_table_link"],
                 case_name=case["case_name"],
                 username=username,
                 position=position)

    return res

