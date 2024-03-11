// Add a listener to each PayPal button row to handle form validation before proceeding with the payment
document.querySelectorAll('.paypal-button-row').forEach(function(buttonRow) {
    buttonRow.addEventListener('click', function() {
        if (document.getElementById('quantity').value === '0') {
            alert('Please select a quantity before proceeding with the payment');
        } else {
            document.getElementById('buy-tickets-form').submit();
        }
    });
});


