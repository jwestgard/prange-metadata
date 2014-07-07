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

from __future__ import print_function
from pymarc import MARCReader
import json, csv, sys


#-------------------
# CLASSES
#-------------------

class SilentDevice():
    def write(self, s):
        pass


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
    print("\nWorking...", end="")
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
        input_data = csv.DictReader(f)
        for num, row in enumerate(input_data):
            row.update({'filename': filename, 'line': num + 1})
            result.append(row)
        return result

def write_output(filename):
    with open('filename', 'w') as outfile:
        for num in sorted(callnos):
            outfile.write(num + "\n")


#------------------------
# DATA HANDLING FUNCTIONS
#------------------------

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
    
def flatten(rec):
    result = {'leader': rec['leader']}
    for field in rec['fields']:
        for key in field.keys():
            result.update({key: field[key]})
    return result

            #if isinstance(field[key], str):
            #    fields.update(field)
            #elif isinstance(field[key], dict):
            #    for subfield in field[key]['subfields']:
            #        for subcode in subfield.keys():
            #            fields[(key+subcode)] = subfield[subcode]
    

def match_data_to_marc():
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
        print("Reading {0}... ".format(f), end="")
        sheet_data = read_spreadsheet(f)
        print("{0} rows read!".format(len(sheet_data)))
        master_data_list.extend(sheet_data)
    
    print("\nSpreadsheet data read, {0} rows loaded.".format(len(master_data_list)))
    print("\nLoading spreadsheet data...\n")
    
    marc_recs = read_marc(marc_filename)

    print("\nMARC data read, {0} rows loaded.".format(len(marc_recs)))
    
    for rec in marc_recs:
        print(rec)

if __name__ == '__main__':
    main()
