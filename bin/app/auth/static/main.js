$(document).ready(function() {
    $('#add-user-form').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/auth/user/new',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                location.reload();
            }
        });
    });

    $('#reset-password-form').on('submit', function(e) {
        e.preventDefault();

        const newPassword = $('[name="new_password"]').val();
        const confirmPassword = $('[name="confirm_password"]').val();

        if (newPassword !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        $.ajax({
            url: '/auth/resetpasswd',
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if(response.startsWith('Passwords do not match')) {
                    alert(response);
                } else {
                    alert('Password updated successfully');
                    window.location.href = '/auth/users';
                }
            },
            error: function(response) {
                alert('An error occurred: ' + response.responseText);
            }
        });
    });
});

function resetPassword(username) {
    window.location.href = '/auth/resetpasswd?username=' + username;
}

function deleteUser(username) {
    if (confirm('Are you sure you want to delete this user?')) {
        $.ajax({
            url: '/auth/user/delete',
            method: 'POST',
            data: { username: username },
            success: function(response) {
                location.reload();
            }
        });
    }
}
