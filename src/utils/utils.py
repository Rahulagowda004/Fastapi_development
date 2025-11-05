import json

def get_data():
    with open('src\\artifacts\\patients.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('src\\artifacts\\patients.json', 'w') as f:
        json.dump(data, f)