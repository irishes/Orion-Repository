from flask import Flask, render_template, request, url_for
from mdUtility import extractIsisData, extractImage, cleanDirs, trimData
import os
from werkzeug.utils import secure_filename
from subprocess import CalledProcessError


# global variable
# CURRENT_FILE will be removed later
CURRENT_FILE = ''
SAMPLE_LINES = 200

# Flask App Environment
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
IMAGE_FOLDER = os.path.join(APP_ROOT, 'static/images')
PVL_FOLDER = os.path.join(APP_ROOT, 'static/pvl')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['PVL_FOLDER'] = PVL_FOLDER


# index.html
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


# upload and save process
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    # if request is post
    if request.method == 'POST':
        # try to extract the file in teh uploadFile form
        try:
            file = request.files['uploadFile']
        except KeyError:
            # catches NULL error and makes user try again
            print("Null File Error: please enter a .cub file ")
            return render_template("index.html")

        # slip the filename on every '.' and grab the last slot to verify it is a .cub file a
        # lso check for an empty filename
        if file.filename.split('.')[-1] == 'cub' and file.filename != '':

            # save the file to the upload directory
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            # save the current filepath to the global variable
            global CURRENT_FILE
            CURRENT_FILE = file.filename

            # open the file we just saved
            file = open(os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE), mode="r")

            # extract the n lines of data and close the file
            return_filename = extractIsisData(file, SAMPLE_LINES)
            file.close()

            # open the output file and read it into a variabale
            testFile = open(return_filename, "r")
            pagecontent = testFile.read()

            # close the output file
            testFile.close()
        else:
            # wrong file type try again
            return render_template('index.html')

            # try to open the uploaded file for read

        try:
            file = open(os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE), "r")
        except FileNotFoundError:
            # let the user try again
            print("Flask could not find the cube file")
            return render_template("index.html")

        # check if the file is empty or not a cube
        if CURRENT_FILE.split('.')[-1] == 'cub' and CURRENT_FILE != '':

            # this try except allows us to run a console command and catch any errors to stop from program crash
            try:
                # this line is calling a string shell command by creating the command string on a single line
                imagename = extractImage(CURRENT_FILE)
                command_return_file = "return.pvl"
                cleanDirs(app.config['PVL_FOLDER'], "ers", command_return_file)

                os.system("campt from=" + os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE)
                          + " to=" + os.path.join(app.config['PVL_FOLDER'], command_return_file))
                os.system("catlab from=" + os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE)
                          + " to=" + os.path.join(app.config['PVL_FOLDER'], command_return_file))
                os.system("catoriglab from=" + os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE)
                          + " to=" + os.path.join(app.config['PVL_FOLDER'], command_return_file))
            except CalledProcessError:
                  print("The command returned CalledProcessError")

            try:
                # try and open the output file
                returnFile = open(os.path.join(app.config['PVL_FOLDER'], command_return_file), "r")
                returnString = returnFile.read()
                returnFile.close()
                file.close()
                full_filename = url_for('static', filename='images/' + imagename)

                # parse file and fill dict
                cubeDictionary = trimData(os.path.join(app.config['PVL_FOLDER'], command_return_file))
                cubeDictionary['image'] = imagename
                for i in cubeDictionary:
                    print(str(i + " : " + cubeDictionary[i]))



                # return filled in text file to user
                return render_template("pwd.html", OT=returnString, IMG=full_filename)
            # catch file not found
            except FileNotFoundError:
                print("ISIS3 command failed to create a pvl")
                return render_template("error.html")

        else:
            print("Input File Error")
            if not file.closed:
                file.close()
            return render_template("index.html")


# needed to run on command line
if __name__ == '__main__':
    app.run(debug=True)
