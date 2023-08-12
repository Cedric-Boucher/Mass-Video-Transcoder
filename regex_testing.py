import re
import os

p = re.compile(".*\\.py$") # all files that end in ".py"

for folderpath, _, filenames in os.walk("C:/Users/onebi/Documents/GitHub/Mass-Video-Transcoder"):
    filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames])
    for filepath in filepaths:
        match = p.match(filepath)
        if match:
            print(filepath)
