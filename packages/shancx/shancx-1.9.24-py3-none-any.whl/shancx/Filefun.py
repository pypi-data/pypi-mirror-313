import gzip

with gzip.open(file_path, 'rt') as file:
    first_line = file.readline()
    
import os 
def getcurrent_file_path():
    current_file_path = os.path.abspath(__file__) 
    current_folder_path = os.path.dirname(current_file_path)
    return current_folder_path
"""
CSV

import gzip
import csv

with gzip.open(file_path, 'rt') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

XML

import gzip
import xml.etree.ElementTree as ET

with gzip.open(file_path, 'rt') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)

YAML        

import gzip
import yaml
with gzip.open(file_path, 'rt') as file:
    data = yaml.safe_load(file)
    print(data)

TEXT

import gzip

with gzip.open(file_path, 'rt') as file:
    for line in file:
        print(line.strip())

"""