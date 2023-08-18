from http.client import NOT_FOUND
from flask import render_template, jsonify, request
import docker
from docker.errors import ImageNotFound


client = docker.from_env()

def port_view():
  
    containers = client.containers.list(all=True)
    ports_data = []

    for container in containers:
        ports = container.attrs['NetworkSettings']['Ports']
        for host_config in ports.values():
            if host_config:
                for config in host_config:
                    port_info = {
                        "host_port": config["HostPort"],
                        "container_port": config["HostIp"] + ":" + config["HostPort"],
                        "name": container.name,
                        "active": container.status == "running",
                        "id": container.id,
                        "ip_type": "IPv6" if "::" in config["HostIp"] else "IPv4"
                    }
                    ports_data.append(port_info)

    # Group by container name
    grouped_ports = {}
    for port in ports_data:
        if port["name"] in grouped_ports:
            grouped_ports[port["name"]].append(port)
        else:
            grouped_ports[port["name"]] = [port]

    return render_template('ports.html', grouped_ports=grouped_ports)
