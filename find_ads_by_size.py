#!/usr/bin/python3

import csv
import subprocess
import sys
import os
from datetime import datetime
from datetime import date

abspath = os.path.abspath(__file__)
dir = os.path.dirname(abspath)
os.chdir(dir)

AD_TEXT_FILE = "adtext.csv"
AD_HEADER_FILE = "adheader.csv"
ADMAX_DATA = "/u/abs/data/ads"
ADMAX_SCR = "/u/abs/exe/def"
OUTPUT_FILE = "bad_sizes.csv"
MIN_HEIGHT = 300
DATE_FORMAT = "%Y%m%d"
ad_dict = {}

with open(OUTPUT_FILE, "w") as f:
	f.write("ad_number,height,start_date,end_date\n")

for file in ["adtext", "adheader"]:
	subprocess.run(["/u/scs/tools/bin/unload", "/C0", f"{file}.csv={ADMAX_DATA}/{file},{ADMAX_SCR}/{file}"])
	
with open(AD_TEXT_FILE, "rb") as maincsv:
	ad_text_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in maincsv), delimiter=",")

	i = 0
	for row in ad_text_reader:

		if ( row["Height"] != '' and float( row["Height"] ) > MIN_HEIGHT ):
			ad_dict[row["AdNumber"]] = row

with open(AD_HEADER_FILE, "rb") as h:
	ad_header_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in h), delimiter=",")

	for header_row in ad_header_reader:
		if( ad_dict.get(header_row["AdNumber"]) and datetime.strptime(header_row["EndDate"], DATE_FORMAT) > datetime.now() and header_row["EndDate"] != '29991231'):

			ad = ad_dict.get(header_row["AdNumber"])
			with open(OUTPUT_FILE, "a") as f:
				i += 1
				f.write( ad["AdNumber"] + "," + ad["Height"] + "," + header_row["StartDate"] + "," + header_row["EndDate"] + "\n")

print( "Number of ads : " + str(i) )

## Remove database csv file.  It could be a large file and we don't need to keep it around
os.system('rm ' + AD_TEXT_FILE)
os.system('rm ' + AD_HEADER_FILE)