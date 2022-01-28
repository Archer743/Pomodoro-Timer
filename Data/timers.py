import json


def get_data():
    with open("Data/data.json", "r") as file:
        return json.load(file)

def update_data(data):
    with open("Data/data.json", "w") as file:
        json.dump(data, file, indent=4)

def check_input(input:tuple):
    if (100 >= input[0] >= 0) and (60 > input[1] >= 0) and (60 > input[2] >= 0):  # (hours) (minutes) (seconds)
        return 0
    
    return 1

def add_timers(name:str, pomodoro:tuple = None, short_break:tuple = None, long_break:tuple = None):
    if pomodoro == short_break == long_break == None:
        return 1  # Error: Nothing was added
    elif (check_input(pomodoro) + check_input(short_break) + check_input(long_break)) != 0:
        return 2 # Error: Check your input
    
    data = get_data()

    pomodoro = pomodoro if pomodoro != None else (0, 25, 0)  # 0 - hours, 25 - minutes, 0 seconds
    short_break = short_break if short_break != None else (0, 5, 0)  # 0 - hours, 5 - minutes, 0 seconds
    long_break = long_break if long_break != None else (0, 15, 0)  # 0 - hours, 15 - minutes, 0 seconds

    new_timers = [pomodoro, short_break, long_break]
    data["timers"][name] = new_timers
    data["timers"]["counter"] += 1
    
    update_data(data)
    return 0

def remove_timers(name:str):
    data = get_data()
    
    try:
        del data["timers"][name]
        update_data(data)
        return 0
    except:
        return 1  # Error: Name Not Found