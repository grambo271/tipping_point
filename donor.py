#--- donor.py ---
# class definition for 'donor' object

import os
import sys
import csv
import string


class Donor:

	#--- instance variables ---
	donor_id = ''
	history = []

	# Function: constructor
	# ---------------------
	# fills out the data fields appropriately
	def __init__ (self, donor_id, donor_history):

		self.donor_id = donor_id
		self.donor_history = donor_history


	# Function: string representation
	# -------------------------------
	# returns a string representation of this object. (call print donor, it will work)
	def __str__ (self):

		top_string = "##########[--- Donor #" + str(self.donor_id) + " ---]##########"
		history_string = '\n'.join([str(s) for s in self.donor_history])

		return '\n'.join([top_string, history_string])




