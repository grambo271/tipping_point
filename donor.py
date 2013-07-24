#--- donor.py ---
# class definition for 'donor' object

import os
import sys
import csv
import string
import math


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
	time_first = None
	time_last = None
	years_total = None
	years_average_diff = None


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
		self.compute_giving_statistics ()

		print self


	# Function: string representation
	# -------------------------------
	# returns a string representation of this object. (call print donor, it will work)
	def __str__ (self):

		top_string = "##########[--- Donor #" + str(self.donor_id) + " ---]##########"
		amount_stat_string = "Amount: (total, average, std_dev) = (" + str(self.amount_total) + ", " + str(self.amount_average) + ", " + str(self.amount_std_dev) + ")"
		time_stat_string = "Time: (total, average, std_dev) = (" + str(self.years_total) + ", " + str(self.years_average_diff) + ", " + str(self.years_std_dev) + ")"
		history_string = '\n'.join([str(s) for s in self.donor_history])

		return '\n'.join([top_string, amount_stat_string, time_stat_string, history_string])






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
		self.time_first = dates_given [0]
		self.time_last = dates_given [-1]

		self.years_total = self.time_last - self.time_first
		
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









