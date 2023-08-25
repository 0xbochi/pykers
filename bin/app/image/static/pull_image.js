$(document).ready(function() {
    /**
     * Show the loading spinner.
     */
    function showLoadingSpinner() {
        $('#loading-spinner').show();
    }

    /**
     * Hide the loading spinner.
     */
    function hideLoadingSpinner() {
        $('#loading-spinner').hide();
    }

    /**
     * Reset the alert container.
     */
    function resetAlertContainer() {
        $('#alert-container').text('').hide();
    }

    /**
     * Handle the image pull response.
     * 
     * @param {Object} response - The response from the server.
     */
    function handleImagePullResponse(response) {
        hideLoadingSpinner();

        if (response.status === 'success') {
            alert('Image pulled successfully!');
            window.location.href = '/image';
        } else {
            $('#alert-container').text(response.message).show();
        }
    }

    /**
     * Initialize the pull image form submit event.
     */
    function initPullImageForm() {
        $('#pull-image-form').submit(function(e) {
            e.preventDefault();
            showLoadingSpinner();
            
            const imageName = $('#image-name').val();

            $('#pull-image-form button[type="submit"]').click(resetAlertContainer);

            $.post('/image/pull_image', { image_name: imageName }, handleImagePullResponse);
        });
    }

    // Initialize the event listeners and handlers.
    initPullImageForm();
});
