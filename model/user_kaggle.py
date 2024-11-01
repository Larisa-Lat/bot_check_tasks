from time import sleep
from model.cases_info.subloader_cases_info import find_case

from model.kaggle_like.update_leaderboard import add_in_leaderboard

from model.cases_info.get_sheet_data import google_sheets_authorization, get_sheet

from gspread.exceptions import SpreadsheetNotFound

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By


class UserKaggle:
    user_case_id = 0
    notebook = ""
    user_username = ""

    case = 0
    check_tables = False
    errors = ("", "")
    leaderboard_table = ""
    score = ""

    def __init__(self, user_info: dict):
        self.user_case_id = user_info["case_id"]
        self.notebook = user_info["notebook"]
        self.user_username = user_info["username"]

        self.case = find_case(self.user_case_id)

    async def check_sheets(self):
        try:
            client = await google_sheets_authorization()
            worksheet = await get_sheet(client, self.case["leaderboard_table_id"])
            leaderboard_table = worksheet.get_all_values()

        except SpreadsheetNotFound as err:
            self.errors = ("exception2", f"Ошибка {SpreadsheetNotFound}  {err} в кейсе {self.case['case_id']}")

        except Exception as err:
            self.errors = ("exception1", f"С credentials.json беда\n{Exception}  {err}")
        else:
            self.check_tables = True
            self.leaderboard_table = leaderboard_table

    async def get_score(self) -> str:
        if self.check_tables:
            options = webdriver.ChromeOptions()
            options.add_argument(
                "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=options)

            browser.get(self.notebook)
            sleep(0.5)

            try:
                data = browser.find_element(By.XPATH, "//div[text()='Public Score']/following-sibling::p")
            except Exception:
                self.score = "error"
            else:
                self.score = data.text
            return self.score

    async def update_leaderboard(self):
        if self.check_tables:
            return await add_in_leaderboard(self.leaderboard_table, self.case, self.user_username, float(self.score), self.notebook)

