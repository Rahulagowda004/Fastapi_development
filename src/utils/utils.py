import json

def get_data():
    with open('C:\\vscode\\Fastapi_development\\src\\artifacts\\patients.json', 'r') as file:
        data = json.load(file)
    return data