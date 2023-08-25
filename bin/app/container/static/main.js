window.onload = function() {
    var containerId = window.location.pathname.split('/')[2];
    var currentStatus = "";

    // Update container details from the API
    function updateContainer() {
        $.get('/container/' + containerId + '/details_api', function(data) {
            $('#container-name').text('Name: ' + data.name);
            $('#container-status').text(data.status);
            if (data.status.includes("running")) {
                $('#container-status').removeClass('text-danger').addClass('text-success');
            } else {
                $('#container-status').removeClass('text-success').addClass('text-danger');
            }
            $('#container-image').text('Image: ' + data.image);
            $('#container-command').text('Command: ' + data.command);
            $('#container-created').text('Created: ' + new Date(data.created));
            $('#container-id').text('ID: ' + data.id);
            $('#container-networks').text(data.networks ?? "N/A");
            $('#container-mounts').text(data.mounts ?? "N/A");
            $('#container-ports').text(data.ports ?? "N/A");
            $('#container-environment').text(data.environment ?? "N/A");

            if (data.status === currentStatus) {
                $('#loading-overlay').hide();
                $('#loading-spinner').hide();
            }
            currentStatus = data.status;

        }).fail(function() {
            $('#loading-overlay').hide();
            $('#loading-spinner').hide();
        });
    }

    // Container actions
    function bindContainerActions() {
        $('#start-button').click(function() {
            $('#loading-spinner').show();
            $.post('/container/' + containerId + '/start', function() {
                updateContainer();
                $('#loading-spinner').hide();
            });
        });

        $('#stop-button').click(function() {
            $('#loading-spinner').show();
            $.post('/container/' + containerId + '/stop', function() {
                updateContainer();
                $('#loading-spinner').hide();
            });
        });

        $('#remove-button').click(function() {
            $('#loading-spinner').show();
            $.post('/container/' + containerId + '/remove', function() {
                window.location.href = '/home';
            });
        });

        $('#restart-button').click(function() {
            $('#loading-spinner').show();
            $.post('/container/' + containerId + '/restart', function() {
                updateContainer();
            });
        });
    }

    // Modal actions
    function bindModalActions() {
        $('#logs-button').click(function() {
            $.get('/container/' + containerId + '/logs', function(data) {
                $('#logs-content').text(data.logs);
                $('#logs-modal').modal('show');
            });
        });

        $('#stats-button').click(function() {
            $.get('/container/' + containerId + '/stats', function(data) {
                $('#stats-content').text(JSON.stringify(data.stats, null, 2));
                $('#stats-modal').modal('show');
            });
        });

        $('#exec-button').click(function() {
            $('#exec-modal').modal('show');
        });

        $('#exec-form').submit(function(e) {
            e.preventDefault();
            var command = $('#command').val();
            $.post('/container/' + containerId + '/exec', { command: command }, function(data) {
                $('#exec-output').text(data);
            });
        });

        $('#inspect-button').click(function() {
            $.get('/container/' + containerId + '/inspect', function(data) {
                $('#inspect-output').text(JSON.stringify(data, null, 2));
                $('#inspect-modal').modal('show');
            });
        });

        $('#copy-button').click(function() {
            $('#copy-modal').modal('show');
        });

        $('#copy-form').submit(function(e) {
            e.preventDefault();
            var src_path = $('#src_path').val();
            $.post('/container/' + containerId + '/copy', { src_path: src_path }, function(data) {
                alert(data.message);
            });
        });
    }

    // Initial call to update container details
    updateContainer();

    // Bind actions to buttons and forms
    bindContainerActions();
    bindModalActions();

    // Refresh container details every 15 seconds
    setInterval(updateContainer, 15000);
};
