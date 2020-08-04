import os
fileDir = os.path.dirname(__file__)
filePath = os.path.join(fileDir, "../data/rapides.txt")
filePath = os.path.abspath(os.path.realpath(filePath))
f = open(filePath, 'w')

f.write("Could not find any relevant information.")

f.close()

print("finished")