from src import EkosSelenium
from src import renamefile
from src import datareformat
from src import GoogleAPI

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
ekos.login(username, password)

# fgoh download and rename
fgohTime = ekos.download_report(fgoh)
fgohTime = rename.dtround(fgohTime)
fgohTime = rename.tzconv(fgohTime)
rename.rename_file(fgohTime, 'fgoh.csv', PATH)

# Invoices download and rename
invTime = ekos.download_report(inv)
invTime = rename.dtround(invTime)
invTime = rename.tzconv(invTime)
rename.rename_file(invTime, 'invoices.csv', PATH)

# Sales Orders download and rename
soTime = ekos.download_report(so)
soTime = rename.dtround(soTime)
soTime = rename.tzconv(soTime)
rename.rename_file(soTime, 'salesorders.csv', PATH)

# Reformat Data
reformat.fgoh_reformat(PATH)
reformat.orders_reformat(PATH)

# Import Data into Google Sheets
api.import_data(PATH)

ekos.quit()
