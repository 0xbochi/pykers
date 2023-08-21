/**
 * Creates and returns a DOM element representing a container.
 * 
 * @param {Object} container - The container data.
 * @returns {HTMLElement} - The container DOM element.
 */
function createContainerElement(container) {
    var containerElement = document.createElement('div');
    containerElement.className = 'col-4 py-3';

    var cardElement = document.createElement('div');
    cardElement.className = 'card text-center';
    cardElement.className += container.status === 'running' ? ' bg-success' : ' bg-secondary';

    var cardBodyElement = document.createElement('div');
    cardBodyElement.className = 'card-body';

    var cardLinkElement = document.createElement('a');
    cardLinkElement.href = '/container/' + container.id;
    cardLinkElement.className = 'text-white stretched-link';

    var cardTitleElement = document.createElement('h5');
    cardTitleElement.className = 'card-title';
    cardTitleElement.textContent = container.name;

    var cardImageElement = document.createElement('p');
    cardImageElement.className = 'card-text';
    cardImageElement.textContent = 'Image: ' + container.image;

    var cardStatusElement = document.createElement('p');
    cardStatusElement.className = 'card-text';
    cardStatusElement.textContent = 'Status: ' + container.status;

    cardBodyElement.appendChild(cardImageElement);
    cardBodyElement.appendChild(cardTitleElement);
    cardBodyElement.appendChild(cardStatusElement);
    cardLinkElement.appendChild(cardBodyElement);
    cardElement.appendChild(cardLinkElement);
    containerElement.appendChild(cardElement);

    return containerElement;
}

/**
 * Fetches container data from the API and updates the container list on the page.
 */
function updateContainers() {
    $.get('/home/api/containers', function(data) {
        var containerListElement = document.getElementById('container-list');
        
        // Clear existing container elements
        while (containerListElement.firstChild) {
            containerListElement.firstChild.remove();
        }

        // Sort containers: running containers first
        data.sort(function(a, b) {
            if (a.status === 'running' && b.status !== 'running') {
                return -1;
            } else if (a.status !== 'running' && b.status === 'running') {
                return 1;
            } else {
                return 0;
            }
        });

        // Append new container elements
        data.forEach(function(container) {
            containerListElement.appendChild(createContainerElement(container));
        });
    });
}

// Initial call to update the containers
updateContainers();

// Update the containers every 5 seconds
setInterval(updateContainers, 5000);
