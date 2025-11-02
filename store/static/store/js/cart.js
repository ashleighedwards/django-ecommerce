function addToCart(productId, button) {
    fetch(`/store/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Accept': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-count').textContent = data.cart_count;

        button.textContent = "Added!";
        setTimeout(() => {
            button.textContent = "Add to Cart";
        }, 1000);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Helper function to get CSRF token from cookie
function getCSRFToken() {
    let cookieValue = null;
    let name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
