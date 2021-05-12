import csv
import os

from ballot import get_ballot

FILE_NAME = 'results.csv'
CWD_PATH = os.path.abspath(os.getcwd())
FILE_PATH = os.path.join(CWD_PATH, FILE_NAME)


def read_results():
    votes = []
    with open(FILE_PATH, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            votes.extend(row)
        return votes


def calculate_results(results):
    calculated_results = {}
    for number in results:
        if number not in calculated_results:
            calculated_results[number] = 0
        calculated_results[number] += 1
    return calculated_results


def sort_results(results):
    return sorted(results.items(), key=lambda x: (x[1], x[0]), reverse=True)


def add_name(results):
    bind_results = {}
    ballot = dict(get_ballot())
    for number, votes in results:
        bind_results[number] = ballot[number], votes
    return bind_results


def get_results():
    votes = read_results()
    calculated_results = calculate_results(votes)
    sorted_results = sort_results(calculated_results)
    results = add_name(sorted_results)
    return results


def print_results(results):
    counter = 0
    print("Секционни резултати:\n")
    for number, token in results.items():
        name, votes = token
        counter += 1
        word = "гласа" if votes > 1 else "глас"
        print(f"{counter}. ({number}) {name} => {votes} {word}.")


print(get_results())
print_results(get_results())