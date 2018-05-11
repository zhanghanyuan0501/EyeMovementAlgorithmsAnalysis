import csv, os

results = []
for file in os.listdir('./data'):
    if file.endswith('.cal'):
        with open('./data/' + file, newline='') as inputfile:
            for line in inputfile:
                results.append(line)

print(results)