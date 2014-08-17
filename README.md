# Prange Metadata Harvest and Manipulation Program

## Description
A program to process and validate metadata spreadsheets, pulling additional data from MARC records using pymarc.

##Data Paths
{code}~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/csv/
~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/excel/
~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/marc/
~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/tsv/{code}

## Pseudocode

1. Read Spredsheet Data.
2. Load MARC file into array using pymarc.
3. Check Spreadsheet Header Rows Against One Another.
4. Search for matching MARC records.
5. Report on possible matches.
6. Pull data over from MARC to main array.
7. Output main array into single CSV file for ingest into Fedora.
