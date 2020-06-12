import os
import glob
import shutil
import time

# run all the scripts
for file in glob.iglob("*.py"):
    if file != "run_all.py":
        os.system("python3 " + file)
    
# Create a directory under data
today = "2020-6-12"
path = "../data/" + today
os.mkdir(path);

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
pdf_list = ["boulder-PDF"]
for folder in pdf_list:
    try:
        shutil.move("../data/" + folder, "../data/" + today + "/" + folder)
    except OSError:
        print(folder + " is not available")
        pass
