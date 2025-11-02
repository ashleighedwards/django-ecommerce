document.addEventListener('DOMContentLoaded', function() {
    if (typeof stripePublicKey === 'undefined') {
        console.error('Stripe public key not defined!');
        return;
    }

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    const messageDiv = document.getElementById('payment-message');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) throw new Error('Server error');

            const data = await response.json();

            // Confirm card payment
            const result = await stripe.confirmCardPayment(data.client_secret, {
                payment_method: { card: card }
            });

            if (result.error) {
                messageDiv.textContent = result.error.message;
            } else if (result.paymentIntent.status === 'succeeded') {
                window.location.href = '/cart/payment-success/';
            }
        } catch (err) {
            messageDiv.textContent = 'An error occurred. Please try again.';
            console.error(err);
        }
    });
});