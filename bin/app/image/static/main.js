$(document).ready(function() {
    $('.delete-image').click(function() {
        let imageId = $(this).data('id');
        $.ajax({
            type: 'POST',
            url: '/image/delete',
            data: {'image_id': imageId},
            success: function(data) {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    location.reload();
                }
            },
            error: function() {
                alert('An error occurred. Please try again.');
            }
        });
    });

    $(".btn-primary").click(function() {
        var imageName = $(this).closest('tr').find('td:first').text();
        $.ajax({
            type: 'POST',
            url: '/image/pull',
            data: { 'image_name': imageName },
            success: function(response) {
                alert(response.message);
            }
        });
    });


});
