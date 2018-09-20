from datetime import datetime, date
from pytz import timezone
import os
import sys

class RenameFile:
	'''Class for renaming files downloaded from Ekos in preperation for
	reformatting data using pandas and then importing data into Google
	Sheets'''

	def dtround(self, datetime):
		'''Rounds seconds of datetime object up if microseconds > 500000
		else returns datetime object'''
		print("Rounding %s" % str(datetime))
		if datetime.microsecond > 500000 and datetime.second == 59:
			datetime = datetime.replace(minute = datetime.minute + 1, 
				second = 0)
		elif datetime.microsecond > 500000:
			datetime = datetime.replace(second = datetime.second + 1)
		return datetime

	def tzconv(self, datetime):
		'''Takes datetime object, sets timezone as Pacific Time
		and the convents timezone to Eastern Time. Necessary because
		Ekos export names incorporate time of download in Eastern Time.
		DST = Daylight Savings Time'''
		print("Adjusting Timezones")
		datetime = timezone('UTC').localize(datetime)
		datetime = datetime.astimezone(timezone('US/Eastern'))
		return datetime

	def rename_file(self, datetime, new_filename, PATH):
		'''takes given datetime and uses it to create a string that
		matches the filename of recently downloaded ekos export. Then
		searches PATH directory for the desired file and renames file
		to new filename provided by user '''
		filename = 'Export_%s_.csv' % datetime.strftime("%m%d%Y%I%M%S")
	        count = 0
         	while os.path.isfile(PATH + filename) is False:
			try:
                                datetime = datetime.replace(second = datetime.second + 1)
				count = count + 1
				#	print datetime
				filename = 'Export_%s_.csv' % datetime.strftime("%m%d%Y%I%M%S")
				#	print filename
				if count == 59:
					sys.exit() # Acts as failsafe to avoid infinite loop
			except ValueError:
				print('ValueError: resetting seconds to 0')
				datetime = datetime.replace(second = 0)
				count = 0
			except SystemExit:
				print('Exiting program due to infinite loop')
		os.rename(PATH + filename, PATH + new_filename)
		return


if __name__ == '__main__':
	datetime = datetime(2018, 6, 3, 13, 5, 11, 76583)
	PATH = '/home/lund/downloads/'

	rename = RenameFile()

	print datetime
	datetime = rename.dtround(datetime)
	print datetime
	datetime = rename.tzconv(datetime)
	print datetime
	rename.rename_file(datetime, 'fgoh.csv', PATH)
	
