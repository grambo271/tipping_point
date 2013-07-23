#!/usr/bin/python
#
# Script: format_data.py
# ---------------------
# Usage: ./format_data.py input_directory output_directory
#
# this script takes all of the .csv files in the input directory and generates splunk-readable files in the
# output directory, one for each input file and with the extension changed to .txt. special treatment for the 
# 'campaigns' files!

import os
import sys
import csv
import string


#--- globals ---
break_pattern = '|||BREAK|||'
csv_filename = 'data/donor_data.csv'
splunklog_filename = 'data/donor_data.txt'


##################################################################################################################
########################[--- UTILITIES ---]#######################################################################
##################################################################################################################
# Function: print_error
# ---------------------
# notifies the user of an error, how to correct it, then exits
def print_error (error_message, correction_message):
	print "ERROR: 	", error_message
	print "	---"
	print "	", correction_message
	exit ()


# Function: dump_row 
# ------------------
# dumps a row to the outfile
def dump_row (outfile, fields, row):

	### Step 1: timestamp ###
	pledge_date_index = fields.index('Pledge_Date')
	pledge_date = row[pledge_date_index]
	time_string = ' timestamp="' + pledge_date.replace('/', '-') + '"'

	dump_string = break_pattern
	dump_string += time_string
	for i in range (len(row)):
		dump_string += ' ' + fields[i] + '="' + row[i] + '"'

	dump_string += "\n"
	print dump_string
	outfile.write (dump_string)
	return 





##################################################################################################################
########################[--- MAIN OPERATION ---]##################################################################
##################################################################################################################

# Function: reformat_csv_file
# ---------------------------
# given filename_raw and filename_formatted, this will dump the contents of a csv file into a splunk-readable
# logfile format
def reformat_csv_file (filename_raw, filename_formatted):

	### Step 1: open files ###
	raw_file = open (filename_raw, 'rU')
	formatted_file = open(filename_formatted, 'w')
	reader = csv.reader (raw_file, delimiter=',', quotechar='"', dialect=csv.excel_tab)


	### Step 2: get the fields without spaces ###
	fields_raw = reader.next ()
	fields_nospaces = [f.replace(' ', '_') for f in fields_raw]
	fields = []
	exclude = set(string.punctuation)
	exclude.remove('_')
	for field in fields_nospaces:
		new_field = ''.join(ch for ch in field if ch not in exclude)
		fields.append (new_field)


	for row in reader:
		if len(row) != len(fields):
			print_error ('Something in the csv file is fucked up...', 'number of fields is not the same as number of columns in a row')
		else:
			dump_row (formatted_file, fields, row)

	raw_file.close ()
	formatted_file.close ()















if __name__ == "__main__":

	print "---> Status: reformatting " + csv_filename
	reformat_csv_file (csv_filename, splunklog_filename)










