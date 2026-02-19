// Basic script to handle UI interactions
document.addEventListener('DOMContentLoaded', function() {
    console.log("Velocify Static Assets Loaded!");
    
    // Auto-hide alerts after 3 seconds
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.display = 'none';
        });
    }, 3000);
});