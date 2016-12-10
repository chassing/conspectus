# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import docker

app = Flask(__name__)
Bootstrap(app)

client = docker.from_env()


@app.route("/")
def index():
    # get all services
    services = {}
    for service in client.services():
        services[service['ID']] = service

    # get all tasks and enrich them with service name
    tasks = {}
    for task in client.tasks():
        task["service_name"] = services[task['ServiceID']]['Spec']['Name']
        if task['NodeID'] not in tasks:
            tasks[task['NodeID']] = []
        tasks[task['NodeID']].append(task)

    # get all nodes and enrich them with tasks
    nodes = []
    for node in client.nodes():
        node['tasks'] = tasks[node['ID']]
        nodes.append(node)

    return render_template('index.html', nodes=nodes)


if __name__ == "__main__":
    app.run()
