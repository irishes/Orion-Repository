"""
File: mdUtility.py
Author: Chadd Frasier <cmf339@nau.edu>
Created Date: 2/24/19
Most Recent Update: 3/30/2019
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


class DataObject():
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

        extractRawData2: str
        version 2: modeled off the previous method, this more successfully captures the list data in the pvl file
            extract all the data from a return file(pvl) and save into instance
    ----------
    """
    # class configuration dictionary: blank
    isis3md_dict = dict()

    # construct using a filename
    def __init__(self, filename, tplFile='Default.tpl'):
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
        self.rawFileData = dict()
        self.divDict = dict(image='')
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
                self.divDict[line.strip().strip('<tag>').strip('</tag>')] = ''

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
            if str(line).split('=')[0].strip() in self.divDict.keys():
                self.divDict[str(line).split('=')[0].strip()] = str(line).split('=')[1].strip().strip("\n")
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

    def cleanData(self, dict):
        """
        creates the div Dict by replace nulls and bad data with, replace nulls with none to allow for human readability
        Parameters:
        -----------
            :param dict: dict
                the dict to clean
            :return: dict
                the new divDict
        """
        # erases nulls
        for key in dict:
            if dict.get(key) != "":
                self.divDict[key] = dict[key]
            else:
                self.divDict[key] = str(None)

            self.divDict[key] = dict[key]
        return self.divDict

    def run_isis(self):
        """
        runs the isis command in a desired order
        :return: return file as str
        """
        command_return_file = "return.pvl"
        cleanDirs(app.config['PVL_FOLDER'], "ers", command_return_file)

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
        return command_return_file

    def cleanRawDict(self, dict):
        """
        clean the dictionary of unwanted symbols
        :param dict:
            the raw file dictionary
        :return: dict
            the new cleaned dict

        """
        # create a temp dictionary
        tempdict = {}
        undesired = list(["'", '^'])
        for key in dict:
            # if content is a list
            if '[' == dict[key][0]:
                valstring = dict[key]
                valstring = valstring.strip("(").strip(")")
                listVals = valstring.split(",")

                for index in range(0, len(listVals)):
                    for char in undesired:
                        listVals[index] = listVals[index].strip(char)

                tempdict[key] = listVals
            # if embedded lists
            elif '((' in dict[key]:
                templist = dict[key].strip("'").split('),')

                for index in range(0, len(templist)):
                    # last format stage
                    templist[index] = templist[index].strip().strip('(').strip(')')
                    # create tuple of integers
                    templist[index] = (int(templist[index].split(',')[0].strip()),
                                       int(templist[index].split(',')[1].strip()))

                tempdict[key] = templist
                # print(templist)

            elif '(' == dict[key][0] and dict[key][-1] == ')':
                tempdict[key] = dict[key].strip('(').strip(')').strip()
                fixedlist = tempdict[key].split(",")

                for index in range(0, len(fixedlist)):
                    fixedlist[index] = fixedlist[index].strip().strip("'")
                tempdict[key] = list(fixedlist)
            else:
                for char in undesired:
                    tempdict[key] = dict[key].strip(char)

        return tempdict

    def extractRawData2(self, pvlFile):
        """
                populate the rawFileData dict
                Parameters:
                -----------
                    :param pvlFile: str
                        the pvl file with the raw data from the isis functions
                    :return: dict
                        the raw dictonary
                """
        # tags that will serve as keys in the dict
        genisis = ''
        objecttag = ''
        grouptag = ''
        nametag = ''

        # open the pvl for reading
        file = open(pvlFile, "r", encoding="utf-8")

        # flag for mini list and string
        isList = False
        isString = False

        stringValue = ''
        for line in file:

            # skip empty lines
            if line == '\n':
                # print('--empty line--')
                continue
            # skip any comments
            elif '/*' in line:
                continue
            elif len(line) > 15 and '=' not in line and 'Object' not in line and 'Group' not in line \
                    and not isList and not isString:
                # print(unqkey)
                # print(stringValue)
                self.rawFileData[unqkey] = self.rawFileData[unqkey] + line.strip()
                continue

            try:

                # The rest of this block Checks and captures all the needed tags before any further parsing
                # is done, when end tags are seen it also will appropriately erase the tags that are no longer valid
                if 'Object = IsisCube' in line:
                    genisis = line.split("=")[1].strip()
                    #print(genisis)
                    continue
                elif 'Object =' in line:
                    objecttag = line.split("=")[1].strip()
                    #print(objecttag)
                    continue
                elif 'End_Object' in line:
                    objecttag = ''
                    grouptag = ''
                    nametag = ''
                    continue
                elif 'Group =' in line:
                    grouptag = line.split("=")[1].strip()
                    #print(grouptag)
                    continue
                elif 'End_Group' in line:
                    grouptag = ''
                    nametag = ''
                    continue
                elif 'Name' in line.strip()[0:7] or 'NAME' in line.strip()[0:7]:
                    nametag = line.split("=")[1].strip()
                    #print(nametag)
            except Exception as e:
                # catch errors and show
                print('Error Extracting Key: ' + str(e))

            try:
                # if the line has = and the loop is not currently in a list or string
                if '=' in line and not isString and not isList:

                    # get the key of the line
                    listkey = line.split('=')[0].strip()

                    # create the unique key for the dictionary in a function
                    unqkey = combineKeys(genisis, objecttag, grouptag, nametag, listkey)

                    # capture the right side of the =
                    if len(line.split('=')) > 2:
                        stringValue = line.split('=')[1].strip() + ' = ' + line.split('=')[2].strip()
                    else:
                        stringValue = line.split('=')[1].strip()

                    # check to see if it is the start of a list or string and mark the appropriate flag
                    if '"' == stringValue[0] and stringValue[-1] != '"':
                        isString = True
                        continue
                    elif '(' == stringValue[0] and stringValue[-1] != ')':
                        isList = True
                        continue
                    else:
                        # otherwise just set it equal directly
                        self.rawFileData[unqkey] = stringValue
            except Exception as e:
                # catch error and display
                print('Error Extracting Key: ' + str(e))

            # if isString True
            if isString:
                # if the other close quote is the last element of the list then it is over
                if '"' == line.strip()[-1]:
                    # append the last part
                    stringValue = stringValue + ' ' + line.strip()
                    # break the condition
                    isString = False
                    # set the key data to the final value
                    self.rawFileData[unqkey] = stringValue
                    continue
                elif not isList:
                    # append the string and continue looping
                    stringValue = stringValue + ' ' + line.strip()
                    continue
            # using same idea as a string but not formatted
            # Important: Needs to be cleaned later
            elif isList:
                if ')' == line.strip()[-1] or '>' == line.strip()[-1]:
                    stringValue = stringValue + line.strip()
                    isList = False
                    self.rawFileData[unqkey] = stringValue
                    continue
                elif not isString:
                    stringValue = stringValue + line.strip()
                    continue

        return self.rawFileData

