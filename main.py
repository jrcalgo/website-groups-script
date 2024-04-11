import tkinter as tk
import urllib
import json
import os

## GROUP_PATH to url groups file
GROUP_PATH = './group_data/url_groups.json'

## URL key numbers are irrelevant; only for key differentiation; URLs are opened sequentially based on dict position
def new_url_group(group:dict={'name':'group','url1':'url','url2':'url'}):
    url_keys = [key for key in group.keys() if key in 'url'.casefold()]
    if not group.has_key('name') and :
        print("group dictionary must contain group name key")
    elif url_keys.isEmpty():
        print("no URL keys specified")
    elif not 'name' in group.keys() and not 'url' in group.keys():
        print("only 'name' and 'url' keys accepted only")
    
    mode = 'w' if os.GROUP_PATH.isfile(GROUP_PATH) else 'a'
    with open(GROUP_PATH, mode) as output:
        json.dump(group, output)
        
def get_url_group(group_name:str="") -> dictionary:
    try:
        with open(GROUP_PATH, 'r') as input:
            groups = json.load(input)
    except IOError as e:
        print e
        print("IOError: Unable to open url_groups.json. Terminating execution.")
        exit(1)
        
    if group_name in groups['name'].values():
        print groups
    else
        print("group name not found")
        
        
def edit_url_group(group_name:str=''):
    group = get_url_group(group_name)
    
    with open(GROUP_PATH, 'a') as output:
        
    

def remove_url_group(group_name:str=''):
    group = get_url_group(group_name)
    
    

def open_url_group(group_name:str=''):
    

def main():
    
    
    
    
if __init__ == main:
    main()
