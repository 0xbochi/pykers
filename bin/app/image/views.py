"""View of image application"""
from http.client import NOT_FOUND
from flask import render_template, jsonify, request
import docker
from docker.errors import ImageNotFound


client = docker.from_env()


def image_view() -> str:
    """
    Retrieve and display details of all Docker images.

    This function fetches a list of all Docker images and extracts relevant details
    such as their name, ID, and the number of containers using each image. If an image
    does not have a name, it defaults to "Unnamed". The images are then sorted based on
    the number of containers using them in descending order and displayed in the 'image.html'
    template.

    Returns:
        str: Rendered 'image.html' template with details of images.
    """
    images_list = client.images.list()
    images_info = []

    for img in images_list:
        img_name = img.tags[0] if img.tags else "Unnamed"
        containers_using = client.containers.list(
            all=True, filters={"ancestor": img.id})
        images_info.append({
            "name": img_name,
            "id": img.id,
            "used_by": len(containers_using)
        })

    images_info = sorted(images_info, key=lambda x: x["used_by"], reverse=True)
    return render_template('image.html', images=images_info)


def pull_image() -> dict:
    """
    Pull a Docker image based on the provided image name.

    This function attempts to pull a Docker image using the name provided in the request form.
    If the image is pulled successfully, a success message is returned. If there's an error during
    the pull operation, an error message containing the exception details is returned.

    Returns:
        dict: A dictionary containing a message about the pull operation and an error status.
    """
    image_name = request.form.get('image_name')
    try:
        client.images.pull(image_name)
        return jsonify(
            {'message': 'Image pulled successfully!', 'error': False})
    except Exception as e:
        return jsonify({'message': str(e), 'error': True})


def delete_image() -> tuple[dict, int]:
    """
    Delete a Docker image based on the provided image ID.

    This function attempts to delete a Docker image using the ID provided in the request form.
    If the image is deleted successfully, a success message and a 200 HTTP status code are returned.
    If there's an error during the deletion operation, an error message containing the exception
    details and a 500 HTTP status code are returned.

    Returns:
        Tuple[dict, int]: A tuple containing a dictionary with a message about the deletion operation
                          and an HTTP status code.
    """
    image_id = request.form.get('image_id')
    try:
        client.images.remove(image_id)
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_containers_for_image() -> dict:
    """
    Delete all Docker containers associated with a specific image ID.

    This function fetches all Docker containers associated with the provided image ID
    from the request form. It then attempts to delete each container. If any container
    deletion fails, an error message containing the exception details is returned.
    If all containers are deleted successfully, a success status is returned.

    Returns:
        dict: A dictionary containing either a success status or an error message.
    """
    image_id = request.form.get('image_id')
    containers = client.containers.list(
        all=True, filters={"ancestor": image_id})

    for container in containers:
        try:
            container.remove(force=True)
        except Exception as e:
            return jsonify(error=str(e)), 500

    return jsonify(success=True)


def pull_image() -> dict:
    """
    Pull a Docker image using the name provided in the request.

    This function pulls an image based on the name given in the request form. If successful, 
    it returns a dictionary with a success status. If there is an exception during the process, 
    it returns a dictionary with the error status and the exception message.

    Returns:
        dict: A dictionary indicating the result of the pull operation with either a success 
              message or an error message.
    """
    if request.method != 'POST':
        return render_template('pull_image.html')
    
    image_name = request.form.get('image_name')
    
    try:
        client.images.pull(image_name)
        return jsonify({'status': 'success', 'message': 'Image pulled successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})