#!/bin/bash

# Define colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

check_docker() {
    if command -v docker &>/dev/null; then
        echo -e "[${GREEN}OK${NC}] Docker is installed."
    else
        echo -e "[${RED}KO${NC}] Docker is not installed. Attempting to install..."
        install_docker
    fi
}

install_docker() {
    # Detect package manager and install Docker accordingly
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install docker.io -y
    elif command -v dnf &>/dev/null; then
        sudo dnf install docker -y
    elif command -v yum &>/dev/null; then
        sudo yum install docker -y
    else
        echo -e "[${RED}KO${NC}] Package manager not supported. Please install Docker manually."
        exit 1
    fi
    sudo systemctl start docker
    sudo systemctl enable docker
}

check_docker_group() {
    if id -nG "$USER" | grep -qw docker; then
        echo -e "[${GREEN}OK${NC}] User is in the docker group."
    else
        echo -e "[${RED}KO${NC}] User is not in the docker group. Adding..."
        sudo usermod -aG docker $USER
    fi
}

check_docker_compose() {
    if command -v docker-compose &>/dev/null; then
        echo -e "[${GREEN}OK${NC}] Docker Compose is installed."
    else
        echo -e "[${RED}KO${NC}] Docker Compose is not installed. Attempting to install..."
        install_docker_compose
    fi
}

install_docker_compose() {
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
}

launch_pykers() {
    cd bin && sudo docker-compose up -d

    # Wait for a few seconds to allow services to start
    sleep 5

    # Check if the service is running on port 5001 using curl
    if curl --output /dev/null --silent --head --fail http://127.0.0.1:5001; then
        echo -e "[${GREEN}OK${NC}] Pykers is running and accessible!"
        echo "URL: http://127.0.0.1:5001"

        # Display the local IP of the machine
        local_ip=$(hostname -I | awk '{print $1}')
        echo "Or access via local network IP: http://$local_ip:5001"

        # Reminder about the container
        echo "Remember, if you kill the container 'pykers-web', you'll need to run this script again to restart the application."
    else
        echo -e "[${RED}KO${NC}] Failed to access Pykers. Please check the service."
    fi
}

check_docker
check_docker_group
check_docker_compose
launch_pykers
