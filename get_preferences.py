import csv
import os

FILE_NAME = 'preferences.csv'
CWD_PATH = os.path.abspath(os.getcwd())
FILE_PATH = os.path.join(CWD_PATH, FILE_NAME)


def get_preferences():
    preferences = {}

    with open(FILE_PATH) as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            string = f"({row[0]}) {row[1]}"
            current = row[2].split(", ")
            pref_dd = {key: val for key, val in [el.split(":") for el in current]}
            preferences[string] = pref_dd

    return preferences


# print(get_preferences())
