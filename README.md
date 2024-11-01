# Telegram bot for managing cases leaderboards in reu ds club.


## Bot commands:
- For users:
  - `/case` - send to calculate the score
  - `/id_cases` - cases ids
  - `/help` - admins ready to help
- For admins:
  - `/cases_info` 
  - `/add_case` 
  - `/delete_case` 
  - `/admins_info` 
  - `/add_admin` 
  - `/delete_admin` 

## Installation:
1. Install Python 3.9 if it is not installed. [Python.org](https://www.python.org/downloads/)

2. Clone the repository:

   ```bash
   git clone https://github.com/REU-DS-CLUB/pet_projects_case_bot

3. Navigate to the project catalog:

   ```bash
   cd pet_projects_case_bot

4. Install the dependencies using pip:

   ```bash
   pip install -r requirements.txt

## Configuration:
1. **.env**

Copy and rename .env.example in .env . Specify the environment variables in .env

BOT_TOKEN = ...

GROUP_CHAT_ID = ...

2. **cases_info.json**

Where: model/data/cases_info.json.example
Copy and rename cases_info.json.example in cases_info.json

Fill cases_info.json for every case:
 - `case_id`: cases id, start with 1 (int)
 - `case_name`: Give case a name (str)
 - `true_labels_table_id`: The URL of your Google spreadsheet to access your true labels data. (str)
 - `metric_func`: classification metric (str)
 - `metric_ascending`: 0 or 1 

(0 - Descending sorted score in leaderboard, 1 - Ascending sorted score in leaderboard) (int)
 - `leaderboard_table_id`: The URL of your Google spreadsheet to access your leaderboard. (str)

3. **admins.json**

Where: bot/data/admins.json.example

Copy and admins.json.example in admins.json:
[[@admin_name1(str), user_id_in_tg(int)], ...]


### How to allow access and download your credetials.json [here]([https://developers.google.com/sheets/api/quickstart/python?hl=ru](https://developers.google.com/sheets/api/quickstart/python?hl=ru)


## Requirements for Google sheets:
- For sheets with true_labels columns must be:
id	true_value


- For sheets with leaderboard columns must be:
position	datetime	username	score

For each table you need add googleservice account from credentials.json


