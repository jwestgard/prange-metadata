#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################
#                                                                          #
#                            MARC-HARVEST.PY                               #
#               A script to harvest data from MARC records                 #
#              and match data to existing spreadsheet rows.                #    
#              Version 1 -- July 2014 -- Joshua A. Westgard                #
#                                                                          #
############################################################################
#                                                                          #       
#   Usage:   python3 marc-harvest.py [marcfile] [pathtospreadsheet(s)]     #
#                                                                          #       
############################################################################


#-------------------
# MODULE IMPORTS
#-------------------

from pymarc import MARCReader
import json, csv, sys, re


#-------------------
# I/O FUNCTIONS
#-------------------

def pretty_print(leader, fields):
    header = "\nLeader = {}".format(leader)
    print(header)
    print("=" * len(header))
    col1width = max([len(k) for k in fields.keys()])
    for k in sorted(fields.keys()):
        col1 = k.rjust(col1width)
        col2 = fields[k]
        print("  {0} : {1}  ".format(col1, col2))

def read_marc(filename):
    result = []
    with open(filename, 'rb') as fh:
        reader = MARCReader(fh, force_utf8=True)
        count = 0
        for record in reader:
            count += 1
            if count % 500 == 0:
                print(".", end="")
                sys.stdout.flush()
            rec_dict = flatten(record.as_dict())
            result.append(rec_dict)
    return result

def read_spreadsheet(filename):
    with open(filename, 'r') as f:
        result = []
        input_data = csv.DictReader(f, delimiter=",")
        for num, row in enumerate(input_data):
            row.update({'filename': filename, 'line': num + 1})
            result.append(row)
        return result

def write_output(filename):
    with open('filename', 'w') as outfile:
        for num in sorted(callnos):
            outfile.write(num + "\n")


#---------------------------
# DATA ANALYSIS AND MATCHING
#---------------------------

def data_stats(data):
    ids = []
    nocall = []
    for r in data:
        try:
            id = data[r]['852h']
        except:
            print("[field not found]")
            nocall.append(data[r])
        try:
            suffix = data[r]['852i']
        except:
            suffix = ""
        ids.append(id + suffix)
    print("Records: {0}".format(len(data)))
    print("852h nos: {0}".format(len(ids)))
    return ids, nocall

def expand(par, ch):
    if isinstance(ch, dict):
        for key in ch.keys():
            expand(key, ch[key])
    elif isinstance(ch, list):
        for item in ch:
            expand(ch, item)
    elif isinstance(ch, str):
        print("{0}: {1}".format(par, ch))

def flatten(rec):
    flat_record = []
    flat_record.append(("Leader", rec['leader']))
    for field in rec['fields']:
        for k, v in field.items():
            if isinstance(v, str):
                flat_record.append((k, v))
            elif isinstance(v, dict):
                for subfield in v['subfields']:
                    for sk, sv in subfield.items():
                        flat_record.append((k + sk, subfield[sk]))
    return flat_record
    
def match_data_to_marc():
    pass


#----------------------------
# DATA MANIPULATION FUNCTIONS
#----------------------------  

def remove_brackets(field):
    return field.strip([ "[", "]" ])

# Normalize the author field so it includes the author's name only
# Japanese terms for editor = 編, 編纂, 編集, 編輯
# Japanese word for author = 著

def remove_author_editor_terms(field):
    for eterm in ["編", "編纂", "編集", "編輯"]:
        if eterm in field:
            result = field.replace(eterm, "")
        elif "著" in field:
            result = field.replace("著", "")
        else:
            result = field
    return result

def remove_yen_abbreviation(field):
    if "Y" in field:
        result = field.replace("Y", "")
    else:
        result = field
    return result

def sum_page_counts(field):
    m = re.search(r'.+p\.', field)
    if m:
        total = sum([int(d) for d in re.findall(r'\d+', m.group())])
        return total

def move_dimensions_info(field):
    m = re.search(";( )?\d+( )?(x \d+)?( )?cm(\.)?", field)
    if m:
        return m.group().replace(";", "").strip()

def remove_Japanese_dates(field):
    pass


#-------------------
# MAIN FUNCTION
#-------------------         

def main():
    master_data_list = []
    marc_filename = sys.argv[1]
    inputfiles = [f for f in sys.argv[2:]]
    print("\nLoading spreadsheet data...\n")
    for f in inputfiles:
        print("\n\nReading {0}... ".format(f), end="")
        sheet_data = read_spreadsheet(f)
        print("{0} rows read!".format(len(sheet_data)))
        print("{} columns in sheet!\n".format(len(sheet_data[0])))
        for key in sheet_data[0].keys():
            print(key) 
        master_data_list.extend(sheet_data)
    print("\nSpreadsheet data read, {0} rows loaded.".format(len(master_data_list)))
    
    for num, record in enumerate(master_data_list):
        print("\nRecord #{0}".format(num))
        print("  {0} => {1}".format(record['author1-jp'],
                                    remove_author_editor_terms(record['author1-jp'])))
        print("  {0} => {1}".format(record['price'],
                                  remove_yen_abbreviation(record['price'])))
        print("  {0} => {1}".format(record['pages'],
                                  sum_page_counts(record['pages'])))
        print("  {0} => {1}".format(record['pages'],
                                  move_dimensions_info(record['pages'])))
        
    print("\nLoading MARC file ", end="")
    marc_data = read_marc(marc_filename)
    print("\n\nMARC file read; {0} records loaded!".format(len(marc_data))) 

    for x in range(100):
        print(x)
    
    
    #all_columns = set()
    #for row in master_data_list:
    #    all_columns.update(row.keys())
    #for col in sorted(all_columns):
    #    print(col)

if __name__ == '__main__':
    main()
