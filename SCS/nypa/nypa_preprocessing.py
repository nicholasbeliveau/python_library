#!/usr/bin/env python3

import csv
import os
import sys
import pandas as pd
import shutil

def get_run_date( file_name ):
  return "20" + file_name[10:12] + file_name[4:6] + file_name[7:9]

if len(sys.argv) > 1:
  INPUT_FILE = sys.argv[1]
else:
  print( "No file passed" )
  sys.exit()

##TODO Add check for number of columns and only chop if 
## Remove Duplicate Column Headings by number
data = pd.read_csv(INPUT_FILE)
data2 = data.drop( data.columns[120], axis=1 )
data2 = data.drop( data.columns[125], axis=1 )
data2.to_csv('temp.csv', sep=',')

OUTPUT_FILE = "nypa_output_" + get_run_date( os.path.basename( INPUT_FILE ) ) + ".csv"
PAPER_EDITION_FILE = "site_mappings.csv"
CATEGORY_FILE = "category_mapping.csv"

with open( OUTPUT_FILE, "w") as f:
  f.write("confirmationId,organizationId,organizationName,organizationContactName,organizationEmail,organizationPhone,category,newspaperNamePaper,newspaperNameEdition,groupName,noticeHeightInches,numberOfColumns,firstRunDate,noticeFilePath,adType\n")

with open("temp.csv", "rb") as inputcsv:
  input_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in inputcsv), delimiter=",")

  for row in input_reader:
    ## /u/ads/imports/eric_input/ put files for testing

    with open( CATEGORY_FILE, "rb" ) as categorycsv:
      classCode = ""

      category_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in categorycsv), delimiter=",")
      for cateogry_row in category_reader:
        if ( cateogry_row["nypaCategoryName"] == row["category"] ):
          classCode = cateogry_row["classCode"]

    with open( PAPER_EDITION_FILE, "rb" ) as paperEditioncsv:
      siteCode = ""
      paper = ""
      edition = ""

      paper_edition_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in paperEditioncsv), delimiter=",")
      for paper_edition_row in paper_edition_reader:
        ##if ( paper_edition_row["site_name"].strip() == row["groupName"].strip() ):
        if ( paper_edition_row["site_name"].strip() == row["newspaperGroupName"].strip() ):
          siteCode = paper_edition_row["site_code"]

        if ( paper_edition_row["paper_name"].strip() == row["newspaperName"].strip() ):
          paper = paper_edition_row["paper_id"]
          edition = paper_edition_row["edition_id"]

      if ( siteCode == "" ):
        print( row["confirmationId"] + " " + row["groupName"] + " site code not mapped correctly" )

      if ( paper == "" or edition == "" ):
        print( "." + row["newspaperName"] + "." + " paper not mapped correctly" )

      fileName = os.path.basename(row["noticeFilePath"])

    with open( OUTPUT_FILE, "a" ) as f:
      f.write(row["confirmationId"] + "," 
            + row["organizationId"] + ","
            + "\"" + row["organizationName"] + "\"" + ","
            + "\"" + row["organizationContactName"] + "\"" + ","
            + row["organizationEmail"] + ","
            + row["organizationPhone"] + ","
            + classCode + "," 
            + paper + ","
            + edition + ","
            + siteCode + ","
            + row["noticeHeightInches"] + ","
            + row["numberOfColumns"] + ","
            + get_run_date( os.path.basename ( INPUT_FILE ) ) + ","
            + os.path.splitext(fileName)[0] + ","
            + "Agate" 
            + "\n" )
      
output_location = os.environ.get( "OutputLocation" )

shutil.copy( OUTPUT_FILE, "/home/nick/" )

os.remove("temp.csv")