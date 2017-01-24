# -*- coding: utf-8 -*-
import docker
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sanic import Sanic
from sanic.response import html

import webcolors

app = Sanic(__name__)
app.static('/static', './static')
client = docker.from_env()

env = Environment(
    loader=FileSystemLoader('./templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

MICRO = 1000
MINUTES = MICRO * 60

# unset http proxies
for item in ["http_proxy", "https_proxy"]:
    try:
        del os.environ[item]
    except:
        pass

    try:
        del os.environ[item.upper()]
    except:
        pass


@app.route("/")
def index(request):
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
        try:
            node['tasks'] = sorted(tasks[node['ID']], key=lambda x: x["service_name"])
        except KeyError:
            node['tasks'] = []
        if "ManagerStatus" not in node:
            node['ManagerStatus'] = {'Leader': False}
        nodes.append(node)

    return html(env.get_template('index.html').render(nodes=sorted(nodes, key=lambda x: x['Description']['Hostname']), reload=int(request.args.get('reload', 100)) * MINUTES))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True if os.getenv('DEBUG') else False)
