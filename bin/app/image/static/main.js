$(document).ready(function() {
    function showSpinner(button) {
        $(button).siblings('.spinner-border').show();
    }

    function hideSpinner(button) {
        $(button).siblings('.spinner-border').hide();
    }

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
