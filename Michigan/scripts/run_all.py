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
county_list = ["genesee", "ingham", "kalamazoo", "kent", "macomb", "oakland", "ottawa", "saginaw", "washtenaw", "wayne"]
for county in county_list:
    try:
        shutil.move("../data/" + county + ".txt", "../data/" + today + "/" + county + ".txt")
    except OSError:
        print(county + " is not available")
        pass
# move all the pdfs
pdf_list = ["kalamazoo-PDF", "kalamazoo-image", "oakland-PDF", "macomb-PDF", "wayne-PDF", "genesee-PDF"]
for folder in pdf_list:
    try:
        shutil.move("../data/" + folder, "../data/" + today + "/" + folder)
    except OSError:
        print(folder + " is not available")
        pass
