import datetime
import json
import csv
import os

from utils.core import logger


def get_all_lines(filepath: str):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    if not lines:
        return []

    return [line.strip() for line in lines]


def load_from_json(path: str):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def save_to_json(path: str, dict_):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data.append(dict_)
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def save_list_to_file(filepath: str, list_: list):
    with open(filepath, mode="w", encoding="utf-8") as file:
        for item in list_:
            file.write(f"{item['session_name']}.session\n")


def save_csv(data_list: list):
    filename = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='w', newline='') as file:
        if data_list:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()

            for data in data_list:
                writer.writerow(data)

    logger.success(f'Data has been saved to {filename}')