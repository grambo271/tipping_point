#--- donation.py ---
# class definition for 'donation' object

import os
import sys
import csv
import string

#--- zip code information ---
from pyzipcode import ZipCodeDatabase

class Donation:

	#--- instance variables ---
	date_raw = ''
	date = ''
	amount = ''
	campaign_name = ''
	zip_code = ''
	latitude = ''
	longitude = ''
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

		#--- time ---
		self.date_raw = date
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


		#--- location ---
		self.zip_code = zip_code
		if len(self.zip_code) == 5:
			try:
				zcdb = ZipCodeDatabase ()
				zip_code = zcdb[self.zip_code]
				self.latitude = zip_code.latitude
				self.longitude = zip_code.longitude
			except:
				self.latitude = ''
				self.longitude = ''


		self.campaign_name = campaign_name
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



	# Function: get_splunk_rep
	# ------------------------
	# returns a splunkable representation of this donation
	def get_splunk_rep (self):

		#--- break and timestamp ---
		break_string = '|||BREAK|||'
		time_string = "timestamp=" + self.date_raw + "'"

		#--- time ---
		year_rep_string = "year_rep=" + str(self.year_rep)
		year_string = "year=" + str(self.year)
		month_string = "month=" + str(self.month)
		day_string = "day=" + str(self.day)
		
		#--- ammount ---
		amount_string = "amount=" +  str(self.amount)

		#--- location ---
		zip_code_string = "zip_code=" + str(self.zip_code)
		latitude_string = "gps_lat=" + str(self.latitude)
		longitude_string = "gps_lon=" + str(self.longitude)

		#--- account id/campaign name ---
		account_id_string = "account_id=" +  str(self.account_id)
		campaign_name_string = "campaign_name='" + str(self.campaign_name) + "'"

		return ' '.join ([break_string, time_string, year_rep_string, year_string, month_string, day_string, amount_string, campaign_name_string, zip_code_string, latitude_string, longitude_string, account_id_string]) + '\n'










