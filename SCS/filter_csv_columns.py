import csv

INPUT_FILE = "/home/nick/nypa_input.csv"
OUTPUT_FILE = "/home/nick/nypa_output.csv"

with open( OUTPUT_FILE, "w") as f:
  f.write("confirmationId,organizationId,organizationName,organizationContactName,organizationEmail,organizationPhone,category,newspaperName,groupName,noticeHeightInches,numberOfColumns,firstRunDate,noticeFilePath\n")

with open(INPUT_FILE, "rb") as inputcsv:
  input_reader = csv.DictReader((line.decode("iso8859-1").replace('\0','') for line in inputcsv), delimiter=",")

  for row in input_reader:
    with open( OUTPUT_FILE, "a" ) as f:
      f.write(row["confirmationId"] + "," 
            + row["organizationId"] + ","
            + "\"" + row["organizationName"] + "\"" + ","
            + "\"" + row["organizationContactName"] + "\"" + ","
            + row["organizationEmail"] + ","
            + row["organizationPhone"] + ","
            + row["category"] + "," 
            + row["newspaperName"] + "," 
            + row["groupName"] + ","
            + row["noticeHeightInches"] + ","
            + row["numberOfColumns"] + ","
            + row["firstRunDate"] + ","
            + row["noticeFilePath"] + "\n" )