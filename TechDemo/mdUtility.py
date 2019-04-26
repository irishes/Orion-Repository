"""
File: mdUtility.py
Author: Chadd Frasier <cmf339@nau.edu>
Date: 2/24/19
Description:
        This file was writen for the purpose of extracting necessary metadata from isis3 headers and function returns.
    This file also houses the helper functions that the metadata needs in order to be prepared for use later. This file
    will also be home to all the isis3 command line interface functions for the various isis3 programs such as campt,
    catlab, isis2std, and catoriglab

    This file is for the Caption Writing Project for NAU sponsored by USGS
"""
from flask import Flask, render_template
from subprocess import CalledProcessError
import threading
import os

# Flask App Environment Configuration
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
IMAGE_FOLDER = os.path.join(APP_ROOT, 'static/images')
PVL_FOLDER = os.path.join(APP_ROOT, 'static/pvl')
CONFIG_FOLDER = os.path.join(APP_ROOT, 'static/config')
TPL_FOLDER = os.path.join(APP_ROOT, 'static/tpl')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONFIG_FOLDER'] = CONFIG_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['PVL_FOLDER'] = PVL_FOLDER
app.config['TPL_FOLDER'] = TPL_FOLDER


class DataObject(threading.Thread):
    """
    This is a class that houses all of the metadata objects and ISIS function interfaces. This is needed
    to allow for multiple users to log on and keep python dictionaries in order

    ...

    Attributes
    ----------
    isis3md_dict : dict
        This is the skeleton dictionary for the important isis3 metadata that will appear in the UI Tag Box

    filename : str
        The name of the cube file that will be used in this instance of the class

    tplFile : str
        This is the file name of the template file of the current instance of the class

    rawFileData: dict
        This is the dictionary that will be used to store all of the retrieved metadata from the cube file

    divDict: dict
        This is the dictionary that is passed back to the user interface and this dictionary is configured
        by the configuration file

    Methods:
    --------
        initDict: str
            initializes the tags in divDict in any instance its called

        camptInterface: str, str
            runs the console isis3 command campt and stored the return in the pvl file

        catlabInterface: str, str
            runs the console isis3 command catlab and stored the return in the pvl file

        catoriglabInterface
            runs the console isis3 command catoriglab and stored the return in the pvl file

        extractImage: str, str
                runs the console isis3 command isis2std and stored the return image as the specified format

        trimData: str
            popuates the divDict

        extractIsisKeyword: str, str
            runs the console isis3 command getkey and returns the result

        cleanDirs: str, str, str
            either erase/delete single or multiple files in a given directory

        removeNulls: dict
            replace empty data spots with a human readable value

        extractRawData: str
            extract all the data from a return file(pvl) and save into instance
    ----------
    """
    # configuration dictionary
    isis3md_dict = dict()

    # construct using a filename
    def __init__(self, filename, tplFile='Default.tpl', rawFileData=dict(), divDict=dict(image='')):
        """
        Parameters:
        -----------
                :param filename: str
                        this is the current cube file
                :param tplFile: str
                        this is the current template file (defaults to 'Default.tpl')
                :param rawFileData: dict
                        this is the raw file extraction dictionary that houses all the extracted metadata
                :param divDict: dict
                        this is the trimmed dictionary that is passed to the webpage
                        (defaults to dict('image') and reads 'config1.cnf')
                """
        self.filename = filename
        self.rawFileData = rawFileData
        self.divDict = divDict
        self.tplFile = tplFile

    def initDict(self, configFile='config1.cnf'):
        """
        initializes the divDict to the tags in the config file. (xml format)
        Parameters:
        -----------
            :param configFile: str
                file that contians the tags that are more important to have in the webpage
            :return:
            the new empty dictionary
        """
        file = open(os.path.join(app.config['CONFIG_FOLDER'], configFile), "r")
        for line in file:
            if '<tag>' in line:
                self.divDict[line.split('<tag>')[1].split("</tag>")[0]] = ''

        file.close()
        return self.divDict

    # run isis3 command campt on a given file and save data into a large combined text file
    def camptInterface(self, cube, returnFile):
        """
        runs the command line campt isis3 program
        Parameters:
        -----------
            :param cube: str
                the cube that will be passed to the function
            :param returnFile: str
                the file that the function returns to
        """
        try:
            os.system("campt from=" + os.path.join(app.config['UPLOAD_FOLDER'], cube)
                      + " to=" + os.path.join(app.config['PVL_FOLDER'], returnFile) + " append=True")
        except Exception as e:
            return "CAMPT FAILED: " + str(e)

    def catlabInterface(self, cube, returnFile):
        """
       runs the command line catlab isis3 program
       Parameters:
        -----------
            :param cube: str
                the cube that will be passed to the function
            :param returnFile: str
                the file that the function returns to
        """
        try:
            os.system("catlab from=" + os.path.join(app.config['UPLOAD_FOLDER'], cube)
                      + " to=" + os.path.join(app.config['PVL_FOLDER'], returnFile) + " append=True")
        except Exception as e:
            return "CATLAB FAILED: " + str(e)

    def catoriglabInterface(self, cube, returnFile):
        """
        runs the command line catoriglab isis3 command
        Parameters:
        -----------
            :param cube: str
                the cube that will be passed to the function
            :param returnFile: str
                the file that the function returns to
        """
        try:
            os.system("catoriglab from=" + os.path.join(app.config['UPLOAD_FOLDER'], cube)
                      + " to=" + os.path.join(app.config['PVL_FOLDER'], returnFile) + " append=True")
        except Exception as e:
            return "CATORIGLAB FAILED: " + str(e)

    def extractImage(self, cube, format='png'):
        """
        extracts the cube image into the specified format
        Parameters:
        -----------
            :param cube: str
                the cube that will be passed to the function
            :param format: str
                the file that the function returns to
            :return image: str
                the link to the image file that was created
        """
        image = str(cube).split("cub")[0] + format
        try:
            os.system("isis2std from=" + os.path.join(app.config['UPLOAD_FOLDER'], str(cube)) + " to="
                      + os.path.join(app.config['IMAGE_FOLDER'], image) + " format= " + format)

            self.divDict['image'] = image
        except Exception as e:
            print("IMAGE EXTRACTION FAILED: " + str(e))
        return

    def barScale(self, cube):
        """
        Returns Scale Bar to front end
        Parameters:
        ----------
            :param cube: str
                the cube that will be passed to the function
        
        """

        image = str(cube).split("cub")[0]
        try:
            os.system("barscale from=" + os.path.join(app.config['UPLOAD_FOLDER'], str(cube)) + " to=" + os.path.join(app.config['IMAGE_FOLDER'], image) + " padimage=True")
        except Exception as e:
            print("Something went wrong....")
        return

    def trimData(self, file):
        """
        populates the divDict for the instance
        Parameters:
        -----------
            :param file: str
                the file that contains the metadata
            :return: dict
                the new dictionary instance
        """
        mdfile = open(file, "r")
        for line in mdfile:
            if str(line).split('=')[0].strip(' ') in self.divDict.keys():
                self.divDict[str(line).split('=')[0].strip(' ')] = str(line).split('=')[1].strip(' ').strip("\n")
        mdfile.close()
        return self.divDict

    def extractIsisKeyword(self, cube, keyword):
        """
        calls the command line isis3 program getkey
        Parameters:
        -----------
            :param cube: str
                the cube to perform the search on
            :param keyword: str
                the keyword to search for
            :return: str
                the return from the call
        """
        try:

            return os.system("getkey from= " + os.path.join(app.config['UPLOAD_FOLDER'], str(cube))
                             + " keyword=" + str(keyword) + " recursive= True")
        except Exception as e:
            return 'GETKEY FAILED: ' + str(e)

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
    def cleanDirs(self, directory, code, file=''):
        """
        cleans up the directory depending on the code
        Parameters:
        -----------
            :param directory: str
                the directory to clean
            :param code: str
                the code of the action the function should preform
            :param file: str (optional)
                the file to search for if needed
            :return: 0 if success; render_template otherwise
        """
        # erase contents of any file given a directory and the filename
        try:
            if code == 'ers' and file != '':
                if file != '':
                    open(os.path.join(directory, file), "w").close()
                return 0
        except FileNotFoundError:
            return render_template("error.html")

    def removeNulls(self, dict):
        """
        replace nulls with none to allow for human readability
        Parameters:
        -----------
            :param dict: dict
                the dict to clean
            :return: dict
                the new divDict
        """
        for key in dict:
            if dict.get(key) != "":
                self.divDict[key] = dict[key]
            else:
                self.divDict[key] = str(None)

        return self.divDict

    # extract all raw data from cube file
    def extractRawData(self, pvlFile):
        """
        populate the rawFileData dict
        Parameters:
        -----------
            :param pvlFile: str
                the pvl file with the raw data from the isis functions
            :return: dict
                the raw dictonary
        """
        file = open(pvlFile, "r", encoding="utf-8")

        for line in file:
            line = line.strip().split('\n')[0]
            # print(line.strip().split("="))
            if len(line.split("=")) > 1 and '(' not in line.split('=')[1] and\
                    'Group' not in line.split("=")[0].strip() and 'Object' not in line.split("=")[0].strip():
                self.rawFileData[str(line.split("=")[0].strip())] = line.split("=")[-1].strip()

        file.close()
        return self.rawFileData

    def run_isis(self):
        command_return_file = "return.pvl"
        DataObject.cleanDirs(self, app.config['PVL_FOLDER'], "ers", command_return_file)

        try:
            # catlab os call to terminal and saves in return file
            DataObject.catlabInterface(self, self.filename, command_return_file)
        except Exception as e:
            print(str(e))

        try:
            # catoriglab os call to terminal and saves in return file
            DataObject.catoriglabInterface(self, self.filename, command_return_file)
        except Exception as e:
            print(str(e))

        try:
            # campt os call to terminal and saves in return file
            DataObject.camptInterface(self, self.filename, command_return_file)
        except Exception as e:
            print(str(e))

        try:
            # barscale os call to terminal and saves in return file
            DataObject.barScale(self, self.filename)
            print("Got this far")
        except Exception as e:
            print(str(e))
        return command_return_file
