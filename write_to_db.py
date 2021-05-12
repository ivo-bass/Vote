import csv
import os

FILE_NAME = 'results.csv'
CWD_PATH = os.path.abspath(os.getcwd())
FILE_PATH = os.path.join(CWD_PATH, FILE_NAME)


def write_to_db(vote):
    print(f"{vote} is writing to db")
    with open(FILE_PATH, "a") as file:
        writer = csv.writer(file)
        writer.writerow([vote])