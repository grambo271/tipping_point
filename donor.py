#--- donor.py ---
# class definition for 'donor' object

import os
import sys
import csv
import string
import math


#--- zip code information ---
from pyzipcode import ZipCodeDatabase

class Donor:

	#--- instance variables ---
	donor_id = ''
	donor_history = []
	num_of_donations = 0

	#--- amount statistics ---
	amount_total = None
	amount_average = None
	amount_std_dev = None
	
	#--- time statistics ---
	time_first_raw = None
	time_last_raw = None
	year_rep_first = None
	year_rep_last = None
	years_total = None
	years_average_diff = None

	#--- location and other shit ---
	zip_code = None
	latitude = None
	longitude = None

	#--- feature representation ---
	features = []
	cluster = None


	##################################################################################################################
	########################[--- INITIALIZATION/INTERFACE ---]########################################################
	##################################################################################################################

	# Function: constructor
	# ---------------------
	# fills out the data fields appropriately
	def __init__ (self, donor_id, donor_history):

		self.donor_id = donor_id
		self.donor_history = sorted(donor_history, key=lambda x:x.date)
		self.num_of_donations = len(self.donor_history)

		#--- time ---
		self.time_first_raw = self.donor_history[0].date_raw
		self.time_last_raw = self.donor_history[-1].date_raw
		

		#--- location ---
		self.zip_code = self.donor_history[-1].zip_code
		if len(self.zip_code) == 5:
			try:
				zcdb = ZipCodeDatabase ()
				zip_code = zcdb[self.zip_code]
				self.latitude = zip_code.latitude
				self.longitude = zip_code.longitude
			except:
				self.latitude = ''
				self.longitude = ''


		#--- higher-level statistics ---
		self.compute_giving_statistics ()


		#--- get feature vector representation ---
		self.get_feature_vector ()



	# Function: get_feature_vector
	# ----------------------------
	# comes up with a feature vector representation of 
	# this donor
	def get_feature_vector (self):

		self.features = []

		#--- amount ---
		self.features.append (self.num_of_donations)
		self.features.append (self.amount_average)
		self.features.append (self.amount_total)
		self.features.append (self.amount_std_dev)

		#--- timing ---
		self.features.append (self.years_total)
		self.features.append (self.years_average_diff)




	# Function: string representation
	# -------------------------------
	# returns a string representation of this object. (call print donor, it will work)
	def __str__ (self):

		intro_string = "###[ " + str(self.donor_id) + "] ###"
		num_of_donations = "	Number of donations: " + str(self.num_of_donations)
		amount_string = "	Amount (total, average, std_dev) = ("+ str(self.amount_total) + ", " + str(self.amount_average) + ", " + str(self.amount_std_dev) + ")"
		time_string = "	Time (years_total, years_average_diff) = (" + str(self.years_total) + ", " + str(self.years_average_diff) + ")"

		return '\n'.join([intro_string, num_of_donations, amount_string, time_string])



	# Function: get_splunk_rep
	# ------------------------
	# returns a splunkable representation of this donation
	# Note: timestamp for users = the first time they gave
	def get_splunk_rep (self):

		#--- break, timestamp and id ---
		break_string = '|||BREAK|||'
		time_string = "timestamp=" + str(self.time_first_raw)
		id_string = "donor_id=" + str(self.donor_id)

		#--- location ---
		zip_code_string = "zip_code=" + str(self.zip_code)
		latitude_string = "gps_lat=" + str(self.latitude)
		longitude_string = "gps_lon=" + str(self.longitude)

		#--- amount ---
		num_donations_string = "number_of_donations=" + str(self.num_of_donations)
		amount_total_string = "amount_total=" + str(self.amount_total)
		amount_avg_string = "amount_average=" + str(self.amount_average) 
		amount_std_dev_string = "amount_std_dev=" + str(self.amount_std_dev)

		#--- time ---
		years_total_string = "years_total=" + str(self.years_total)
		years_avg_diff_string = "years_average_diff=" + str(self.years_average_diff)
		years_std_dev_string = "years_std_dev=" + str(self.years_std_dev)



		return ' '.join ([break_string, time_string, id_string, zip_code_string, latitude_string, longitude_string, num_donations_string, amount_total_string, amount_avg_string, amount_std_dev_string, years_total_string, years_avg_diff_string, years_std_dev_string]) + '\n'




	##################################################################################################################
	########################[--- COMPUTING STATISTICS ---]############################################################
	##################################################################################################################
	# Function: compute_giving_statistics
	# -----------------------------------
	# computes a host of statistics on the user's giving patterns
	def compute_giving_statistics (self):

		### Step 1: get separate lists of giving amounts, dates, etc ###
		amounts_given = [d.amount for d in self.donor_history]
		dates_given = [d.year_rep for d in self.donor_history]


		### Step 2: giving amount statistics (total, avg, std_dev) ###
		self.amount_total = sum(amounts_given)
		self.amount_average = float(self.amount_total) / float(len(amounts_given))
		squared_differences = [(self.amount_average - a)*(self.amount_average - a) for a in amounts_given]
		average_squared_difference = float(sum(squared_differences)) / float(len(squared_differences))
		self.amount_std_dev = math.sqrt (average_squared_difference);


		### Step 3: giving time statistics (start, end, range, avg gap, etc) ###
		self.year_rep_first = dates_given [0]
		self.year_rep_last = dates_given [-1]

		self.years_total = self.year_rep_last - self.year_rep_first
		
		if len(amounts_given) == 1:
			self.years_average_diff = 0
		else:
			self.years_average_diff = float(self.years_total) / float(len(dates_given) - 1)


		sum_sq_diff = 0
		if len(dates_given) <= 2:
			self.years_std_dev = 0.0
		else:
			prev_year = dates_given [0]
			for current_year in dates_given[1:]:
				diff = current_year - prev_year;
				sum_sq_diff += (diff - self.years_average_diff)*(diff - self.years_average_diff)
				prev_year = current_year
			avg_sq_diff = sum_sq_diff / float(len(dates_given) - 1)
			self.years_std_dev = math.sqrt (avg_sq_diff)













