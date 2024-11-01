from json import load, dump
from typing import NamedTuple


class Admin(NamedTuple):
    admin_name: str
    admin_id: int


def get_admins() -> list[Admin]:
    with open('bot/admins_info/admins.json', encoding='utf-8') as json_file:
        admins = load(json_file)
    return [Admin(admin_name=admin[0], admin_id=admin[1]) for admin in admins]


def get_admins_id() -> set[int]:
    admins = get_admins()
    return set(admin.admin_id for admin in admins)


def get_admins_names() -> list:
    admins = get_admins()
    return [admin.admin_name for admin in admins]


def delete_admin(admin_name: str) -> None:
    admins = get_admins()
    for i in range(len(admins)):
        if admins[i].admin_name == admin_name:
            del admins[i]
            with open("bot/admins_info/admins.json", mode='w', encoding='utf-8') as json_file:
                dump(admins, json_file, indent=4, ensure_ascii=False)
            return


def add_admin(new_admin: dict) -> None:
    new_admin = Admin(**new_admin)
    data = get_admins()
    with open("bot/admins_info/admins.json", mode='w', encoding='utf-8') as json_file:
        data.append(new_admin)
        dump(data, json_file, indent=4, ensure_ascii=False)
