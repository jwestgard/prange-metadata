#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarc import MARCReader

def flatten(rec):
    fields = {}
    for field in rec['fields']:
        for value in field.keys():
            if isinstance(field[value], str):
                fields.update(field)
            elif isinstance(field[value], dict):
                for subfield in field[value]['subfields']:
                    for subcode in subfield.keys():
                        fields[(value+subcode)] = subfield[subcode]
    result = { rec['leader']: fields }
    return result
        
def pretty_print(leader, fields):
    header = "\nLeader = {}".format(leader)
    print(header)
    print("=" * len(header))
    col1width = max([len(k) for k in fields.keys()])
    for k in sorted(fields.keys()):
        col1 = k.rjust(col1width)
        col2 = fields[k]
        print("  {0} : {1}  ".format(col1, col2))

def read_data():
    record_set = {}
    inputfile = input("Enter the name of the MARC file to read: ")
    with open(inputfile, 'rb') as fh:
        reader = MARCReader(fh, force_utf8=True)
        for record in reader:
            mydict = record.as_dict()
            record_set.update(flatten(mydict))
    return record_set

record_set = read_data()
for k, v in record_set.items():
    pretty_print(k, v)
