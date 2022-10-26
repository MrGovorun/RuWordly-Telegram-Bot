import csv

all_words = dict()

with open('words.csv') as file:
    csv_reader = csv.reader(file)
    for line in csv_reader:
        all_words[line[0]] = int(line[1])
