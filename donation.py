#--- donation.py ---
# class definition for 'donation' object

import os
import sys
import csv
import string

class Donation:

	#--- instance variables ---
	date = ''
	amount = ''
	campaign_name = ''
	zip_code = ''
	account_id = ''
	donation_id = ''

	month = ''
	day = ''
	year = ''
	year_rep = ''


	# Function: constructor
	# ---------------------
	# fills out the data fields appropriately
	def __init__ (self, date, amount, stage, campaign_name, zip_code, account_id, donation_id):

		#--- date ---
		splits = date.split ('/')
		self.month = int(splits[0])
		self.day = int(splits[1])
		self.year = int('20' + splits [2])
		self.date = (self.year, self.month, self.day)

		self.year_rep = self.year + float(self.month) / 12.0

		#--- amount ---
		amount = amount.replace ('$', '')
		amount = amount.replace (',', '')
		amount = amount.split('.')[0]
		self.amount = int(amount)


		self.campaign_name = campaign_name
		self.zip_code = zip_code
		self.account_id = account_id
		self.donation_id = donation_id



	# Function: string representation
	# --------------------
	# prints out all info on this object 
	def __str__ (self):
		top_string = "----- info for donation id #" + str(self.donation_id) + " -----"
		date_string = "	date = " + str(self.date)
		year_rep_string = "	year_rep = " + str(self.year_rep) 
		amount_string = "	amount = " +  str(self.amount)
		campaign_name_string = "	campaign_name = " + str(self.campaign_name)
		zip_code_string = "	zip_code = " + str(self.zip_code)
		account_id_string = "	account_id = " +  str(self.account_id)

		return '\n'.join([top_string, date_string, year_rep_string, amount_string, campaign_name_string, zip_code_string, account_id_string])















