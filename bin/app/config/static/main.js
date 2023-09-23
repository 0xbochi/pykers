document.getElementById('ip-config-form').addEventListener('submit', function(e) {
    e.preventDefault();

    let ipAddress = document.getElementById('ip-address').value;

    if (!isValidIpCidr(ipAddress)) {
        alert('Invalid IP/CIDR');
        return;
    }

    fetch('/config/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'ip_address': ipAddress
        })
    })
    .then(response => response.text())
    .then(data => {
        location.reload();
    });
});

function isValidIpCidr(ip) {
    const ipCidrPattern = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\/([0-9]|[1-2][0-9]|3[0-2])$/;
    return ipCidrPattern.test(ip);
}

function deleteIP(ip) {
    if (!isValidIpCidr(ip)) {
        alert('Invalid IP/CIDR');
        return;
    }

    if (!confirm('Are you sure you want to delete this IP?')) {
        return;
    }

    fetch('/config/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'ip': ip
        })
    })
    .then(response => response.text())
    .then(data => {
        location.reload();
    });
}