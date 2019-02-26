from flask import Flask, Response, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('basic.html')

@app.route("/getPlotCSV")
def getPlotCSV():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = 'targetname,mars\ntargetbody,5\naugulas,30'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=exportISIS.csv"})

if __name__ == "__main__":
    app.run(debug=True)
