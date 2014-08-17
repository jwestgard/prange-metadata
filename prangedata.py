#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import json, csv, sys

def read_file_data(filename):
    with open(filename, 'r') as f:
        result = []
        input_data = csv.DictReader(f)
        for num, row in enumerate(input_data):
            row.update({'filename': filename, 'line': num + 1})
            result.append(row)
        return result
    
def read_marc_records():
    pass

def match_data_to_marc():
    pass

def write_output():
    pass

master_data_list = []
inputfiles = [f for f in sys.argv[1:]]

for f in inputfiles:
    print("Reading {0}... ".format(f), end="")
    sheet_data = read_file_data(f)
    print("{0} rows read!".format(len(sheet_data)))
    master_data_list.extend(sheet_data)
    
for row in master_data_list:
    print(row['filename'], row['line'])


