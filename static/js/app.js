// Activate Featericons
feather.replace();

// Account Deletion Confirmation
var delBtn = document.getElementById('deleteAccountBtn');
if (delBtn != null) {
    delBtn.addEventListener('click', () => {
        var userChoice = confirm('Are you sure you want to delete your account?');
        if (userChoice) {
            fetch('/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
                .then(res => console.error(res))
                .catch(err => console.error(err));
        }
    });
}