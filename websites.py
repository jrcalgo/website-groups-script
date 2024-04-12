import collections
from urllib.parse import urlparse
import webbrowser
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
    if group_name in get_url_group_names(): print("invalid group name"); return
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
    except IOError:
        print("IOError: Unable to open url_groups.json. Terminating execution."); return
        
    return groups['groups'][group_name]
       
## when editing urls, new_urls will replace all existing urls in said group if append is False
## warning: append being True will still overwrite existing urls if key is the same as existing url
def edit_url_group(group_name:str='', new_group_name:str='', new_urls:dict={}, append_urls:bool=False):
    group = get_url_group(group_name)
    with open(GROUP_PATH, 'r+') as output:
        if group_name in get_url_group_names():
            groups = json.load(output)
            if new_group_name != '':
                groups['groups'].pop(group_name)
                groups['groups'][new_group_name] = group
                group = groups['groups'][new_group_name]
            if new_urls != {}:
                for new_url in new_urls.items():
                    if append_urls:
                        group[new_url[0]] = new_url[1]
                    else:
                        group.update({new_url[0]: new_url[1]})
            output.seek(0)
            groups['groups'].update(group)
            output.seek(0)
            json.dump(groups, output, indent=4)
        else:
            print("**group name does not exist**"); return

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
            print("**group name does not exist**"); return

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
                if input("Add another URL? (y/n): ").casefold() == 'n': break
            for url in urls:
                url_name, link = url
                group[group_name] = {url_name: link}
            new_url_group(group)
            if input("Add another group? (y/n): ").casefold() == 'n': break
        sort_file_by_name()
    elif command == COMMANDS[3]:
        group_name = ''
        new_group_name = ''
        new_urls = {}
        append_urls = False
        while True:
            group_name = input("Enter group name: ")
            if group_name == '': print("invalid group name")
            elif group_name in get_url_group_names(): print("group name already exists")
            else: break
        while True:
            new_group_name = input("New group name? (y/n): ")
            if new_group_name.casefold() == 'y':
                while True:
                    new_group_name = input("Enter new group name: ")
                    if new_group_name == '': print("invalid group name")
                    elif new_group_name in get_url_group_names(): print("group name already exists")
                    else: break
            else: break
        while True:
            new_urls = input("Enter new URLs? (y/n): ")
            if new_urls.casefold() == 'y':
                new_url = input("Enter URL name: ")
                if new_url == '': print("invalid url name")
                else:
                    while True:
                        while True:
                            new_url = (new_url, input("Enter URL: "))
                            if not all([urlparse(new_url[1]).scheme, urlparse(new_url[1]).netloc]): print("invalid url")
                            else: new_urls[new_url[0]] = new_url[1]
                        if input("Add another URL? (y/n): ").casefold() == 'n': break
                    while True:
                        append_urls = input("Append to existing group? (y/n): ")
                        if append_urls.casefold() == 'y': append_urls = True; break
                        elif append_urls.casefold() == 'n': append_urls = False; break
                        else: print("invalid response")
        edit_url_group(group_name, new_group_name, new_urls, append_urls)
    elif command == COMMANDS[4]:
        group_name = input("Enter group name: ")
        remove_url_group(group_name)
