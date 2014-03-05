#!/usr/bin/env python3
# Merges two CSV files based on OID value
import codecs
import csv
import os

_TOTAL_COLUMNS_NUM = [] # Total number of columns
_ALL_COLUMNS = []

def open_file_and_list_rows(file_name):
    """Obtains the list of rows in a file. Prints each item to the screen
    ARGS:
        file_name: A string representing the file to be opened
    return: 
        A list of strings where each string is a colum
    """
    global _TOTAL_COLUMNS_NUM
    global _ALL_COLUMNS

    try:
        with codecs.open(file_name, 'r', 'utf-8') as f:
            # columns is a list of each column in the CSV
            columns = f.readline().strip().split(',')
    except IOError:
        print("Error: file does not exist")
        exit(-1)


    _TOTAL_COLUMNS_NUM.append(len(columns))

    for i, column in enumerate(columns):
        column_with_fileName = file_name + "." + column
        _ALL_COLUMNS.append(column_with_fileName)
        print(str(i) + ")\t["  + column_with_fileName + "]")
    return columns

def get_rows_from_csv(fileName):
    """ Function to get the values from a CSV file
    ARGS:
        fileName: name of the file to read
        be delimeted by ','

    return:
        list of rows from the file. """

    #Opening the file as a csv.reader object
    with codecs.open(fileName, 'r', 'utf-8') as csvFile:
        csvReader = csv.reader(csvFile)
        columns = next(csvReader, None)

        #print("\nColumns of " + fileName + " are:")
        #for idx, column in enumerate(columns):
        #    print(str(idx) + ") " + str(column))

        items = [] #Holder for items I need in the csv
        for row in csvReader:
            items.append(row)
        return(items)

def combine_all_ticket_values(CSV1, CSV2, OID_1, OID_2):
    """Combines two list of rows with matching OID values from Ticket_Matches
    ARGS:
        CSV1: First list of rows 
        CSV2: Second list of rows 
        OID_1: Column number for first CSV's OID
        OID_2: Column number for second CSV's OID

    return:
        list of rows where the OID matches"""

    #row2 can have multiple instances, append all to single row1
    outputCSV = []
    for row1 in CSV1:
        OID = row1[OID_1] # Saving the OID value of the ticket
        temp = [row1] # Add the row from the first file
        for row2 in CSV2: # Adding all relevant rows from second file
            if row2[OID_2] == OID:
                # Add the history data
                temp = temp + row2
        # Removing all NULL's
        temp = [item for item in temp if item != 'NULL']
        # Converting all strings to upper case
        temp = [item.upper() for item in temp]
        outputCSV.append(temp)

    return(outputCSV)

def get_only_summary(CSV1, summary_column):
    """Creates a list of just summary's
    ARGS:
        CSV1: List of rows
        summary_column: Column number for the summary

    return:
       List of rows where each row has the itemID and Summary only """
    outputCSV = []
    for row1 in CSV1:
        temp = [row1[summary_column]]

        # Removing all NULL's
        temp = [item for item in temp if item != 'NULL']
        # Converting all strings to upper case
        temp = [item.upper() for item in temp]
        outputCSV.append(temp)
    return(outputCSV)

def get_only_summary_and_comments(CSV1, CSV2, OID_1, OID_2,\
        summary_column, comments_column):
    """Creats a list of just summary and comments.
        Comments are combined only if the Action column has "Description".
    ARGS:
        CSV1: First list of rows
        CSV2: Second list of rows
        OID_1: Column number for first CSV's OID
        OID_2: Column number for second CSV's OID
        summary_column: Column number for the summary
        action_column: Column number for the action
        comments_column: Column number for the comments

    return:
        List of rows where with the itemID, summary, and all comments"""

    #row2 can have multiple instances, append all to single row1
    outputCSV = []
    for row1 in CSV1:
        OID = row1[OID_1] # Saving the OID value of the ticket
        temp = [row1[summary_column]] # Add the summary from the first file
        for row2 in CSV2: # Adding all relevant rows from second file
            if (row2[OID_2] == OID):
                # Add the history data
                temp = temp + [row2[comments_column]]
        # Removing all NULL's
        temp = [item for item in temp if item != 'NULL']
        # Converting all strings to upper case
        temp = [item.upper() for item in temp]
        outputCSV.append(temp)

    return(outputCSV)

def write_list_to_file(CSVIN):
    """Write the list of tickets to a file
    ARGS:
        CSVIN: The list of tickets to write

    return:
        None"""
    out_file_name = input("Name of file to write to: ")

    with open(out_file_name, 'w') as f:
        for item in CSVIN:
            f.write( ", ".join(item) + "\n")

def main():
    # Getting the information about the main file
    main_file = input("Please enter the main file: ")
    open_file_and_list_rows(main_file)


    #TODO(Bader): Make UI more intuitive 
    if(input("Only do summary? [y/N]: ").upper() == 'Y'):
        summary_column = int(input("Enter the column with the summary: "))
        print("Extracting data from files")
        CSV1 = get_rows_from_csv(main_file)
        print("File:[%s] is done" % (main_file))

        output_csv = get_only_summary(CSV1, summary_column)
        print("Done getting summary columns")
        write_list_to_file(output_csv)
        return()

    # Get the OID column to match everything else with
    main_OID_column = int(input("Enter the column with the OID: "))

    # Getting information about the second file
    second_file = input("Please enter the second file: ")
    open_file_and_list_rows(second_file)
    second_OID_column = int(input("Enter the column with the OID: "))

    # Combining the data of the two CSV files
    print("Extracting data from files")
    CSV1 = get_rows_from_csv(main_file)
    print("File:[%s] is done" % (main_file))
    CSV2 = get_rows_from_csv(second_file)
    print("File:[%s] is done" % (second_file))

    summary_column = int(input("Enter the column "
        "with the summary from the first file: "))
    comments_column = int(input("Enter the column with the comments: "))

    output_csv = get_only_summary_and_comments(CSV1, CSV2,\
            main_OID_column, second_OID_column,  \
            summary_column, comments_column)

    write_list_to_file(output_csv)
    return()

if __name__ == '__main__':
    main()