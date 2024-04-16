import pandas as pd
import json

def  remove_https(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            new_line = line.replace('https://', '')
            

def json_to_xlsx(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if line[0] == '{':
                data = dict(line)
                print(data)
                