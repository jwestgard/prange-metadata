# Prange Metadata Harvesting and Manipulation Program

## Description
A program to process and validate metadata spreadsheets, pulling additional data from MARC records using pymarc.

##Data Paths
    ~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/csv/
    ~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/excel/
    ~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/marc/
    ~/Box\ Sync/PrangeMetadataStuff/CSV-data-conversion/tsv/

## Pseudocode
1. Read Spredsheet Data.
2. Load MARC file into array using pymarc.
3. Check Spreadsheet Header Rows Against One Another.
4. Search for matching MARC records.
5. Report on possible matches.
6. Pull data over from MARC to main array.
7. Output main array into single CSV file for ingest into Fedora.

## Data Wrangling Algorithm
1. Remove brackets from author names (were used to indicate supplied names, but not needed for Digital Collections).
2. Separate the term for "editor" (編, 編纂, 編集, 編輯) from the name of the editor; and likewise remove the term for author (著) from the author column
3. Separate page count info from dimensions; create sum of page counts where multiple page counts have been listed.
4. Remove Japanese dates from publication date field.  
5. Remove the Y abbreviation for Yen.

## Subject Terms Matching
1. Compare call no. from spreadsheet against field 852h (where multiple call nos. in Aleph, check each one); if only one match is found, trust the match.
2. If no match found, try matching 852i or combined 852h + i.
3. If no match found, try matchign after removing volume info from call no.
4. If no match found, try matching on Author/Title.
5. If multiple matches found, flag record for follow up.
6. Output a report of all matches by each of the various methods, as well as a list of unmatched records from the spreadsheets.

