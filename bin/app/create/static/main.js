$(document).ready(function() {
    var currentStep = 1;

    function showStep(step) {
        $('.step').hide();  
        $('#step' + step).show();  
    }


    showStep(currentStep);

    $('#create-form').submit(function(e) {
        e.preventDefault();

        if (currentStep < 5) {  
            currentStep++;
            showStep(currentStep);
        } else {
           
            var formData = {
                'image': $('input[name=image]').val(),
                'env_vars': $('input[name=env_vars]').val(),
                'volumes': $('input[name=volumes]').val(),
                'ports': $('input[name=ports]').val(),
                'links': $('input[name=links]').val(),
                'mem_limit': $('input[name=mem_limit]').val(),
                'name': $('input[name=name]').val()
            };


            $.ajax({
                type: 'POST',
                url: '/create',
                data: formData,
                dataType: 'json',
                encode: true
            }).done(function(data) {

                if (data.error) {
 
                    $('#error-message').text(data.error);
                } else {
 
                    window.location.href = '/container/' + data.id;
                }
            }).fail(function(data) {

                $('#error-message').text('An error occurred while trying to create the container.');
            });
        }
    });
});
