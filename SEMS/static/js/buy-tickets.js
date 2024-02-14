function nextStep() {
    var quantity = document.getElementById('id_ticket_quantity').value;
    var paymentMethod = document.getElementById('id_payment_method').value;
    if (quantity && paymentMethod) {
        document.getElementById('step-1').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'block';

        if (paymentMethod === 'qr') {
            document.getElementById('step-2-qr').style.display = 'block';
        } else if (paymentMethod === 'card') {
            document.getElementById('step-2-card').style.display = 'block';
        }
    }else{
        alert('Please select the quantity and payment method');
    }
}

