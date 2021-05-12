import csv
import os

FILE_NAME = 'ballot.csv'
CWD_PATH = os.path.abspath(os.getcwd())
FILE_PATH = os.path.join(CWD_PATH, FILE_NAME)


def get_ballot():
    ballot = []

    with open(FILE_PATH) as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            ballot.append((row[0], row[1]))

    return ballot
