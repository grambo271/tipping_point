#!/usr/bin/python
#--- donor_analysis.py ---
# provides an analysis of donor data
# as well as predictions and whatnot

import os
import sys
import csv
import string
import pickle
import copy

#--- ML ---
from sklearn.cluster import KMeans

#--- custom modules ----
from donation import Donation
from donor import Donor



#--- data filenames ---
donations_csv_filename = 'data/input/donor_data.csv'
donations_pickle_filename = 'data/input/donations.obj'
donors_pickle_filename = 'data/input/donors.obj'
donations_splunk_output = 'data/splunk/donations.txt'
donors_splunk_output = 'data/splunk/donors.txt'


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

def print_status (stage, status):
	print "-----> " + stage + ': ' + status

def print_message (message):
	print "-" * len(message)
	print message
	print "-" * len(message)





class Tipping_Point_Analyzer:

	#--- Filenames ---
	filenames = {}			# dict for holding filenames

	#--- Data ---
	donors 		= []		# list of all donors
	donations 	= []		# list of all donations



	def __init__ (self, filenames):

		### Step 1: get filenames ###
		self.filenames = filenames

		### Step 2: read in donors, donations ###
		#--- If you want to unpickle ---
		print_status ("Initialization", "Loading donors/donations")
		self.load_data ()
		#--- If you want to load from csv file ---
		# print_status ("Initialization", "Getting donations")
		# self.get_donations (filenames['infile'])
		# print_status ("Initialization", "Getting donors")
		# self.get_donors ()
		# print_status ("Initialization", "Pickling data")		
		# self.save_data ()
		# self.print_data_summary ()

		### Step 2: clustering ###
		print_status ("Initialization", "Performing clustering")
		self.cluster_donors ()


	##################################################################################################################
	########################[--- CLUSTER DONORS ---]##################################################################
	##################################################################################################################
	# Function: cluster_donors 
	# ------------------------
	# performs clustering procedures on the donors in order to stratify them
	def cluster_donors (self):

		km = KMeans (n_clusters=8, init='k-means++', max_iter=300)
		donor_examples = [d.features for d in self.donors]
		labels = km.fit_predict (donor_examples)
		for index, l in enumerate(labels):
			self.donors[index].cluster = l

		for i in range(5):
			
			print "##################################################[ CLUSTER ", i, " ]################################\n"
			this_cluster = [d for d in self.donors if d.cluster == i]
			print len(this_cluster)
			# for c in this_cluster:
				# print c
			# print "\n\n"





	##################################################################################################################
	########################[--- LOAD/SAVE DATA ---]##################################################################
	##################################################################################################################

	# Function: get_donations
	# ------------------------
	# given a filename containing a csv with all of the donor information,
	# this will return a list of dicts, each describing an individual donation.
	def get_donations (self, filename):

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
		self.donations = []
		donation_id = 0
		for row in reader:


			if row[1]: #throw out data points without an amount...
				new_donation = Donation (row[0], row[1], row[2], row[3], row[4], row[5], donation_id)
				self.donations.append (new_donation)
				donation_id += 1


		### Step 4: close files and return ###
		csv_file.close ()


	# Function: get_donors
	# --------------------
	# given a list of donors, this function will return a list of donors
	def get_donors (self):

		self.donors = []

		temp_donations = copy.copy (self.donations)
		while (len (temp_donations) > 0):

			### Step 1: get all donations of a given id ###
			search_id = temp_donations[0].account_id
			donor_history = [d for d in temp_donations if d.account_id == search_id]

			### Step 2: remove all of those donors from the list ###
			for d in donor_history:
				temp_donations.remove (d)

			### Step 3: make a donor appropriately ###
			new_donor = Donor (search_id, donor_history)
			self.donors.append (new_donor)



	# Function: print_data
	# --------------------
	# displays a high-level analysis of data presented
	def print_data_summary (self):

		print_message ("Data input: ")
		print "	# of donations:", len(self.donations)
		print "	# of donors: ", len(self.donors)
		print "\n"


	# Function: save_data
	# -------------------
	# function to save all the donor/donation data that we have amassed
	def save_data (self):

		pickle.dump (self.donations, open(self.filenames['donations_pickle_file'], 'wb'))
		pickle.dump (self.donors, open(self.filenames['donors_pickle_file'], 'wb'))



	# Function: load_data
	# -------------------
	# function to load donor/donations information
	def load_data (self):
		self.donations = pickle.load (open(self.filenames['donations_pickle_file'], 'r'))
		self.donors = pickle.load (open(self.filenames['donors_pickle_file'], 'r'))




	##################################################################################################################
	########################[--- DUMPING INTO SPLUNK ---]#############################################################
	##################################################################################################################
	# Function: dump_into_splunk
	# --------------------------
	# given the path to a file to dump into, this function will dump all contacts and donations
	# into the file
	def dump_into_splunk (donors, donations, donors_filename, donations_filename):

		donors_file = open(donors_filename, 'w')
		for donor in donors:
			donors_file.write (donor.get_splunk_rep ())

		donations_file = open (donations_filename, 'w')
		for donation in donations:
			donations_file.write (donation.get_splunk_rep())




if __name__ == '__main__':

	filenames = {	'infile': '/Users/jhack/Programming/Splunk/tipping_point/data/input/donor_data.csv',
					'donations_pickle_file': '/Users/jhack/Programming/Splunk/tipping_point/data/input/donations.obj',
					'donors_pickle_file': '/Users/jhack/Programming/Splunk/tipping_point/data/input/donors.obj',
					'outfile': '/Users/jhack/Programming/Splunk/tipping_point/data/splunk/output.txt'}

	tp = Tipping_Point_Analyzer (filenames)








