import operator
import psutil
from flask import Flask, render_template, request, make_response
import sqlite3
from flask import Flask, send_file
import pandas as pd
import json
import db
from time import time
from random import random
from bar_graph import create_plot

app = Flask(__name__)


@app.route("/names.json", methods=['GET', 'POST'])
def name():
    if request.method == 'GET':
        names = []
        psutil.cpu_percent(interval=1)
        procs = psutil.process_iter()
        all_procs = [[proc.cpu_percent(), proc.name(), proc.pid] for proc in procs]
        procss = all_procs[:3]
        for proc in all_procs[:3]:
            names.append(proc[1])
        return json.dumps(names)


@app.route("/data.json", methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        # db.main()
        # connection = sqlite3.connect("db.sqlite")
        # cursor = connection.cursor()
        # cursor.execute("SELECT 1000*timestamp, measure from measures")
        # result = cursor.fetchall()
        # cursor.close()
        # return json.dumps(result)
        results = []
        result = []
        connection = sqlite3.connect("db.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT id from measures GROUP BY id ")
        ids = cursor.fetchall()
        print(ids)
        print("jjj")
        for ID in ids:
            print(ID[0])
            cursor.execute("SELECT timestamp, measure from measures WHERE id=?", (ID[0],))
            result = cursor.fetchall()
            results.append(result)
            print(results)
        cursor.close()
        return json.dumps(results)


@app.route("/")
def graph():
    # clear the table
    # db.clear_table()

    if request.method == 'GET':
        names = []
        psutil.cpu_percent(interval=1)
        procs = psutil.process_iter()
        all_procs = [[proc.cpu_percent(), proc.name(), proc.pid] for proc in procs]
        procss = all_procs[:3]
        for proc in all_procs[:3]:
            names.append(proc[1])
        ids = []
        for proc in all_procs[:3]:
            print(id)
            ids.append(proc[2])
        # db.main(ids)
        mem = psutil.virtual_memory()
        # bar chart
        bar = create_plot(mem)
        # pie chart
        data = {'Memory': 'bytes', 'total': mem.total, 'available': mem.available, 'used': mem.used, 'free': mem.free}

        return render_template('graph.html', procss=procss, data=data, plot=bar, names=names)


@app.route('/live-graph')
def hello_world():
    return render_template('index.html')


@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, psutil.cpu_percent()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)