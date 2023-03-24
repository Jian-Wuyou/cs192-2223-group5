(() => {
    document.getElementsByTagName('form')[0].addEventListener('submit', async (event) => {
        event.preventDefault();

        // Get username and password
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Check if either field is empty
        if (username.length === 0 || password.length === 0) {
            alert('Please fill in both fields');
            return;
        }

        // Encrypt credentials
        const credentials = `${username}:${password}`;

        // Transmit encrypted credentials to server via POST
        const r = await fetch('/link/uvle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                credentials: credentials,
            }),
        });

        const data = await r.json();

        if (data['success']) {
            window.location.href = '/dashboard';
        } else {
            alert(data['error']);
        }
    });
})();