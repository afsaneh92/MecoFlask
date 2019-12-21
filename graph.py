import operator
import psutil
from flask import Flask, render_template, request
import sqlite3
import json
import pandas as pd
from flask import Flask, send_file
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
import db
from flask import jsonify


app = Flask(__name__)


@app.route("/data.json", methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        db.main()
        connection = sqlite3.connect("db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT 1000*timestamp, measure from measures")
        result = cursor.fetchall()
        cursor.close()
        return json.dumps(result)
        # results = []
        # result = []
        # connection = sqlite3.connect("db.sqlite")
        # cursor = connection.cursor()
        # cursor.execute("SELECT id from measures GROUP BY id ")
        # ids = cursor.fetchall()
        # print(ids)
        # print("jjj")
        # for ID in ids:
        #
        #     print(ID[0])
        #     cursor.execute("SELECT 10*timestamp, measure from measures WHERE id=?", (ID[0],))
        #     result = cursor.fetchall()
        #     results.append(result)
        #     print(results)
        # cursor.close()
        # return json.dumps(result)

    if request.method == 'POST':
        jsdata = request.form['javascript_data']
        jsdata = json.loads(jsdata)
        print(jsdata)
        # db.main(int(4))

        # for id in jsdata:
        #     print(id)
        #     db.main(int(id))

        results = []
        connection = sqlite3.connect("db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT id from measures GROUP BY id ")
        ids = cursor.fetchall()
        print(ids)
        print("iiii")
        for ID in ids:
            result = []
            print(ID[0])
            cursor.execute("SELECT 10*timestamp, measure from measures WHERE id=?", (ID[0],))
            result = cursor.fetchall()
            results.append(result)
            print(len(results))
            print(results)

        cursor.close()
        return json.dumps(results)


@app.route("/")
def graph():
    # clear the table
    db.clear_table()

    if request.method == 'GET':
        psutil.cpu_percent(interval=1)
        procs = psutil.process_iter()
        all_procs = [[proc.cpu_percent(), proc.name(), proc.pid] for proc in procs]
        procss = all_procs[:3]
        # for proc in all_procs[:3]:
        #     procss.append(proc[1])
        mem = psutil.virtual_memory()
        # bar chart
        bar = create_plot(mem)
        # pie chart
        data = {'Memory': 'bytes', 'total': mem.total, 'available': mem.available, 'used': mem.used, 'free': mem.free}

        return render_template('graph.html', procss=procss, data=data, plot=bar)


def create_plot(mem):

    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

    data = [
        go.Bar(
            x=['total', 'available', 'used', 'free'], # assign x as the dataframe column 'x'
            y=[ mem.total,  mem.available, mem.used,  mem.free]
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == '__main__':
    app.run(port=5000, debug=True)