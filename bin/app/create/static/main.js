$(document).ready(function() {
    var currentStep = 1;
    var totalSteps = 6;

    // Show the current step and update the buttons accordingly

    function showStep(step) {
        $('.step').hide();
        $('#step' + step).show();
        $('#step-indicator').text(step + '/6');
    
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
        $('#alert-container').text('').hide(); // Clear any previous error messages
    
        if (currentStep === 1) {
            // Show the loading spinner
            $('#val-bt').hide();
            showSpinner();
    
            // Check the container name
            var containerName = $('input[name=name]').val();
            $.post('/create/check_container_name', { container_name: containerName }, function(nameResponse) {
                if (nameResponse.status === 'error') {
                    hideSpinner();
                    $('#val-bt').show();
                    $('#alert-container').text(nameResponse.message).show();
                    return;
                }
    
                // Check the image if container name is valid
                var image = $('#image-selector').val();
                $.post('/create/check_image', { image_name: image }, function(imageResponse) {
                    hideSpinner();
                    if (imageResponse.status === 'success') {
                        $('#val-bt').show();
                        currentStep++;
                        showStep(currentStep);
                    } else {
                        $('#val-bt').show();
                        $('#alert-container').text(imageResponse.message).show();
                    }
                });
            });
        }
        else if (currentStep === 2) {
            var env_vars = $('input[name=env_vars]').val();
            var regex = /^([A-Za-z_][A-Za-z0-9_]*=[^,]+)(,[A-Za-z_][A-Za-z0-9_]*=[^,]+)*$/;
            if (env_vars && !regex.test(env_vars)) {
                $('#alert-container').text("Invalid environment variables format. Should be in format KEY1=VALUE1,KEY2=VALUE2,...").show();
            } else {
                currentStep++;
                showStep(currentStep);
            }
        } 
        else if (currentStep === 3) {
            var volumes = $('input[name=volumes]').val();
            var regex = /^(\/[\w\-\.]+)+:(\/[\w\-\.]+)+$/;
            if (volumes && !regex.test(volumes)) {
                $('#alert-container').text("Invalid volumes format. Should be in format /host/path:/container/path").show();
            } else {
                currentStep++;
                showStep(currentStep);
            }
        } 
        else if (currentStep === 4) {
            var ports = $('input[name=ports]').val();
            var regex = /^\d+:\d+$/;
            if (ports && !regex.test(ports)) {
                $('#alert-container').text("Invalid ports format. Should be in format 80:8080").show();
            } else {
                currentStep++;
                showStep(currentStep);
            }
        } 
        else if (currentStep === 5) {
            var mem_limit = $('input[name=mem_limit]').val();
            var regex = /^(\d+m|\d+g)$/;
            if (mem_limit && !regex.test(mem_limit)) {
                $('#alert-container').text("Invalid memory limit format. Example: 512m for 512MB, 1g for 1GB, etc").show();
            } else {
                currentStep++;
                showStep(currentStep);
            }
        } 
        else if (currentStep === 6) {
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
