$(document).ready(function() {
    var currentStep = 1;
    var totalSteps = 5;

    function showStep(step) {
        $('.step').hide();  
        $('#step' + step).show();  

        if (currentStep === totalSteps) {
            $('#val-bt').prop('value', 'Create')
            $('#val-bt').prop('class', 'btn btn-success')
            $('#back-button').show();  
        } else {
            $('#val-bt').prop('value', 'next')
            $('#val-bt').prop('class', 'btn btn-primary')
            if (currentStep > 1) {
                $('#back-button').show();  
            } else {
                $('#back-button').hide();  
            }
        }
    }

    function showSpinner() {
        $('#loading-spinner').show();
    }

    function hideSpinner() {
        $('#loading-spinner').hide();
    }

    showStep(currentStep);

    $('#next-button').click(function(e) {
        e.preventDefault();

        if (currentStep < totalSteps) {  
            currentStep++;
            showStep(currentStep);
        } 
    });

    $('#back-button').click(function(e) {
        e.preventDefault();

        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });

    $('#create-form').submit(function(e) {
        e.preventDefault();

        if (currentStep < 5) {  
            currentStep++;
            showStep(currentStep);
        } else {
           
            var formData = {
                'image': $('#image-selector').val(),
                'env_vars': $('input[name=env_vars]').val(),
                'volumes': $('input[name=volumes]').val(),
                'ports': $('input[name=ports]').val(),
                'links': $('input[name=links]').val(),
                'mem_limit': $('input[name=mem_limit]').val(),
                'name': $('input[name=name]').val()
            };

            showSpinner();
            

            $.ajax({
                type: 'POST',
                url: '/create',
                data: formData,
                dataType: 'json',
                encode: true
            }).done(function(data) {
                hideSpinner();

                if (data.error) {
                    $('#error-message').text(data.error);
                } else {
                    window.location.href = '/container/' + data.id;
                }
            }).fail(function(data) {
                hideSpinner();
                $('#error-message').text('An error occurred while trying to create the container.');
            });
        }
    });
});
