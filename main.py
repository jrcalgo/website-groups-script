import collections
from urllib.parse import urlparse
import json
import os

## GROUP_PATH to url groups file
GROUP_PATH = './group_data/url_groups.json'

## URL key numbers are irrelevant; only for key differentiation; URLs are opened sequentially based on dict position
## ensure your urls contain scheme (http/https) and netloc(domain)
def new_url_group(group={'name': {'url1': 'http://www.google.com','url2': 'https://www.amazon.com'}}) -> None:
    url_tuples = [()]
    for url_dict in group.values():
        if isinstance(url_dict, dict):
            url_tuples.extend([(key, value) for key, value in url_dict.items()])
            key, value = url_tuples[-1]
            if not isinstance(value, str):
                print("contains non-string value"); return
            elif not all([urlparse(value).scheme, urlparse(value).netloc]):
                print("contains invalid URL"); return
        else:
            print("contains non-dict value"); return

    if url_tuples == [()]:
        print("no URL pairs specified"); return
    
    mode = 'r+' if os.path.isfile(GROUP_PATH) else 'w'
    with open(GROUP_PATH, mode) as output: 
        if mode == 'w':
            groups = {'groups':group}
            json.dump(groups, output, indent=4)
        else:
            output.seek(0)
            groups = json.load(output)
            if set(group.keys()).isdisjoint(groups['groups']):
                groups['groups'].update(group)
                output.seek(0)
                json.dump(groups, output, indent=4)
            else:
                print("group name already exists"); return

def get_url_group_names() -> list:
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
    except IOError:
        print("IOError: Unable to open url_groups.json. Terminating execution."); return

    return list(groups['groups'].keys())

def get_url_group(group_name:str="") -> dict:
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
    except IOError:
        print("IOError: Unable to open url_groups.json. Terminating execution."); return
        
    return groups['groups'][group_name]
        
def edit_url_group(group_name:str='', new_group_name:str='', new_urls:dict={'url1':'http://www.google.com','url2':'https://www.amazon.com'}):
    group = get_url_group(group_name)
    with open(GROUP_PATH, 'r+') as output:
        groups = json.load(output)
        if new_group_name != '':
            group = groups['groups'].pop(group_name)
            groups['groups'][new_group_name] = group
        else:
            while True:
                new_group_name = input("Enter new group name: ")
                if new_group_name in get_url_group_names(): print("group name already exists")
                else: break
            group = groups['groups'].pop(group_name)
            groups['groups'][new_group_name] = group
        if group_name in get_url_group_names():
            output.seek(0)
            groups['groups'].update(group)
            output.seek(0)
            json.dump(groups, output, indent=4)
        else:
            print("group name does not exist"); return

def remove_url_group(group_name:str=''):
    group = get_url_group(group_name)
    with open(GROUP_PATH, 'r+') as output:
        groups = json.load(output)
        if group_name in get_url_group_names():
            del groups['groups'][group_name]
            output.seek(0)
            output.truncate()
            json.dump(groups, output, indent=4)
        else:
            print("group name does not exist"); return

def sort_file_by_name(path:str=''):
    with open(GROUP_PATH, 'r+') as file:
        groups = json.load(file)
        sorted_groups = collections.OrderedDict(sorted(groups['groups'].items()))
        groups['groups'] = sorted_groups
        file.seek(0)
        file.truncate()
        json.dump(groups, file, indent=4)
        
def open_url_group(group_name:str=''):
    group = get_url_group(group_name)
    pass


COMMANDS = ['open', 'list', 'new', 'edit', 'remove']
while True:
    print ("Available commands: ")
    commands = ', '.join(COMMANDS)
    print (commands)
    while True:
        command = input("Enter command: ")
        if command in COMMANDS: break
        else: print("invalid command")
    if command == COMMANDS[0]:
        group_name = input("Enter group name: ")
        open_url_group(group_name)
    elif command == COMMANDS[1]:
        print("=========================")
        for group in get_url_group_names():
            print(group)
        print("=========================")
    elif command == COMMANDS[2]:
        group={}
        urls = []
        while True:
            while True:
                group_name = input("Enter group name: ")
                if group_name == '': print("invalid group name")
                elif group_name in get_url_group_names(): print("group name already exists")
                else: break
            while True:
                url = input("Enter URL name: ")
                if url == '': print("invalid url name")
                else: 
                    while True:
                        url = (url, input("Enter URL: "))
                        if not all([urlparse(url[1]).scheme, urlparse(url[1]).netloc]): print("invalid url")
                        else: urls.append(url); break
                if input("Add another URL? (y/n): ").lower() == 'n': break
            for url in urls:
                url_name, link = url
                group[group_name] = {url_name: link}
            new_url_group(group)
            if input("Add another group? (y/n): ").lower() == 'n': break
    elif command == COMMANDS[3]:
        while True:
            group_name = input("Enter group name: ")
            if group_name == '': print("invalid group name")
            else: break
        while True:
            new_group_name = input("New group name? (y/n): ")
            if new_group_name.lower() == 'y':
                new_group_name = input("Enter new group name: ")
                if new_group_name == '': print("invalid group name")
                elif new_group_name in get_url_group_names(): print("group name already exists")
                else: break
            else: break
        while True:

        edit_url_group(group_name)
    elif command == COMMANDS[4]:
        group_name = input("Enter group name: ")
        remove_url_group(group_name)