# END OF CLASS

# TODO: Finish this function
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
        if'.py' in file:
            print('CANNOT MANIPULATE SCRIPT FILES')
            return 1
        elif code == 'ers' and file != '':
            if file != '':
                open(os.path.join(directory, file), "w").close()
            return 0
        elif code == 'del' and file != '':
            # print(os.path.join(directory, file))
            if file == os.getcwd():
                os.system('rm ' + file)
                return 0
            else:
                os.system('rm ' + os.path.join(directory, file))
                return 0

# non class related function
def combineKeys(genisis, objecttag, grouptag, nametag, listkey):
    # TODO: default to isiscube for genisis or set and SDFU_LABEL? *ASK DR.KESTAY*
    """
           combines and creates the unique tag given a the different tags as input.
           Note:
                I know that I am erasing the tags when they are not included so that is why I can check for a '' string
           Parameters:
           -----------
                :param: genisis
                    the generic isiscube tag
                :param: objecttag
                    the object tag from the pvl
                :param: grouptag
                    the group tag found in the pvl
                :param: nametag
                    the name tag found in the pvl
                :param: listkey
                    the key of the dict tag


               :return: str
                   the unique key for anything in a isiscube
           """

    # sanitize all the input variables
    genisis = cleanString(genisis)
    objecttag = cleanString(objecttag)
    grouptag = cleanString(grouptag)
    nametag = cleanString(nametag)
    listkey = cleanString(listkey)

    #everything tag
    if objecttag != '' and grouptag != '' and nametag != '':
        return objecttag + '.' + grouptag + '.' + nametag + '.' + listkey
    # only name tag
    elif objecttag == '' and grouptag != '' and nametag != '':
        return grouptag + '.' + nametag + '.' + listkey
    # only group
    elif objecttag == '' and grouptag != '' and nametag == '':
        return grouptag + '.' + listkey
    # only object tag
    elif objecttag != '' and grouptag == '' and nametag == '':
        return objecttag + '.' + listkey
    # object and name
    elif objecttag != '' and grouptag == '' and nametag != '':
        return objecttag + '.' + nametag + '.' + listkey
    # object and group tags exist
    elif objecttag != '' and grouptag != '' and nametag == '':
        return objecttag + '.' + grouptag + '.' + listkey
    # group and name tags exist
    elif objecttag == '' and grouptag != '' and nametag != '':
        return grouptag + '.' + nametag + '.' + listkey
    else:
        # no tags
        return genisis + '.' + listkey


def cleanString(string):
    """
    This function takes a string input and strips off all the characters that we deem unwanted
    :param: str
        string that will be striped of all undesired characters
    :return:
        the striped string
    """
    undesired = list(['^', '"', ' '])
    for char in undesired:
        if char in string:
            if char == ' ':
                string = string.replace(char, '_')
            else:
                string = string.strip(char)
    return string.strip()

