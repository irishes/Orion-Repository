#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, Response, send_file
from mdUtility import DataObject, cleanDirs
import os
import ast
from werkzeug.utils import secure_filename


# Flask App Environment
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
IMAGE_FOLDER = os.path.join(APP_ROOT, 'static/images')
PVL_FOLDER = os.path.join(APP_ROOT, 'static/pvl')
TPL_FOLDER = os.path.join(APP_ROOT, 'static/tpl')
CONFIG_FOLDER = os.path.join(APP_ROOT, 'static/config')

app = Flask(__name__)
app.secret_key = b'_5#7ey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONFIG_FOLDER'] = CONFIG_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['PVL_FOLDER'] = PVL_FOLDER
app.config['TPL_FOLDER'] = TPL_FOLDER


# index.html
@app.route("/", methods=["GET"])
def index():
    status = cleanDirs(app.config['PVL_FOLDER'],'ers', 'return.pvl')
    print(status)
    # print(os.path.join(os.getcwd(),'print.prt'))
    loadingGif = url_for('static', filename='images/loading.gif')
    return render_template('index.html', LOADINGGIF=loadingGif)


# upload and save process
@app.route("/upload", methods=['GET', 'POST'])
def upload():

    # if request is post
    if request.method == 'POST':
        # Make File Post an Instance of a DataObject and extract all the tags from that data
        # =============================================================================
        try:
            # grab the file post using request lib
            cubeFile = request.files['uploadFile']

        except KeyError:
            # catches NULL error and makes user try again
            # TODO: better UI for when a user fails to complete this.
            #  exp: a popup message
            print("Null File Error: please enter a .cub file ")
            return render_template("index.html")
        try:
            # try to capture template and create instance using constructor
            tplFile = request.files['templateFile']
            current_instance = DataObject(cubeFile.filename, tplFile.filename)
            # captures the important tags from config
            current_instance.divDict = DataObject.initDict(current_instance)
            print("div dict after init" + str(current_instance.divDict))

        except KeyError:
            # if this fails because of a null value it will use the default construction
            current_instance = DataObject(cubeFile.filename)
            # captures the important tags from config
            current_instance.divDict = DataObject.initDict(current_instance)
            print("div dict after init" + str(current_instance.divDict))



        if (current_instance.tplFile.split('.')[-1] == 'tpl' and current_instance.tplFile != '') \
                and (current_instance.filename.split('.')[-1] == 'cub' and current_instance.filename != ''):
            # save the file to the upload directory
            cubeFile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(current_instance.filename)))
            if current_instance.tplFile != 'Default.tpl':
                # save the file to the upload directory
                tplFile.save(os.path.join(app.config['TPL_FOLDER'], secure_filename(current_instance.tplFile)))

            # this try except allows us to run a console command and catch and displays errors to prevent crashes
            try:

                # this line is calling a string shell command by creating the command string on a single line
                DataObject.extractImage(current_instance, current_instance.filename)

                # run the data collection in parent
                command_file_output = DataObject.run_isis(current_instance)
            except Exception as e:
                print('Threading Section Critical Failure:' + str(e))
                if current_instance:
                    del current_instance
                return render_template("index.html")

            try:
                # run data collection algorithm on the returned ISIS3 PVL file
                current_instance.rawFileData = DataObject.extractRawData2(
                    current_instance, os.path.join(app.config['PVL_FOLDER'], str(command_file_output))
                )

                # clean the raw dictionary which includes complex structures
                current_instance.rawFileData = DataObject.cleanRawDict(current_instance, current_instance.rawFileData)
                print('CLEANED DICTIONARY: ' + str(current_instance.rawFileData))

                # read in the desired template file
                templateFile = open(os.path.join(app.config['TPL_FOLDER'], current_instance.tplFile), "r")
                templateString = templateFile.read()
                templateFile.close()

                # save file location for web page use later
                full_filename = url_for('static', filename='images/' + current_instance.divDict['image'])

                # parse file and fill important tag dict
                current_instance.divDict = DataObject.trimData(
                    current_instance, os.path.join(app.config['PVL_FOLDER'], str(command_file_output))
                )
                # save the image location in the dict for access
                # TODO: possible rethink on this idea of keeping the location
                current_instance.divDict['image'] = full_filename

                # clean the div dict of all unwanted symbols
                # Function: cleanData
                current_instance.divDict = DataObject.cleanData(current_instance, current_instance.divDict)

                print('DivDict: ' + str(current_instance.divDict))

                # delete unneeded files
                try:
                    cleanDirs(os.getcwd(), 'del', 'print.prt')
                except Exception as e:
                    print('Error Deleteing Files' + str(e))

                dictstring = str(current_instance.divDict)

                print("Dict string being passed is : "+dictstring)
                temparea = str(templateString)
                img = current_instance.divDict['image']
                csvDownload = current_instance.rawFileData

                csvstring = ""
                for tempKey, tempVal in current_instance.rawFileData.items():
                    csvstring = csvstring + str(tempKey) + ":" + str(tempVal) + "@@@"
                csvstring = csvstring[:-3]

                del current_instance
                # pass all necessary data to the front end
                return render_template("output.html", DICTSTRING=dictstring, TEMPAREA=temparea,
                                       IMG=img, CSVSTRING=csvstring, CSVDOWNLOAD = csvDownload)
            # catch file not found error when looking for the returned data file
            except FileNotFoundError:
                print("ISIS3 command failed to create a pvl")
                return render_template("error.html")
        else:
            # fatal error
            print("Fatal Error: This is Probably a Coding Problem!!")
            return render_template("index.html")



# display the image page
@app.route('/showImage', methods=['POST'])
def showImage():
    # if POST
    if request.method == 'POST':
        # recieve the image from the web page to keep users from colliding
        image = request.form.get('image_present')
        meta = request.form.get('image_string')
        # render that image from the server
        return render_template("imageDisplay.html", IMG=image, DICTSTRING = meta)


# download the raw data as a csv
@app.route('/getCSV', methods=['GET', 'POST'])
def getCSV():
    if request.method == 'POST':

        csvString = request.form.get('passedTXT')
        new_str = ""
        csvString = ast.literal_eval(csvString)

        # create the new string of data as a csv
        for key, value in csvString.items():
            new_str = new_str + str(key) + "," + str(value) + "\n"
        # use Response to send the whole string as a csv file
        return Response(
            new_str,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=exportISIS.csv"})


# download the image file as a png
# TODO: download different file types using isis3
@app.route('/getImage', methods=['GET', 'POST'])
def getImage():
    if request.method == 'POST':
        imagepath = os.path.join(app.config['IMAGE_FOLDER'], str(request.form.get('passedIMG')).split("/")[-1])

        try:
            return send_file(imagepath,
                             mimetype='application/octet-stream',
                             as_attachment=True,
                             attachment_filename=imagepath.split("/")[-1])

        except Exception as e:
            return str(e)


# needed to run on command line
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
