#!/usr/bin/python3
import subprocess
import os

ADMAX_DATA = "/u/abs/data/ads"
ADMAX_SCR = "/u/abs/exe/def"

def dumpAdmaxTable( tableName ):

    if ( type(tableName) == str):
        subprocess.run(["/u/scs/tools/bin/unload", "/C0", f"{tableName}.csv={ADMAX_DATA}/{tableName},{ADMAX_SCR}/{tableName}"])
    elif ( type(tableName) == list ):
        for file in tableName:
            subprocess.run(["/u/scs/tools/bin/unload", "/C0", f"{file}.csv={ADMAX_DATA}/{file},{ADMAX_SCR}/{file}"])
    else:
        print("Invalid tableName")

def cleanupAdmaxTable( tableName ):
    if (type(tableName) == str):
        os.system('rm ' + tableName + ".csv")
    elif (type(tableName) == list):
        for file in tableName:
            os.system('rm ' + file + ".csv")
    else:
        print("Invalid table name")
    
