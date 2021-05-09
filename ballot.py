import csv


def get_ballot(path):
    ballot = []

    with open(path, newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='|')
        for row in reader:
            ballot.append((row[0], row[1]))

    return ballot

