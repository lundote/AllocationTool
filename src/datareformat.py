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
		# create list of product names from Item column
		product = []
		for i in range(0, len(invdf['Item'])):
			product.append(invdf['Item'].iloc[i][:invdf['Item'].iloc[i].find(' (')])
		# create list of order type to be added to df
		orderType = []
		for i in range(0, len(invdf['Item'])):
			orderType.append('Invoice')
		# convert product list and orderType list to pandas Series
		product = pd.Series(data=product)
		orderType = pd.Series(data=orderType)
		# add product and orderType series to df
		invdf = invdf.assign(Product=product)
		invdf = invdf.assign(OrderType=orderType)
		# remove packaging type from df - redundent
		invdf = invdf.drop(['Packaging Type'], axis=1)
		#reorder columns in invdf
		columnOrder = ['Company','Salesperson','Product','Item',
		               'Quantity','Delivery Date','OrderType']
		invdf = invdf.reindex(columns=columnOrder)

		# Clean Sales Order data in prep for merging with invdf
		sodf = pd.read_csv(PATH + sofile)
		# Create list of orderType to be added to df
		orderType = []
		for i in range(0, len(sodf)):
			orderType.append('Sales Order')
		# Convert orderType list to Pandas Series
		orderType = pd.Series(data=orderType)
		# Add orderType to sodf
		sodf = sodf.assign(OrderType=orderType)
		# Rename Delivery Due Date Column to Delivery Date
		sodf = sodf.rename(index=str, columns={'Delivery Due Date':
			                                   'Delivery Date'})
		# Update Product column from item name
		product = []
		for i in range(0, len(sodf['Item'])):
		    product.append(sodf['Item'].iloc[i][:sodf['Item'].iloc[i].find(' (')]) 
		sodf['Product'] = product

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




