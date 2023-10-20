# Python script to execute python functions to rename, relocate and extract .json information from .h5 files
# Francesco D'Antonio 10/2023
''' 
To run execute the following in the terminal

python GEh5_script.py <input directory> <output directory>

Example

python GEh5_script.py /usr/Archive/Closed/Exam2321 /usr/Scans2023-10-20
'''

# Import section
import sys
import GEh5_extraction_functions as GE


# Extract variables from terminal input
Exam_filepath = sys.argv[1]
output_dir = sys.argv[2]

# generate list of file names
file_list = GE.GEArchive_Filepath(Exam_filepath)

# from the list create .json files, rename and relocate .h5 files
for filepath in file_list:
    GE.GEArchive_h52json(filepath,output_dir)

