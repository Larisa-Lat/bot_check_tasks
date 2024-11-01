from model.cases_info.subloader_cases_info import find_case

from model.hackathon.count_score import count_score
from model.hackathon.update_leaderboard import add_in_leaderboard

from model.cases_info.get_sheet_data import google_sheets_authorization, get_sheet

from gspread.exceptions import SpreadsheetNotFound


class UserHackathon:
    user_case_id = 0
    user_file_name = 0
    user_username = ""

    case = 0
    check_tables = False
    errors = ("", "")
    true_labels_table = ""
    leaderboard_table = ""
    score = 0

    def __init__(self, user_info: dict):
        self.user_case_id = user_info["case_id"]
        self.user_file_name = user_info["file_name"]
        self.user_username = user_info["username"]

        self.case = find_case(self.user_case_id)

    async def check_sheets(self):
        try:
            client = await google_sheets_authorization()
            worksheet = await get_sheet(client, self.case["true_labels_table_id"])
            true_labels_table = worksheet.get_all_records()
            worksheet = await get_sheet(client, self.case["leaderboard_table_id"])
            leaderboard_table = worksheet.get_all_values()

        except SpreadsheetNotFound as err:
            self.errors = ("exception2", f"Ошибка {SpreadsheetNotFound}  {err} в кейсе {self.case['case_id']}")

        except Exception as err:
            self.errors = ("exception1", f"С credentials.json беда\n{Exception}  {err}")
        else:
            self.check_tables = True
            self.true_labels_table = true_labels_table
            self.leaderboard_table = leaderboard_table

    async def get_score(self) -> str:
        if self.check_tables:
            score = await count_score(self.true_labels_table, self.case, self.user_file_name)
            self.score = score
            return score

    async def update_leaderboard(self):
        if self.check_tables:
            return await add_in_leaderboard(self.leaderboard_table, self.case, self.user_username, self.score)
