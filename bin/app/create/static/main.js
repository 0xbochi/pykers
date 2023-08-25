$(document).ready(function() {
    var currentStep = 1;
    var totalSteps = 6;

    // Show the current step and update the buttons accordingly
    function showStep(step) {
        $('.step').hide();
        $('#step' + step).show();

        if (currentStep === totalSteps) {
            $('#val-bt').prop('value', 'Create').prop('class', 'btn btn-success');
            $('#back-button').show();
        } else {
            $('#val-bt').prop('value', 'Next').prop('class', 'btn btn-primary');
            $('#back-button').toggle(currentStep > 1);
        }
    }

    // Show and hide loading spinner
    function showSpinner() {
        $('#loading-spinner').show();
    }

    function hideSpinner() {
        $('#loading-spinner').hide();
    }

    // Initial display of the current step
    showStep(currentStep);

    // Handle next button click
    $('#next-button').click(function(e) {
        e.preventDefault();

        if (currentStep < totalSteps) {
            currentStep++;
            showStep(currentStep);
        }
    });

    // Handle back button click
    $('#back-button').click(function(e) {
        e.preventDefault();
        $('#alert-container').hide();

        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });
    $('#image-selector').on('input', function() {
        if ($(this).val()) {
            $('#val-bt').prop('disabled', false);
        } else {
            $('#val-bt').prop('disabled', true);
        }
    });

    // Handle form submission
    $('#create-form').submit(function(e) {
        e.preventDefault();
    
        if (currentStep === 1) {
            // Show the loading spinner
            $('#val-bt').hide();
            showSpinner();
            $('#alert-container').text('').hide();
    
            // Check the image
            var image = $('#image-selector').val();
            $.post('/create/check_image', { image_name: image }, function(response) {
                if (response.status === 'success') {
                    hideSpinner();
                    $('#val-bt').show();
    
                    currentStep++;
                    showStep(currentStep);
                } else {
                    hideSpinner();
                    $('#val-bt').show();
                    $('#alert-container').text(response.message).show();
                }
            });
        } else if (currentStep < totalSteps) {
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
                'name': $('input[name=name]').val(),
                'initial_command': $('input[name=initial-command]').val()
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
                    $('#alert-container').text(data.error).show();
                } else {
                    window.location.href = '/container/' + data.id;
                }
            }).fail(function() {
                hideSpinner();
                $('#alert-container').text('An error occurred while trying to create the container.').show();
            });
        }
    });
    
});
