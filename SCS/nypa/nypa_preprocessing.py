import csv
import os

INPUT_FILE = "ads_12.10.24.csv"
OUTPUT_FILE = "nypa_output_20241210.csv"
PAPER_EDITION_FILE = "site_mapping.csv"
CATEGORY_FILE = "category_mapping.csv"

def get_run_date( date ):
  return "20" + date[10:12] + date[4:6] + date[7:9]

with open( OUTPUT_FILE, "w") as f:
  f.write("confirmationId,organizationId,organizationName,organizationContactName,organizationEmail,organizationPhone,category,newspaperNamePaper,newspaperNameEdition,groupName,noticeHeightInches,numberOfColumns,firstRunDate,noticeFilePath,adType\n")

with open(INPUT_FILE, "rb") as inputcsv:
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
        if ( paper_edition_row["site_name"].strip() == row["groupName"].strip() ):
          siteCode = paper_edition_row["site_code"]

        if ( paper_edition_row["paper_name"].strip() == row["newspaperName"].strip() ):
          paper = paper_edition_row["paper_id"]
          edition = paper_edition_row["edition_id"]

      if ( siteCode == "" ):
        print( row["confirmationId"] + " " + row["groupName"] + " site code not mapped correctly" )

      if ( paper == "" or edition == "" ):
        print( "." + row["newspaperName"] + "." + " paper not mapped correctly" )

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
            + get_run_date( INPUT_FILE ) + ","
            + os.path.basename(row["noticeFilePath"]) + ","
            + "Agate" 
            + "\n" )