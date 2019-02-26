"""
File: mdUtility.py
Author: Chadd Frasier <cmf339@nau.edu>
Date: 2/24/19
Description:
        This file was writen for the purpose of extracting necessary metadata from isis3 headers and function returns.
    This file also houses the helper functions that the metadata needs in order to be prepared for use later. This file
    will also be home to all the isis3 command line interface functions for the various isis3 programs such as campt,
    catlab, isis2std, and catoriglab

    This file is for the Caption Writing Project at USGS
"""
from flask import Flask, url_for
from subprocess import CalledProcessError
import os


# Flask App Environment
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
IMAGE_FOLDER = os.path.join(APP_ROOT, 'static/images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

isis3md_dict = {
    'TargetName': '',
    'SpacecraftName': '',
    'InstrumentId': '',
    'SCAN_CREATION_DATE': '',
    'SlantDistance': '',
    'SampleResolution': '',
    'NorthAzimuth': '',
    'Incidence': '',
    'Emission': '',
    'Phase': '',
    'SubSpacecraftGroundAzimuth': '',
    'SubSolarAzimuth': '',
    'SCAN_DENSITY_RANGE': '',
    'image': ''
    }




# run isis3 command campt on a given file and save data into a large combined text file
def camptInterface():
    return 0


# extract the image from a cube file to a specified format using isis2std() from the isis3 environment
# input -> cube file, format= png
# output -> name of image file that can be found in the static/images folder
def extractImage(cube, format='png'):
    image = str(cube).split("cub")[0] + format
    try:
        os.system("isis2std from=" + os.path.join(app.config['UPLOAD_FOLDER'], str(cube)) + " to="
                  + os.path.join(app.config['IMAGE_FOLDER'], image) + " format= " + format)
    except CalledProcessError:
        return CalledProcessError
    return image


# takes a large string of data and cuts the
# string down to only the needed metadata strings
# this is to help save data into a structure later
# input -> string data
# output -> less string data
def trimData(file):
    trimmed_dict = isis3md_dict
    mdfile = open(file, "r")
    for line in mdfile:
        if str(line).split('=')[0].strip(' ') in trimmed_dict.keys():
            trimmed_dict[str(line).split('=')[0].strip(' ')] = str(line).split('=')[1].strip(' ').strip("\n")

    mdfile.close()
    return trimmed_dict


# extract a specific isis3 keyword from the data
# input -> keyword string, file to search in
# returns value of the keyword if found
# throws KeyError otherwise
#
# (FUNCTION MUST BE CAUGHT)
def extractIsisKeyword():
    print("run stub function extractIsisKeyword")
    return 0


# will be called after the user hits restart or when some files are no longer needed
# flush working directories of unnecessary files for performance reasons
# function:
#     inputs-> directory string, code to tell the function what to do to the directory, and optional file variable
#
#     CLEAR all files ; code = clr and file == NULL
#     CLEAR all file of type file ; code= clr and file != NULL
#     DELETE file when code = del and file != NULL
#     ERASE contents of a file; code= ers file != NULL
#
def cleanDirs(directory, code, file=''):
    # erase contents of any file given a directory and the filename
    if code == 'ers' and file != '':
        if file != '':
            open(os.path.join(directory, file), "w").close()
        return 0
    return 1


# must use unique names for middle man files to stop form corruption with multiple clients
#  parse the isiscube data line by line for nlines writes lines to text and returns the name of the return file
def extractIsisData(file, nLines):
    # use a default middle man file
    returnFile = "return.txt"

    try:  # open/ create the file for writing
        returnFile = open(file=returnFile, mode="w+")
        # save the name of the file to return
        return_str = returnFile.name
    except FileNotFoundError:
        # catch the error for no file to avoid errors
        print("No file found creating file")

    # for each line in the input file
    for line in file:
        # write the line and decrement the line counter
        returnFile.writelines(str(line))
        nLines -= 1
        # if nLines = -1 we are done
        if nLines < 0:
            # close the file and return the filename
            returnFile.close()
            return return_str
