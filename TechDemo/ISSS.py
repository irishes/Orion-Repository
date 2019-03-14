from flask import Flask, render_template, request, url_for, Response, send_file
from mdUtility import DataObject
import threading
import os
import ast
from werkzeug.utils import secure_filename


# global variable
# CURRENT_FILE will be removed later

SAMPLE_LINES = 200

# temp vars
users = 0


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
    loadingGif = url_for('static', filename='images/loading.gif')
    return render_template('index.html', LOADINGGIF=loadingGif)


# upload and save process
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    global users
    # if request is post
    if request.method == 'POST':
        # make file an instance of a data class and extract all the tags from that data.
        # in order to do this i need a class called filedata
        # try to extract the file in the uploadFile form
        try:
            cubeFile = request.files['uploadFile']

        except KeyError:
            # catches NULL error and makes user try again
            print("Null File Error: please enter a .cub file ")
            return render_template("index.html")

        try:
            tplFile = request.files['templateFile']
            current_instance = DataObject(cubeFile.filename, tplFile.filename)

        except KeyError:
            current_instance = DataObject(cubeFile.filename)

        # init div dict
        current_instance.divDict = DataObject.initDict(current_instance)
        # print(current_instance.divDict)

        if (current_instance.tplFile.split('.')[-1] == 'tpl' and current_instance.tplFile != '') \
                and (current_instance.filename.split('.')[-1] == 'cub' and current_instance.filename != ''):
            # save the file to the upload directory
            cubeFile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(current_instance.filename)))
            if current_instance.tplFile != 'Default.tpl':
                # save the file to the upload directory
                tplFile.save(os.path.join(app.config['TPL_FOLDER'], secure_filename(current_instance.tplFile)))

            #   *--temp variable counter --*
            users += 1

            # print(current_instance.filename)
            # print("total upload requests = " + str(users))

            # this try except allows us to run a console command and catch any errors to stop from program crash
            try:
                # this line is calling a string shell command by creating the command string on a single line
                imageExtractThread = threading.Thread(target=DataObject.extractImage,
                                                      args=(current_instance, current_instance.filename,),
                                                      name='imageExtractThread'
                                                      )
                isisCommandThread = threading.Thread(target=DataObject.run_isis,
                                                      args=(current_instance,),
                                                      name='imageExtractThread'
                                                      )

                imageExtractThread.start()
                isisCommandThread.start()

                command_file_output = isisCommandThread.join()
                imageExtractThread.join()

            except Exception as e:
                print('Threading Section Critical Failure:' + str(e))
                if current_instance:
                    del current_instance
                return render_template("index.html")

            try:
                current_instance.rawFileData = DataObject.extractRawData(current_instance, os.path.join(app.config['PVL_FOLDER'], 'return.pvl'))
                #print(current_instance.rawFileData)

                templateFile = open(os.path.join(app.config['TPL_FOLDER'], current_instance.tplFile), "r")
                templateString = templateFile.read()
                templateFile.close()

                full_filename = url_for('static', filename='images/' + current_instance.divDict['image'])

                # parse file and fill dict
                current_instance.divDict = DataObject.trimData(current_instance, os.path.join(app.config['PVL_FOLDER'], 'return.pvl'))
                current_instance.divDict['image'] = full_filename

                current_instance.divDict = DataObject.removeNulls(current_instance, current_instance.divDict)
                # return filled in text file to user
                return render_template("output.html", DICTSTRING=current_instance.divDict, TEMPAREA=templateString,
                                       IMG=current_instance.divDict['image'], CSVSTRING=current_instance.rawFileData)
            # catch file not found
            except FileNotFoundError:
                print("ISIS3 command failed to create a pvl")
                return render_template("error.html")
        else:
            print("Input File Error")
            return render_template("index.html")


@app.route('/showImage', methods=['POST'])
def showImage():
    if request.method == 'POST':
        image = request.form.get('image_present')
        return render_template("imageDisplay.html", IMG=image)


@app.route('/getCSV', methods=['GET', 'POST'])
def getCSV():
    if request.method == 'POST':

        csvString = request.form.get('passedTXT')
        new_str = ""
        csvString = ast.literal_eval(csvString)

        for key, value in csvString.items():
            new_str = new_str + str(key) + ", " + str(value) + "\n"

        return Response(
            new_str,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=exportISIS.csv"})


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
    app.run(debug=True)
