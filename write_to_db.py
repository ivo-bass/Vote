import csv
import os


VOTE_FILE_NAME = 'results.csv'
PREFERENCES_FILE_NAME = 'preferences_results.csv'

CWD_PATH = os.path.abspath(os.getcwd())

VOTE_FILE_PATH = os.path.join(CWD_PATH, VOTE_FILE_NAME)
PREFERENCES_FILE_PATH = os.path.join(CWD_PATH, PREFERENCES_FILE_NAME)


def write_vote_to_db(vote):
    print(f"{vote} is writing to db")
    with open(VOTE_FILE_PATH, "a+") as file:
        writer = csv.writer(file)
        writer.writerow([vote])


def write_preference_to_db(vote, pref):
    if pref:
        print(f"{pref} is writing to db")
        with open(PREFERENCES_FILE_PATH, "a+") as file:
            writer = csv.writer(file)
            writer.writerow([vote, pref])
