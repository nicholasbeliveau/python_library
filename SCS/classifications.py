from __future__ import print_function
from datetime import datetime, timedelta
import mysql.connector, csv

cnx = mysql.connector.connect(user='admin', database='test_site', password='Test12345?')
cursor = cnx.cursor()
now = datetime.now()

add_classification = ("INSERT INTO categories "
                    "(categories_id, categories_image, parent_id, sort_order, date_added, last_modified, placead_disable, force_hold) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

add_classification_description = ("INSERT INTO categories_description "
                                  "(categories_id, language_id, categories_name) "
                                  "VALUES (%s, %s, %s)")

major_class_ids = []  # List of tuples (numeric_id, string_id)

def add_major_classes():
    print("Adding Major Classifications")

    with open('classifications.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line = 0
        class_id = 9112

        for row in reader:
            if line == 0:
                line += 1
            else:
                if row["CLASSIFICATION"] == "~~~~":
                    print( "Invalid clasification")
                else:
                    if row["PARENT"] == "~~~~":
                        if not row["CLASSIFICATION"].isnumeric():
                            classification = class_id
                            major_class_ids.append((class_id, row["CLASSIFICATION"]))
                            class_id += 1
                        else:
                            classification = row["CLASSIFICATION"]

                        data_classification = ( classification, '', 0, 0, now.strftime("%d/%m/%Y %H:%M:%S"), now.strftime("%d/%m/%Y %H:%M:%S"), '', '' )
                        data_classification_description = ( classification, '1', row["CLASSTITLE"].title() )

                        cursor.execute(add_classification, data_classification)
                        cursor.execute(add_classification_description, data_classification_description)

def add_sub_classes():
    print("Adding Minor Classifications")

    with open('classifications.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        line = 0

        for row in reader:
            if line == 0:
                line += 1
            else:
                if row["PARENT"] != "~~~~":
                    if row["PARENT"].isnumeric():
                        data_classification = ( row["CLASSIFICATION"], '', row["PARENT"], 0, now.strftime("%d/%m/%Y %H:%M:%S"), now.strftime("%d/%m/%Y %H:%M:%S"), '', '' )
                        data_classification_description = ( row["CLASSIFICATION"], '1', row["CLASSTITLE"].title() )

                        cursor.execute(add_classification, data_classification)
                        cursor.execute(add_classification_description, data_classification_description)
                    else:
                        for i in range(len(major_class_ids)):
                            if row["PARENT"] == major_class_ids[i][1]:
                                data_classification = ( row["CLASSIFICATION"], '', major_class_ids[i][0], 0, now.strftime("%d/%m/%Y %H:%M:%S"), now.strftime("%d/%m/%Y %H:%M:%S"), '', '' )
                                data_classification_description = ( row["CLASSIFICATION"], '1', row["CLASSTITLE"].title() )

                                cursor.execute(add_classification, data_classification)
                                cursor.execute(add_classification_description, data_classification_description)


add_major_classes()
add_sub_classes()

# Make sure data is committed to the database
cnx.commit()
cursor.close()
cnx.close()