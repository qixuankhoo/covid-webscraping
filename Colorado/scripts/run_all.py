#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import os
import glob
import shutil
import time
from datetime import date

# run all the scripts
for file in glob.iglob("*.py"):
    if file != "run_all.py":
        os.system("python3 " + file)
    
# Create a directory under data
today = str(date.today())
path = "../data/" + today
os.mkdir(path)

# move all the files under the directory
time.sleep(20)
county_list = ["adams", "arapahoe", "boulder", "denver", "douglas", "el_paso" , "jefferson", "larimer", "pueblo", "weld"]
for county in county_list:
    try:
        shutil.move("../data/" + county + ".txt", "../data/" + today + "/" + county + ".txt")
    except OSError:
        print(county + " is not available")
        pass
# move all the pdfs
pdf_list = ["boulder-PDF", "brockton-PDF", "tri-county-PDF", "weld-PDF", "larimer-PDF", "el_paso-PDF", "jefferson-PDF", "douglas-PDF", "denver-PDF"]
for folder in pdf_list:
    try:
        shutil.move("../data/" + folder, "../data/" + today + "/" + folder)
    except OSError:
        print(folder + " is not available")
        pass
