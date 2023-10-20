# Python functions to rename, relocate and get information out of .h5 files to create .json files
# Francesco D'Antonio 10/2023

# import section
import h5py
import xml.etree.ElementTree as ET
import json
import shutil
import os

def GEArchive_Filepath(Exam_filepath) :
    ''' GEnerates a list of filepaths ending in .h5 which iwll be used to generate .json files

    '''
    # generate file lise
    file_list = []

    for root, dir, files in os.walk(Exam_filepath):
        for file in files :
            if file.endswith('.h5') :
                file_list.append(os.path.join(root, file))

    return file_list



def GEArchive_h52json(h5File_dir,output_dir) :
    ''' Extracts information from .h5 GE file

    Uses that information to create a json file containing:
    - series description
    - date
    - exam number
    - series number
    - software used

    Copies the .h5 file to the directory 

    Filename convention: Series#_YYYYMMDD.h5 (or json)
    '''

    # Load the file from the directory provided
    h5_file = h5py.File(h5File_dir,'r')
    
    # Extract 'DownloadMetaData' doc and decode it from binary
    DownloadMetaData = h5_file['DownloadMetaData'][()][0].decode('latin-1')

    # Load it as a json file and extract the series description
    series_description = json.loads(DownloadMetaData).get("SeriesDescription")

    # Extract Header information (XML file)
    Header_xml = h5_file['Header.xml'][()]

    # Extract info out of Header
    root_header = ET.fromstring(Header_xml)
    date_element = root_header.find('.//date').text
    exam_element = root_header.find('.//ExamNumber').text
    series_element = root_header.find('.//SeriesNumber').text
    software_element = root_header.find('.//SoftwareLabel').text
    
    # Create a json file
    output_data = {
    "SeriesDescription": series_description,
    "Date": date_element,
    "ExamNumber": exam_element,
    "SeriesNumber": series_element,
    "Software": software_element
    }



    # if more the one .h5 file we need to rename the files appropriately
    # count how many files there are in the input directory
    file_count = len([f for f in os.listdir(os.path.dirname(h5File_dir))])

    # if we have more than 1 we change the naming convention to enumerate the file number at the end:
    # Scan#_YYYYMMDD_#
    if file_count > 1 :
        counter = 1
        output_file = f"{output_dir}/Series{series_element}_{date_element}_{counter}.json"
        
        # if there is a file by the same name, add 1 to the counter
        while os.path.exists(output_file):
            counter = counter + 1 
            output_file = f"{output_dir}/Series{series_element}_{date_element}_{counter}.json"
        
        # save the file
        with open(output_file, "w") as json_output_file:
            json.dump(output_data, json_output_file, indent=4)
        
        # copy the .h5 file with new name
        shutil.copy(h5File_dir, f"{output_dir}/Series{series_element}_{date_element}_{counter}.h5")

    # only 1 .h5 file in the directory
    else :
        output_file = f"{output_dir}/Series{series_element}_{date_element}.json"

        with open(output_file, "w") as json_output_file:
            json.dump(output_data, json_output_file, indent=4)

        shutil.copy(h5File_dir, f"{output_dir}/Series{series_element}_{date_element}.h5")

    return
    
    