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
PVL_FOLDER = os.path.join(APP_ROOT, 'static/pvl')
TPL_FOLDER = os.path.join(APP_ROOT, 'static/tpl')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['PVL_FOLDER'] = PVL_FOLDER
app.config['TPL_FOLDER'] = TPL_FOLDER


isis3md_dict = dict(TargetName='', SpacecraftName='', InstrumentId='', PlanetocentricLatitude='', SCAN_CREATION_DATE='',
                    SlantDistance='', SampleResolution='', NorthAzimuth='', Incidence='', Emission='', Phase='',
                    SubSpacecraftGroundAzimuth='', SubSolarAzimuth='', image='')


# run isis3 command campt on a given file and save data into a large combined text file
def camptInterface(cube, returnFile):
    os.system("campt from=" + os.path.join(app.config['UPLOAD_FOLDER'], cube)
              + " to=" + os.path.join(app.config['PVL_FOLDER'], returnFile))


def catlabInterface(cube, returnFile):
    os.system("catlab from=" + os.path.join(app.config['UPLOAD_FOLDER'], cube)
              + " to=" + os.path.join(app.config['PVL_FOLDER'], returnFile))


def catoriglabInterface(cube, returnFile):
    os.system("catlab from=" + os.path.join(app.config['UPLOAD_FOLDER'], cube)
              + " to=" + os.path.join(app.config['PVL_FOLDER'], returnFile))


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
def extractIsisKeyword(cube, keyword):
    return os.system("getkey from= " + os.path.join(app.config['UPLOAD_FOLDER'], str(cube))
                     + " keyword=" + str(keyword) + " recursive= True")


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


def removeNulls(dict):
    returnDict = {}
    for key in dict:
        if dict.get(key) != "":
            returnDict[key] = dict[key]


    return returnDict
