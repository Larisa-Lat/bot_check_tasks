import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


async def google_sheets_authorization():
    # авторизация и получение данных
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client


async def get_sheet(client, sheet_id):
    sheet = client.open_by_key(sheet_id)  # получение доступ к конкретной таблицы
    worksheet = sheet.sheet1  # подключение к 1ой страницы выбранной таблицы
    return worksheet


async def update_sheet_data(sheet_id, leaderboard):
    client = await google_sheets_authorization()
    worksheet = await get_sheet(client, sheet_id)
    # обновление google sheet
    worksheet.update([leaderboard.columns.values.tolist()] + leaderboard.values.tolist())