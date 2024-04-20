import collections
from urllib.parse import urlparse
import webbrowser
import datetime
import json
import csv
import os

SORT_ARGS = ['-az', '-za', '-mr', '-lr']
FILE_ARGS = ['-j', '-c', '-jc']
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

## GROUP_PATH to url groups file
GROUP_PATH = './group_data/url_groups.json'
RECENT_USE_PATH = './group_data/recent_url_groups.csv'

def get_url_group_names() -> list:
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
            return list(groups['groups'].keys())
    except:
        return []

def get_url_group(group_name:str="") -> dict:
    if group_name not in get_url_group_names(): print("group does not exist"); return
    try:
        with open(GROUP_PATH, 'r') as file:
            groups = json.load(file)
            return groups['groups'][group_name]
    except:
        return []

def sort_file(sort_arg:str="-az"):
    if sort_arg not in SORT_ARGS: print("invalid sort argument"); return
    elif sort_arg == "" or sort_arg == '-az' or sort_arg == '-za':
        with open(GROUP_PATH, 'r+') as file:
            groups = json.load(file)
            sorted_groups = collections.OrderedDict(sorted(groups['groups'].items()), 
                                                    reverse=False if (sort_arg == '-az' or sort_arg == '') else True)
            groups['groups'] = sorted_groups
            file.seek(0)
            file.truncate()
            json.dump(groups, file, indent=4)
    elif sort_arg == '-mr' or sort_arg == '-lr':
        if sort_arg == '-mr' and recent_groups[0][1] > recent_groups[1][1]:
            print("groups already sorted")
            return
        elif sort_arg == '-lr' and recent_groups[0][1] < recent_groups[1][1]:
            print("groups already sorted")
            return
        if len(get_url_group_names()) > 1 and os.path.exists(RECENT_USE_PATH):
            recent_groups = []
            with open(RECENT_USE_PATH, 'r') as file:
                data = csv.reader(file)
                for row in data:
                    timestamp = datetime.strptime(row[1], TIMESTAMP_FORMAT)
                    recent_groups.append((row[0], timestamp))
                recent_groups.sort(key=lambda x: x[1], reverse=False if (sort_arg == '-mr' or sort_arg == '') else True)
            with open(GROUP_PATH, 'r+') as file:
                groups = json.load(file)
                groups['groups'] = {group: groups['groups'][group] for group, _ in recent_groups}
                file.seek(0)
                file.truncate()
                json.dump(groups, file, indent=4)
        else:
            print("no recent groups to sort"); return
    else:
        print("invalid sort argument"); return

def open_url_group(group_name:str=''):
    try:
        group = get_url_group(group_name)
        if group:
            first_url = True
            for url in group.values():
                if first_url:
                    webbrowser.open(url, new=1, autoraise=False)
                    first_url = False
                else:
                    webbrowser.open(url, new=2, autoraise=False)
            with open(RECENT_USE_PATH, 'r+') as file:
                data = csv.reader(file)
                data[group_name] = datetime.now().strftime(TIMESTAMP_FORMAT)
                csv.writer(file).writerows(data)
        else:
            return
    except:
        print("*** error opening group ***"); return
    
def fix_file(args:str='-jc'):
    if args == '-j' or args == '-jc':
        if os.path.exists(GROUP_PATH):
            DEPRECATED_PATH = './group_data/url_groups_deprecated.json'
            iter = 1
            while os.path.exists(DEPRECATED_PATH):
                DEPRECATED_PATH = f'./group_data/url_groups_deprecated_{iter}.json'
            os.rename(GROUP_PATH, DEPRECATED_PATH)
        with open(GROUP_PATH, 'w') as file:
            file.seek(0)
            json.dump({"groups": {}}, file, indent=4)
    elif args =='-c' or args == '-jc':
        if os.path.exists(RECENT_USE_PATH):
            DEPRECATED_PATH = './group_data/recent_url_groups_deprecated.csv'
            iter = 1
            while os.path.exists(DEPRECATED_PATH):
                DEPRECATED_PATH = f'./group_data/recent_url_groups_deprecated_{iter}.csv'
            os.rename(RECENT_USE_PATH, DEPRECATED_PATH)
        with open(RECENT_USE_PATH, 'w') as file:
            file.seek(0)
            csv.writer(file).writerow(['group_name', 'timestamp'])
       
def main():     
    COMMANDS = ['open', 'list', 'sort', 'fix_file']
    while True:
        command = ''
        group_name = ''
        sort_arg = ''
        file_arg = ''
        valid_input = False

        print ("Available commands: ")
        commands = ', '.join(COMMANDS)
        print (commands)
        while True:
            while True:
                while True:
                    command_input = input("Enter command: ").split()
                    command = command_input[0]
                    arg = command_input[1:]
                    if command not in COMMANDS:
                        print("invalid command")
                    elif command == COMMANDS[0] and len(arg) < 1:
                        print("open requires arguments; use an available group name")
                    elif command == COMMANDS[1] and len(arg) > 0:
                        print("list requires no arguments")
                    else:
                        valid_input = True
                        break
                if len(arg) > 1:
                    print("too many arguments, executing first argument only, if applicable")
                    continue
                if command == COMMANDS[0] and arg[0] in get_url_group_names():
                    group_name = arg[0]
                    valid_input = True
                    break
                elif command == COMMANDS[2] and arg[0] in SORT_ARGS:
                    sort_arg = arg[0]
                    valid_input = True
                    break
                elif command == COMMANDS[3] and arg[0] in FILE_ARGS:
                    file_arg = arg[0]
                    valid_input = True
                    break
                else: print("invalid argument")
            if valid_input: break
        if command == COMMANDS[0]:
            open_url_group(group_name)
        elif command == COMMANDS[1]:
            print("=========================")
            for group in get_url_group_names():
                print(group)
            print("=========================")
        elif command == COMMANDS[2]:
            print("=========================")
            sort_file(sort_arg)
            print("groups sorted")
            print("=========================")
        elif command == COMMANDS[3]:
            print("***WARNING: this will deprecate the old file in the directory, if it exists")
            if input("Are you sure you want to continue (y/n): ").casefold() == 'y':
                fix_file(file_arg)
                s = 's' if file_arg == '-jc' else ''
                print("=========================")
                print(f"file{s} fixed")
                print("=========================")
                break
            else:
                break
        
if __name__ == '__main__':
    main()
    