#!/usr/bin/python3

import csv
import subprocess
import sys
import os

abspath = os.path.abspath(__file__)
dir = os.path.dirname(abspath)
os.chdir(dir)

INPUT_FILE = "adtext.csv"
ADMAX_DATA = "/u/abs/data/ads"
ADMAX_SCR = "/u/abs/exe/def"
OUTPUT_FILE = "bad_sizes.csv"
MIN_HEIGHT = 300

with open(OUTPUT_FILE, "w") as f:
	f.write("ad_number,height\n")

# Unload alias, customer, and contacts files
for file in ["adtext"]:
	subprocess.run(["/u/scs/tools/bin/unload", "/C0", f"{file}.csv={ADMAX_DATA}/{file},{ADMAX_SCR}/{file}"])
	
print( INPUT_FILE )
with open(INPUT_FILE, "rb") as maincsv:
	reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in maincsv), delimiter=",")

	i = 1
	for row in reader:
		i += 1
			
		if ( row["Height"] != '' and float( row["Height"] ) > MIN_HEIGHT ):
			with open(OUTPUT_FILE, "a") as f:
				f.write(row["AdNumber"] + "," + row["Height"] + "\n")

## Remove database csv file.  It could be a large file and we don't need to keep it around
os.system('rm ' + INPUT_FILE)