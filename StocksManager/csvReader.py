import csv

def retrieve_csv_row(csv_string: str, row: str):
    list = []
    with open(csv_string, mode ='r') as file:
        csvFile = csv.DictReader(file)
        for i in csvFile:
            if i[row]:
                list.append(i[row])
    return list