import os
from shutil import copy2

output_path = "K:/vids to import/test1_scrambled/"

for folderpath, _, filenames in os.walk("K:/vids to import/test1"):
    filepaths = tuple([os.path.abspath(folderpath+"/"+filename) for filename in filenames]) # convert to absolute filepaths
    for filepath in filepaths:
        destination_filepath = output_path+os.path.basename(filepath)
        destination_filepath = destination_filepath.replace(" CRF0 PRESET0", "_DB")
        destination_filepath = destination_filepath.replace(" CRF0 PRESET3", "_DE")
        destination_filepath = destination_filepath.replace(" CRF0 PRESET6", "_DC")
        destination_filepath = destination_filepath.replace(" CRF0 PRESET9", "_DA")
        destination_filepath = destination_filepath.replace(" CRF0 PRESET12", "_DD")
        destination_filepath = destination_filepath.replace(" CRF10 PRESET0", "_GB")
        destination_filepath = destination_filepath.replace(" CRF10 PRESET3", "_GE")
        destination_filepath = destination_filepath.replace(" CRF10 PRESET6", "_GC")
        destination_filepath = destination_filepath.replace(" CRF10 PRESET9", "_GA")
        destination_filepath = destination_filepath.replace(" CRF10 PRESET12", "_GD")
        destination_filepath = destination_filepath.replace(" CRF20 PRESET0", "_FB")
        destination_filepath = destination_filepath.replace(" CRF20 PRESET3", "_FE")
        destination_filepath = destination_filepath.replace(" CRF20 PRESET6", "_FC")
        destination_filepath = destination_filepath.replace(" CRF20 PRESET9", "_FA")
        destination_filepath = destination_filepath.replace(" CRF20 PRESET12", "_FD")
        destination_filepath = destination_filepath.replace(" CRF30 PRESET0", "_AB")
        destination_filepath = destination_filepath.replace(" CRF30 PRESET3", "_AE")
        destination_filepath = destination_filepath.replace(" CRF30 PRESET6", "_AC")
        destination_filepath = destination_filepath.replace(" CRF30 PRESET9", "_AA")
        destination_filepath = destination_filepath.replace(" CRF30 PRESET12", "_AD")
        destination_filepath = destination_filepath.replace(" CRF40 PRESET0", "_CB")
        destination_filepath = destination_filepath.replace(" CRF40 PRESET3", "_CE")
        destination_filepath = destination_filepath.replace(" CRF40 PRESET6", "_CC")
        destination_filepath = destination_filepath.replace(" CRF40 PRESET9", "_CA")
        destination_filepath = destination_filepath.replace(" CRF40 PRESET12", "_CD")
        destination_filepath = destination_filepath.replace(" CRF50 PRESET0", "_EB")
        destination_filepath = destination_filepath.replace(" CRF50 PRESET3", "_EE")
        destination_filepath = destination_filepath.replace(" CRF50 PRESET6", "_EC")
        destination_filepath = destination_filepath.replace(" CRF50 PRESET9", "_EA")
        destination_filepath = destination_filepath.replace(" CRF50 PRESET12", "_ED")
        destination_filepath = destination_filepath.replace(" CRF60 PRESET0", "_BB")
        destination_filepath = destination_filepath.replace(" CRF60 PRESET3", "_BE")
        destination_filepath = destination_filepath.replace(" CRF60 PRESET6", "_BC")
        destination_filepath = destination_filepath.replace(" CRF60 PRESET9", "_BA")
        destination_filepath = destination_filepath.replace(" CRF60 PRESET12", "_BD")

        copy2(filepath, destination_filepath) # remove "_in_progress" once file is done being created
