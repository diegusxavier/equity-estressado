import pandas as pd
import json

def  remove_https(original_file):
    with open(original_file, 'r', encoding='utf-8') as raw_file, open('src\\utils\\json_formated.json', 'w', encoding='utf-8') as new_file:
        for line in raw_file:
            if line[0] == '{':
                new_line = line.replace('https://', '')
                new_file.write(new_line)


def json_to_xlsx(file):
    remove_https(file)
                