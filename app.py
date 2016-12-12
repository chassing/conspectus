# -*- coding: utf-8 -*-
import docker

from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

import webcolors

app = Flask(__name__)
Bootstrap(app)

client = docker.from_env()

MICRO = 1000
MINUTES = MICRO * 60


@app.route("/")
def index():
    # get all services
    services = {}
    for service in client.services():
        services[service['ID']] = service

    # get all tasks and enrich them with service name
    tasks = {}
    for task in client.tasks(filters={'desired-state': 'running'}):
        service_name = services[task['ServiceID']]['Spec']['Name']
        task["service_name"] = service_name
        task["color"] = "rgba({},{},{},0.35)".format(*webcolors.html5_parse_legacy_color(service_name))
        if task['NodeID'] not in tasks:
            tasks[task['NodeID']] = []
        tasks[task['NodeID']].append(task)

    # get all nodes and enrich them with tasks
    nodes = []
    for node in client.nodes():
        node['tasks'] = sorted(tasks[node['ID']], key=lambda x: x["service_name"])
        if "ManagerStatus" not in node:
            node['ManagerStatus'] = {'Leader': False}
        nodes.append(node)

    return render_template('index.html', nodes=nodes, reload=int(request.args.get('reload', 100)) * MINUTES)


if __name__ == "__main__":
    app.run()
