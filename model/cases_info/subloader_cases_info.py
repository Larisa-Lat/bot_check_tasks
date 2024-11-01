import json
from typing import TypedDict


class Case(TypedDict):
    case_id: int
    case_name: str
    category: int
    task: str
    true_labels_table_id: str
    metric_func: str
    metric_ascending: int
    leaderboard_table_id: str
    leaderboard_table_link: str


def get_all_info() -> list[Case]:
    with open("model/cases_info/cases_info.json", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return [Case(**d) for d in data]


def find_case(case_id: int) -> Case:
    data = get_all_info()
    for d in data:
        if d["case_id"] == case_id:
            return d


def get_cases_category(category: int) -> list[Case]:
    res = []
    data = get_all_info()
    for d in data:
        if d['category'] == category:
            res.append(d)
    return res


def new_case(new_data: dict) -> None:
    data = get_all_info()
    with open("model/cases_info/cases_info.json", mode='w', encoding='utf-8') as json_file:
        data.append(new_data)
        data.sort(key=lambda x: x["case_id"])
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def delete_case(case_id: int) -> None:
    cases = get_all_info()
    for i in range(len(cases)):
        if cases[i]["case_id"] == case_id:
            del cases[i]
            with open("model/cases_info/cases_info.json", mode='w', encoding='utf-8') as json_file:
                json.dump(cases, json_file, indent=4, ensure_ascii=False)
            return
