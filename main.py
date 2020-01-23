from src import EkosSelenium
from src import renamefile
from src import datareformat
from src import GoogleAPI
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create file handler
fh = logging.FileHandler('AllocationTool/allocationtool.log') # PATH to file on local machine
fh.setLevel(logging.INFO)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add formatter to fh
fh.setFormatter(formatter)
# Add fh to logger
logger.addHandler(fh)

# Initialize classes
ekos = EkosSelenium.EkosSelenium()
rename = renamefile.RenameFile()
reformat = datareformat.DataReformat()
api = GoogleAPI.GoogleAPI()

# Define variables
username = 'USERNAME'
password = 'PASSWORD'
PATH = '/home/lund/downloads/'	# PATH on local machine
fgoh = 'Google Sheets - Finished Goods On-Hand'
inv = 'Google Sheets - Invoices - Package Type By Sales Rep'
so = 'Google Sheets - Sales Orders Product and Items'


# def main(username=username, password=password, PATH=PATH, 
# 	     fgoh=fgoh, inv=inv, so=so):
try:
	ekos.login(username, password)

	# fgoh download and rename
	fgohTime = ekos.download_report(fgoh)
	rename.rename_file('fgoh.csv', PATH)

	# Invoices download and rename
	invTime = ekos.download_report(inv)
	rename.rename_file('invoices.csv', PATH)

	# Sales Orders download and rename
	soTime = ekos.download_report(so)
	rename.rename_file('salesorders.csv', PATH)

	# Reformat Data
	reformat.fgoh_reformat(PATH)
	reformat.orders_reformat(PATH)

	# Import Data into Google Sheets
	api.import_data(PATH)

	ekos.quit()
except Exception as e:
	logger.error(e, exc_info=True)
	ekos.quit()
