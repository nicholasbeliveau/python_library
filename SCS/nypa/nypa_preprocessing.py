#!/usr/bin/env python3

import csv
import os
import sys
import pandas as pd
import re
import shutil
import subprocess

def get_run_date( file_name ):
  return "20" + file_name[10:12] + file_name[4:6] + file_name[7:9]

def handle_multipage_pdf(pdf_path, output_dir):
  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

  os.makedirs(output_dir, exist_ok=True)

  res = subprocess.run(["pdfinfo", pdf_path], stdout=subprocess.PIPE)

  info_text = res.stdout.decode("utf-8").replace("\n", " ")

  num_pages = int(re.sub(".*Pages:[^0-9]*", "", info_text).split(" ")[0])

  if num_pages > 1:
    output_pdf_pattern = output_dir + os.path.basename(pdf_path).replace(".pdf", "-%d.pdf")
    subprocess.run(["pdfseparate", pdf_path, output_pdf_pattern])

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
      run_date = get_run_date(os.path.basename(INPUT_FILE))

      if siteCode is not None and len(siteCode) > 0:
        xxx_ppee = f"{siteCode.upper()}_{paper.zfill(2)}{edition.zfill(2)}"
        pdf_path = "/u/pub_ads/" + xxx_ppee

        if xxx_ppee == "STR_0601":
          pdf_path += "/Photo_News/The_Chronicle"

        pdf_path += f"/{run_date[:4]}/{run_date[4:6]}-{run_date[6:8]}/Public_notice/"
        pdf_path += fileName
        
        output_dir = f"/u/data/{siteCode.upper()}/{siteCode.upper() + paper}/converted/{run_date[4:8]}/"

        handle_multipage_pdf(pdf_path, output_dir)

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
            + run_date + ","
            + os.path.splitext(fileName)[0] + ","
            + "Agate" 
            + "\n" )
      
output_location = os.environ.get( "OutputLocation" )

shutil.copy( OUTPUT_FILE, output_location )
