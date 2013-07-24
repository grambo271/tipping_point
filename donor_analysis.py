#!/usr/bin/python
#--- donor_analysis.py ---
# provides an analysis of donor data
# as well as predictions and whatnot

import os
import sys
import csv
import string
import pickle

#--- custom modules ----
from donation import Donation
from donor import Donor



#--- data filenames ---
donations_csv_filename = 'data/donor_data.csv'
donations_pickle_filename = 'data/donations.obj'
donors_pickle_filename = 'data/donors.obj'


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



##################################################################################################################
########################[--- LOAD/SAVE DATA ---]##################################################################
##################################################################################################################

# Function: get_donations
# ------------------------
# given a filename containing a csv with all of the donor information,
# this will return a list of dicts, each describing an individual donation.
def get_donations (filename):

	### Step 1: open files ###
	csv_file = open (filename, 'rU')
	reader = csv.reader (csv_file, delimiter=',', quotechar='"', dialect=csv.excel_tab)


	### Step 2: get the fields without spaces ###
	fields_raw = reader.next ()
	fields_nospaces = [f.replace(' ', '_') for f in fields_raw]
	fields = []
	exclude = set(string.punctuation)
	exclude.remove('_')
	for field in fields_nospaces:
		new_field = ''.join(ch for ch in field if ch not in exclude)
		fields.append (new_field)


	### Step 3: for each row, create a 'donation' dict ###
	donations = []
	donation_id = 0
	for row in reader:


		if row[1]: #throw out data points without an amount...
			new_donation = Donation (row[0], row[1], row[2], row[3], row[4], row[5], donation_id)
			donations.append (new_donation)
			donation_id += 1


	### Step 4: close files and return ###
	csv_file.close ()
	return donations


# Function: get_donors
# --------------------
# given a list of donors, this function will return a list of donors
def get_donors (donations):

	donors = []
	while (len (donations) > 0):

		### Step 1: get all donations of a given id ###
		search_id = donations[0].account_id
		donor_history = [d for d in donations if d.account_id == search_id]

		### Step 2: remove all of those donors from the list ###
		donations = list(set(donations).difference (set(donor_history)))

		### Step 3: make a donor appropriately ###
		new_donor = Donor (search_id, donor_history)
		donors.append (new_donor)

	return donors

# Function: save_data
# -------------------
# function to save all the donor/donation data that we have amassed
def save_data (donors, donations):

	print "	---> Status: saving donations"
	pickle.dump (donations, open(donations_pickle_filename, 'wb'))

	print "	---> Status: saving donors"
	pickle.dump (donors, open(donors_pickle_filename, 'wb'))


# Function: load_data
# -------------------
# function to load donor/donations information
def load_data (donations_filename, donors_filename):
	donations = pickle.load (open(donations_filename, 'rb'))
	donors = pickle.load (open(donors_filename, 'rb'))
	return (donations, donors)






if __name__ == '__main__':

	### --- set arguments --- ###
	load = False
	save = True



	### Step 1: get/load the data ###
	if not load:
		print "---> Status: extracting data from csv files"
		donations = get_donations (donations_csv_filename);	
		donors = get_donors (donations)
	else:
		print "---> Status: loading data from pickled files"
		(donations, donors) = load_data (donations_pickle_filename, donors_pickle_filename)


	#############
	for donor in donors:
		if len(donor.donor_history) == 4:
			print donor


	### Final Step: save data ###
	if (save):
		print "---> Status: pickling data"
		save_data (donors, donations)







