from flask import Flask, render_template, request, url_for, Response, send_file
from mdUtility import extractImage, cleanDirs, trimData, camptInterface, catoriglabInterface, catlabInterface, removeNulls
import os
import ast
from werkzeug.utils import secure_filename
from subprocess import CalledProcessError


# global variable
# CURRENT_FILE will be removed later
CURRENT_FILE = ''
CURRENT_TPL_FILE = ''
SAMPLE_LINES = 200
cubeDictionary = ''

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


# index.html
@app.route("/", methods=["GET"])
def index():
    global CURRENT_FILE, CURRENT_TPL_FILE
    CURRENT_FILE, CURRENT_TPL_FILE = "", ""
    return render_template('index.html')


# upload and save process
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # if request is post
    if request.method == 'POST':
        # try to extract the file in the uploadFile form
        try:
            # get cube file
            cubeFile = request.files['uploadFile']
            # get template file
            templateFile = request.files['templateFile']
        except KeyError:
            # catches NULL error and makes user try again
            print("Null File Error: please enter a .cub file ")
            return render_template("index.html")

        if (templateFile.filename.split('.')[-1] == 'tpl' and templateFile.filename != '') \
                and (cubeFile.filename.split('.')[-1] == 'cub' and cubeFile.filename != ''):

            # save the file to the upload directory
            cubeFile.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(cubeFile.filename)))
            # save the current filepath to the global variable
            global CURRENT_FILE
            CURRENT_FILE = cubeFile.filename

            # save the file to the upload directory
            templateFile.save(os.path.join(app.config['TPL_FOLDER'], secure_filename(templateFile.filename)))

            # save the current filepath to the global variable
            global CURRENT_TPL_FILE
            CURRENT_TPL_FILE = templateFile.filename

        # check if the file is empty or not a cube
        if CURRENT_FILE.split('.')[-1] == 'cub' and CURRENT_FILE != '':
            # this try except allows us to run a console command and catch any errors to stop from program crash
            try:
                # this line is calling a string shell command by creating the command string on a single line
                imagename = extractImage(CURRENT_FILE)
                command_return_file = "return.pvl"
                cleanDirs(app.config['PVL_FOLDER'], "ers", command_return_file)

                # campt os call to terminal and saves in return file
                camptInterface(CURRENT_FILE, command_return_file)
                # catlab os call to terminal and saves in return file
                catlabInterface(CURRENT_FILE, command_return_file)
                # catoriglab os call to terminal and saves in return file
                catoriglabInterface(CURRENT_FILE, command_return_file)

            except Exception as e:
                  print(str(e))

            try:
                templateFile = open(os.path.join(app.config['TPL_FOLDER'], CURRENT_TPL_FILE), "r")
                templateString = templateFile.read()
                templateFile.close()
                full_filename = url_for('static', filename='images/' + imagename)

                # parse file and fill dict
                global cubeDictionary 
                cubeDictionary = trimData(os.path.join(app.config['PVL_FOLDER'], command_return_file))
                cubeDictionary['image'] = full_filename

                cubeDictionary = removeNulls(cubeDictionary)
                # return filled in text file to user
                return render_template("output.html", DICTSTRING=cubeDictionary, TEMPAREA=templateString, IMG=cubeDictionary['image'])
            # catch file not found
            except FileNotFoundError:
                print("ISIS3 command failed to create a pvl")
                return render_template("error.html")

        else:
            print("Input File Error")
            return render_template("index.html")


@app.route('/getCSV', methods=['GET', 'POST'])
def getCSV():
    if request.method == 'POST':

        csvString = request.form.get('passedTXT')
        new_str = ""
        csvString = ast.literal_eval(csvString)

        for key, value in csvString.items():
            new_str = new_str + key + ", " + value + "\n"

        return Response(
            new_str,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=exportISIS.csv"})


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
            return(str(e))

@app.route('/showImage')
def showImage():
    global cubeDictionary
    IMG = cubeDictionary['image']
    return render_template("imageDisplay.html", IMG=IMG)

# @app.route('/getTemplate', methods=['GET', 'POST'])
# def getTemplate():
#     if request.method == 'POST':

#         tplString = request.form.get('passedTPL')

#         return Response(
#             tplString,
#             mimetype="text/plain",
#             headers={"Content-disposition":
#                          "attachment; filename=exportTPL.txt"})



# needed to run on command line
if __name__ == '__main__':
    app.run(debug=True)

