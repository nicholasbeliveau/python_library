import csv
import os

INPUT_FILE = "/home/nick/nypa_input.csv"
OUTPUT_FILE = "/home/nick/nypa_output.csv"
PAPER_EDITION_FILE = "paper_edition_codes.csv"
CATEGORY_FILE = "category_mapping.csv"

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
        if ( paper_edition_row["newspaperName"] == row["groupName"] ):
          siteCode = paper_edition_row["siteCode"]
          paper = paper_edition_row["paperID"]
          edition = paper_edition_row["editionID"]

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
            + row["firstRunDate"][6:10] + row["firstRunDate"][0:2] + row["firstRunDate"][3:5] + ","
            + os.path.basename(row["noticeFilePath"]) + ","
            + "AGATE" 
            + "\n" )