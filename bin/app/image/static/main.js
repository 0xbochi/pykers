$(document).ready(function() {
    /**
     * Shows the spinner next to the given button.
     * 
     * @param {HTMLElement} button - The button element.
     */
    function showSpinner(button) {
        $(button).siblings('.spinner-border').show();
    }

    /**
     * Hides the spinner next to the given button.
     * 
     * @param {HTMLElement} button - The button element.
     */
    function hideSpinner(button) {
        $(button).siblings('.spinner-border').hide();
    }

    /**
     * Handles the delete image action.
     */
    $('.delete-image').click(function() {
        let imageId = $(this).data('id');
        
        showSpinner(this);

        $.ajax({
            type: 'POST',
            url: '/image/delete',
            data: {'image_id': imageId},
            success: (data) => {
                hideSpinner(this);
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    location.reload();
                }
            },
            error: () => {
                hideSpinner(this);
                alert('An error occurred. Please try again.');
            }
        });
    });

    /**
     * Handles the pull image action.
     */
    $(".btn-primary").click(function() {
        var imageName = $(this).closest('tr').find('td:first').text();
        
        showSpinner(this);

        $.ajax({
            type: 'POST',
            url: '/image/pull',
            data: { 'image_name': imageName },
            success: (response) => {
                hideSpinner(this);
                alert(response.message);
            },
            error: () => {
                hideSpinner(this);
                alert('An error occurred while trying to pull the image.');
            }
        });
    });

    /**
     * Handles the delete containers for a specific image action.
     */
    $('.delete-containers').click(function() {
        let imageId = $(this).data('id');
        
        showSpinner(this);

        $.ajax({
            type: 'POST',
            url: '/image/delete-containers',
            data: {'image_id': imageId},
            success: (data) => {
                hideSpinner(this);
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    location.reload();
                }
            },
            error: () => {
                hideSpinner(this);
                alert('An error occurred. Please try again.');
            }
        });
    });
});
