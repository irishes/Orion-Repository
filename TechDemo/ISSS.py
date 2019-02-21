from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from subprocess import CalledProcessError


# global variable
# CURRENT_FILE will be removed later
CURRENT_FILE = ''
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
SAMPLE_LINES = 63

# Flask App Environment
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# index.html
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


# campt function and return render html with the string variable data
@app.route("/upload/campt", methods=['GET', 'POST'])
def campt():
    # check if current method is post request
    if request.method == 'POST':
        # try to open the uploaded file for read
        try:
            file = open(os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE), "r")
        except FileNotFoundError:
            # let the user try again
            print("Flask could not find the cube file")
            return render_template("index.html")
        # check if the file is empty or not a cube
        if CURRENT_FILE.split('.')[-1] == 'cub' and CURRENT_FILE != '':
            # print("RUNS CORRECTLY")

            # this try except allows us to run a console command and catch any errors to stop from program crash
            try:
                # this line is calling a string shell command by creating the command string on a single line
                os.system("campt from=" + os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_FILE) + " to= return.pvl ")
            except CalledProcessError:
                print("The command returned CalledProccessError")

            try:
                # try and open the output file

                returnFile = open("return.pvl", "r")
                returnString = returnFile.read()
                returnFile.close()
                file.close()
                return render_template("pwd.html", OT=returnString)
            # catch file not found
            except FileNotFoundError:
                print("ISIS3 command failed to create a pvl")
                return render_template("error.html")

        else:
            print("AHHHHHHH!")
            if not file.closed:
                file.close()
            return render_template("index.html")


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

        # slip the filename on every '.' and grab the last slot to verify it is a .cub file also check for an empty filename
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

            # render the html page with the variable filled in
            return render_template('ls.html', filecontent=pagecontent)
        else:
            # wrong file type try again
            return render_template('index.html')


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


# needed to run on command line
if __name__ == '__main__':
    app.run(debug=True)
