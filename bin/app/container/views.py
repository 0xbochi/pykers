from flask import render_template, request, jsonify, redirect, url_for, send_file
from docker import DockerClient
from docker.errors import NotFound, ImageNotFound
import os


client = DockerClient.from_env()


def details(id):
    try:
        c = client.containers.get(id)
        return render_template('details.html', container=c)
    except NotFound:
        return "Container not found", 404


def stop(id):
    try:
        c = client.containers.get(id)
        c.stop()
        return redirect(url_for('container.details', id=id))
    except NotFound:
        return "Container not found", 404

def start(id):
    try:
        c = client.containers.get(id)
        c.start()
        return redirect(url_for('container.details', id=id))
    except NotFound:
        return "Container not found", 404

def remove(id):
    try:
        c = client.containers.get(id)
        if c.status == 'running':
            c.stop()
        c.remove()
        return redirect(url_for('home.index'))
    except NotFound:
        return "Container not found", 404
    

def details_api(id):
    try:
        c = client.containers.get(id)

        try:
            image_tag = c.image.tags[0] if c.image.tags else "No image"
        except ImageNotFound:
            image_tag = "No image"

        return jsonify({
            'name': c.name,
            'status': c.status,
            'image': image_tag,
            'command': ' '.join(c.attrs['Config']['Cmd']),
            'created': c.attrs['Created'],
            'id': c.id,
            'networks': ', '.join(c.attrs['NetworkSettings']['Networks']),
            'mounts': ', '.join([mount['Source'] for mount in c.attrs['Mounts']]),
            'ports': ', '.join([f"{k}->{v[0]['HostPort']}" for k, v in c.attrs['NetworkSettings']['Ports'].items() if v is not None]),
            'environment': ', '.join(c.attrs['Config']['Env'])
        })
    except NotFound:
        return "Container not found", 404



def restart(id):
    try:
        c = client.containers.get(id)
        c.restart()
        return redirect(url_for('container.details', id=id))
    except NotFound:
        return "Container not found", 404
    

def logs(id):
    try:
        c = client.containers.get(id)
        return jsonify({
            'logs': c.logs().decode()
        })
    except NotFound:
        return "Container not found", 404
    

def stats(id):
    try:
        c = client.containers.get(id)
        return jsonify({
            'stats': c.stats(stream=False)
        })
    except NotFound:
        return "Container not found", 404
    
def exec(id):
    try:
        c = client.containers.get(id)
        command = request.form.get('command')
        exit_code, output = c.exec_run(command)
        return output.decode('utf-8')
    except NotFound:
        return "Container not found", 404
    

def inspect(id):
    try:
        c = client.containers.get(id)
        return jsonify(c.attrs)
    except NotFound:
        return "Container not found", 404
    


def copy(id):
    try:
        c = client.containers.get(id)
        src_path = request.form.get('src_path')
        dest_path = '/tmp'
        

        file_name = os.path.basename(src_path)
        
        container_directory = os.path.join(dest_path, c.name)
        os.makedirs(container_directory, exist_ok=True)
        
        dest_file_path = os.path.join(container_directory, file_name)
        
        tar_stream, stat = c.get_archive(src_path)
        
        with open(dest_file_path, 'wb') as file:
            for chunk in tar_stream:
                file.write(chunk)

        return jsonify({'message': 'File copied successfully.'}), 200
    except NotFound:
        return "Container not found", 404
    except Exception as e:
        print(e)
        return str(e), 500