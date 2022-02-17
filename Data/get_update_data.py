import json


def get_data():
    with open("Data/data.json", "r") as file:
        return json.load(file)

def update_data(data):
    with open("Data/data.json", "w") as file:
        json.dump(data, file, indent=4)