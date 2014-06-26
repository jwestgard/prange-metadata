#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarc import MARCReader

def flatten(rec):
    fields = {}
    for field in rec:
        for value in field.keys():
            if isinstance(field[value], str):
                fields.update(field)
            elif isinstance(field[value], dict):
                for subfield in field[value]['subfields']:
                    for subcode in subfield.keys():
                        fields[(value+subcode)] = subfield[subcode]
    return fields
        
def pretty_print(record):
    header = "\nLeader = {0}".format(record['leader'])
    print(header)
    print("=" * len(header))
    col1width = max([len(k) for k in record.keys()])
    for k in sorted(record.keys()):
        col1 = k.rjust(col1width)
        col2 = record[k]
        print("  {0} : {1}  ".format(col1, col2))

def read_data():
    inputfile = input("Enter the name of the MARC file to read: ")
    print("\nWorking...", end="")
    with open(inputfile, 'rb') as fh:
        reader = MARCReader(fh, force_utf8=True)
        count = 0
        record_set = []
        for item in reader:
            record = {}
            count += 1
            if count % 1000 == 0:
                print(count, end=" ", flush=True)
            mydict = item.as_dict()
            record['id'] = count
            record['leader'] = mydict['leader']
            flat = flatten(mydict['fields'])
            for key in flat:
                record.update({key : flat[key]})
            record_set.append(record)
    return record_set

def save_data(dataset):
    with open('output.txt', 'w') as outfile:
        for item in dataset:
            outfile.write(item + "\n")

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
for record in record_set:
    pretty_print(record)

