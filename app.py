# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import docker

app = Flask(__name__)
Bootstrap(app)

client = docker.from_env()


@app.route("/")
def index():
    # for node in client.nodes()
    from pprint import pprint
    nodes = []
    for n in client.nodes():
        n['tasks'] = []
        for task in client.tasks(filters={'node': n['ID']}):
            task['service_name'] = client.services(filters={'id': task['ServiceID']})[0]['Spec']['Name']
            pprint(task)
            n['tasks'].append(task)
        nodes.append(n)

    pprint(nodes)
    return render_template('index.html', nodes=nodes)


if __name__ == "__main__":
    app.run()
