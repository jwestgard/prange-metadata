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
    print("\nWorking...", end="")
    with open(inputfile, 'rb') as fh:
        reader = MARCReader(fh, force_utf8=True)
        count = 0
        for record in reader:
            count += 1
            mydict = record.as_dict()
            record_set.update(flatten(mydict))
            print(count)
            #if len(record_set.keys()) % 250 == 0:
            #    print(".", end="", flush=True)
    return record_set

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
    
record_set = read_data()
for k, v in record_set.items():
    pretty_print(k, v)
callnos, nocall = data_stats(record_set)

with open('output.txt', 'w') as outfile:
    for num in sorted(callnos):
        outfile.write(num + "\n")
        
print(nocall)
