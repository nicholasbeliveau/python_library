import csv
import datetime

INPUT_FILE = "/home/nick/nypa_input.csv"
OUTPUT_FILE = "/home/nick/nypa_output.csv"
PAPER_EDITION_FILE = "/home/nick/python_library/SCS/nypa/paper_edition_codes.csv"

with open( OUTPUT_FILE, "w") as f:
  f.write("confirmationId,organizationId,organizationName,organizationContactName,organizationEmail,organizationPhone,category,newspaperNamePaper,newspaperNameEdition,groupName,noticeHeightInches,numberOfColumns,firstRunDate,noticeFilePath\n")

with open(INPUT_FILE, "rb") as inputcsv:
  input_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in inputcsv), delimiter=",")

  for row in input_reader:

    ## TODO add ad_type AGATE
    ## TODO do mapping for classification codes '0001'
    ## TODO add site code mapping to paper_edition_codes
    ## /u/ads/imports/eric_input/ put files for testing

    with open( OUTPUT_FILE, "a" ) as f:
      f.write(row["confirmationId"] + "," 
            + row["organizationId"] + ","
            + "\"" + row["organizationName"] + "\"" + ","
            + "\"" + row["organizationContactName"] + "\"" + ","
            + row["organizationEmail"] + ","
            + row["organizationPhone"] + ","
            + row["category"] + "," 
            + "1,"
            + "1,"
            + row["groupName"] + ","
            + row["noticeHeightInches"] + ","
            + row["numberOfColumns"] + ","
            + row["firstRunDate"][6:10] + row["firstRunDate"][0:2] + row["firstRunDate"][3:5] + ","
            + row["noticeFilePath"] + "\n" ) ## TODO cut this down to just the file name