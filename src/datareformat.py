import csv
import numpy as np
import scipy as sp
import pandas as pd
from pandas import DataFrame, Series
import matplotlib as mpl
# import matplotlib.pyplot as plt


class DataReformat:
	# Class for reformating exported csv files from Ekos in preperation
	# for porting them into Google Sheets
	#
	# Specifically for Allocation GS tool

	def fgoh_reformat(self, PATH, filename='fgoh.csv'):
		# Reformats finished goods on hand csv file in preperation
		# for porting data into Google Sheets

		print("Reformating %s" % filename)
		df = pd.read_csv(PATH + filename)
		df = df.rename(index=str, columns={'On&#8209;Hand':'On Hand'})
		df.to_csv(path_or_buf=PATH + 'fgohGS.csv')
		return

	def orders_reformat(self, PATH, invfile='invoices.csv', 
	                    sofile='salesorders.csv'):
		# Takes invoices csv file and sales orders csv file, reformats
		# and merges them into one csv file in preperation for import into
		# Google Sheets
		
		print("Reformating and merging %s and %s" % (invfile, sofile))
		# clean and reformat invoices.csv
		invdf = pd.read_csv(PATH + invfile)
		# create Product column from Item colum
		invdf['Product'] = [i[:i.find(' (')] for i in invdf.Item]
		# create OrderType column
		invdf['OrderType'] = 'Invoice'
		#reorder columns in invdf - removes unwanted columns
		columnOrder = ['Company','Salesperson','Product','Item',
		               'Quantity','Delivery Date','OrderType']
		invdf = invdf.reindex(columns=columnOrder)
		# Clean Sales Order data in prep for merging with invdf
		sodf = pd.read_csv(PATH + sofile)
		# Create list of orderType to be added to df
		sodf['OrderType'] = 'Sales Order'
		# Rename Delivery Due Date Column to Delivery Date
		sodf = sodf.rename(index=str, columns={'Delivery Due Date':
			                                   'Delivery Date'})
		# Update Product column from item name
		sodf['Product'] = [i[:i.find(' (')] for i in sodf.Item]
		# Merge sodof with invdf
		ordersdf = invdf.append(sodf, ignore_index=True)
		# Write ordersdf to csv
		ordersdf.to_csv(path_or_buf=PATH + 'ordersGS.csv')

		return


if __name__ == '__main__':
	reformat = DataReformat()
	PATH = '/home/lund/downloads/'

	reformat.fgoh_reformat(PATH)
	# reformat.orders_reformat(PATH)




