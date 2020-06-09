import os
import glob
import shutil

# run all the scripts
for file in glob.iglob("*.py"):
    os.system("python3 " + file)

# Create a directory under data
today = "2020-6-9"
path = "../data/" + today
os.mkdir(path);

# move all the files under the directory
county_list = ["adams", "arapahoe", "boulder", "denver", "douglas", "el_paso" , "jefferson", "larimer", "pueblo", "weld"]
for county in county_list:
    try:
        shutil.move("../data/" + county + ".txt", "../data/" + today + "/" + county + ".txt")
    except OSError:
        print(county + " is not available")
        pass
