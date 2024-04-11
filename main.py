import tkinter as tk
from urllib.parse import urlparse
import json
import os

## GROUP_PATH to url groups file
GROUP_PATH = './group_data/url_groups.json'

## URL key numbers are irrelevant; only for key differentiation; URLs are opened sequentially based on dict position
## ensure your urls contain scheme (http/https) and netloc(domain)
def new_url_group(group={'name': {'url1':'http://www.google.com','url2':'https://www.amazon.com'}}) -> None:
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
    
    mode = 'a' if os.path.isfile(GROUP_PATH) else 'w'
    with open(GROUP_PATH, mode) as output: 
        if mode == 'w':
            groups = {'groups':group}
            json.dump(groups, output, indent=4)
        else:
            groups['groups'].add(group)
            json.dump(groups, output, indent=4)

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
        
def edit_url_group(group_name:str=''):
    group = get_url_group(group_name)
    
    with open(GROUP_PATH, 'a') as output:
        pass
    

def remove_url_group(group_name:str=''):
    group = get_url_group(group_name)
    
def sort_file_by_name(path:str=''):
    pass

def open_url_group(group_name:str=''):
    group = get_url_group(group_name)
    pass

COMMANDS = ['open group', 'list groups', 'new group', 'edit group', 'remove group']
while True:
    print ("Available commands: ")
    commands = ', '.join(COMMANDS)
    print (commands)
    while True:
        command = input("Enter command: ")
        if command in COMMANDS: break
        else: print("invalid command")
    if command == 'open group':
        group_name = input("Enter group name: ")
        open_url_group(group_name)
    if command == 'list groups':
        for group in get_url_group_names():
            print(group)
    if command == 'new group':
        group={}
        urls = [()]
        while True:
            while True:
                group_name = input("Enter group name: ")
                if group_name == '': print("invalid group name")
                else: break
            while True:
                url = input("Enter URL name: ")
                if url == '': print("invalid url name")
                else: 
                    while True:
                        url = (url, input("Enter URL: "))
                        if url[1] == '': print("invalid url")
                        else:
                            urls.append(url)
                            break
                if input("Add another URL? (y/n) ").lower() == 'n': break
                
            for url in urls:
                url_name, link = url
                group[group_name] = {url_name: link}
            new_url_group(group)
            if input("Add another group? (y/n) ").lower() == 'n': break
    if command == 'edit group':
        group_name = input("Enter group name: ")
        edit_url_group(group_name)
    if command == 'remove group':
        group_name = input("Enter group name: ")
        remove_url_group(group_name)
