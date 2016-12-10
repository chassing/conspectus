Conspectus
==========

Conspectus is a small shiny overview page for your Docker Swarm cluster.

Usage
-----

As prerequisite setup your swarm cluster before you run Conspectus, see `Docker Swarm Documentation <https://docs.docker.com/engine/swarm/>`_.

Run Conspectus itself as docker service and point your browser afterwards to http://cluster-manager:8000. You have to run conspectus on a swarm manager and bind mount the docker socket too.

.. code-block:: bash

    $ docker service create --name conspectus -p 8000:5000 --mount src=/var/run/docker.sock,dst=/var/run/docker.sock,type=bind --constraint "node.role == manager" conspectus:latest
    ✨🍻😎✨
