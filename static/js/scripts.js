document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault(); // Зупиняє перезавантаження
    
    fetch(this.action, {
        method: 'POST',
        body: new FormData(this),
    }).then(response => {
        if (response.ok) {
            document.getElementById("button-like-mater").classList.toggle("active");
        }
    });
});


