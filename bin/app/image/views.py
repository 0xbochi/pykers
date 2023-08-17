from http.client import NOT_FOUND
from flask import render_template, jsonify, request
import docker
from docker.errors import ImageNotFound


client = docker.from_env()

def image_view():
  
    images_list = client.images.list()
    images_info = []

    for img in images_list:
        img_name = img.tags[0] if img.tags else "Unnamed"
        containers_using = client.containers.list(all=True, filters={"ancestor": img.id})
        images_info.append({
            "name": img_name,
            "id": img.id,  # Ajout de l'id de l'image
            "used_by": len(containers_using)
        })

    return render_template('image.html', images=images_info)




def pull_image():
    image_name = request.form.get('image_name')
    try:
        client.images.pull(image_name)
        return jsonify({'message': 'Image pulled successfully!', 'error': False})
    except Exception as e:
        return jsonify({'message': str(e), 'error': True})



def delete_image():
    image_id = request.form.get('image_id')
    try:
        client.images.remove(image_id)
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
