function createContainerElement(container) {
    var containerElement = document.createElement('div');
    containerElement.className = 'col-4 py-3';

    var cardElement = document.createElement('div');
    cardElement.className = 'card text-center';
    if (container.status === 'running') {
        cardElement.className += ' bg-success';
    } else {
        cardElement.className += ' bg-secondary';
    }

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

function updateContainers() {
    $.get('/home/api/containers', function(data) {
        var containerListElement = document.getElementById('container-list');
        while (containerListElement.firstChild) {
            containerListElement.firstChild.remove();
        }

        data.sort(function(a, b) {
            if (a.status === 'running' && b.status !== 'running') {
                return -1;
            } else if (a.status !== 'running' && b.status === 'running') {
                return 1;
            } else {
                return 0;
            }
        });
        data.forEach(function(container) {
            containerListElement.appendChild(createContainerElement(container));
        });
    });
}


updateContainers();
setInterval(updateContainers, 5000);
