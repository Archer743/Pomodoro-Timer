from sys import path
path.insert(1, "./Data")
from Data.get_update_data import *


def edit_settings(*args, **kwargs):
    audio = kwargs.get("audio")
    theme = kwargs.get("theme")

    data = get_data()
    changed = False

    if isinstance(audio, bool) and data["settings"]["audio"] != audio:
        data["settings"]["audio"] = audio
        changed = True

    if isinstance(theme, str) and data["settings"]["theme"] != theme:
        data["settings"]["theme"] = theme.lower()
        changed = True

    if changed:
        update_data(data)

def update_presence(pr:bool):
    if (data := get_data()):
        data["presence"] = pr
        update_data(data)