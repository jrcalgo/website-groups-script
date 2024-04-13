import collections
from urllib.parse import urlparse
import webbrowser
import json
import os

## GROUP_PATH to url groups file
GROUP_PATH = './group_data/url_groups.json'

def get_url_group_names() -> list:
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
            return list(groups['groups'].keys())
    except:
        return []

def get_url_group(group_name:str="") -> dict:
    if group_name in get_url_group_names(): print("invalid group name"); return
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
            return groups['groups'][group_name]
    except:
        return []

def sort_file_by_name():
    with open(GROUP_PATH, 'r+') as file:
        groups = json.load(file)
        sorted_groups = collections.OrderedDict(sorted(groups['groups'].items()))
        groups['groups'] = sorted_groups
        file.seek(0)
        file.truncate()
        json.dump(groups, file, indent=4)

def open_url_group(group_name:str=''):
    try:
        group = get_url_group(group_name)
        if group:
            first_url = True
            for url in group.values():
                if first_url:
                    webbrowser.open(url, new=1)
                    first_url = False
                else:
                    webbrowser.open_new_tab(url)
        else:
            return
    except:
        print("**error opening group**"); return
    
def fix_file():
    pass

COMMANDS = ['open', 'list', 'sort', 'fix_file']
while True:
    command = ''
    group_name = ''
    valid_input = False

    print ("Available commands: ")
    commands = ', '.join(COMMANDS)
    print (commands)
    while True:
        while True:
            command_input = input("Enter command: ").split()
            command = command_input[0]
            if command not in COMMANDS:
                print("invalid command"); break
            elif (command == 'list' or command == 'sort') and len(command_input) > 1:
                print("command requires no arguments"); break
            elif command == 'list' or command == 'sort':
                valid_input = True
                break
            group_arg = command_input[1:]
            if len(group_arg) > 1:
                print("too many arguments, executing first argument only, if applicable")
                continue
            if group_arg[0] not in COMMANDS and group_arg[0] in get_url_group_names():
                group_name = group_arg[0]
                valid_input = True
                break
            else: print("invalid command")
        if valid_input: break
    if command == COMMANDS[0]:
        open_url_group(group_name)
    elif command == COMMANDS[1]:
        print("=========================")
        for group in get_url_group_names():
            print(group)
        print("=========================")
    elif command == COMMANDS[2]:
        sort_file_by_name()
        print("=========================")
        print("file sorted")
        print("=========================")
    elif command == COMMANDS[3]:
        print("***WARNING: this will deprecate the old file in the directory, if it exists")
        if input("do you want to continue? (y/n): ").casefold() == 'y':
            fix_file()
            print("=========================")
            print("file fixed")
            print("=========================")
            break
        else:
            break
