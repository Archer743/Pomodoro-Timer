import json


def get_data():
    with open("Data/data.json", "r") as file:
        return json.load(file)

def update_data(data):
    with open("Data/data.json", "w") as file:
        json.dump(data, file, indent=4)

def edit_settings(*args, **kwargs):
    sound = kwargs.get("sound")
    theme = kwargs.get("theme")

    data = get_data()
    changed = False

    if isinstance(sound, bool) and data["settings"]["sound"] != sound:
        data["settings"]["sound"] = sound
        changed = True

    if isinstance(theme, str) and data["settings"]["theme"] != theme:
        data["settings"]["theme"] = theme.lower()
        changed = True

    if changed:
        update_data(data)