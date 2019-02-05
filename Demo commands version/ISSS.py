from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ls/", methods=['POST'])
def move_ls():
    output = subprocess.check_output('ls -lah',shell = True)
    return render_template('ls.html', OT = output)

@app.route("/pwd/", methods=['POST'])
def move_pwd():
    output = subprocess.check_output('pwd',shell = True)
    return render_template('pwd.html', OT = output)

if __name__ == '__main__':
    app.run(debug = True)