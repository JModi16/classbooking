/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/
/* global Stripe */

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripeInstance = Stripe(stripePublicKey);
var elements = stripeInstance.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var cardNumber = null;
var cardExpiry = null;
var cardCvc = null;
var card = null;
var primaryCardElement = null;

if (document.getElementById('card-number-element') && document.getElementById('card-expiry-element') && document.getElementById('card-cvc-element')) {
    cardNumber = elements.create('cardNumber', {
        style: style,
        showIcon: true,
    });
    cardExpiry = elements.create('cardExpiry', {style: style});
    cardCvc = elements.create('cardCvc', {style: style});

    cardNumber.mount('#card-number-element');
    cardExpiry.mount('#card-expiry-element');
    cardCvc.mount('#card-cvc-element');
    primaryCardElement = cardNumber;
} else if (document.getElementById('card-element')) {
    card = elements.create('card', {style: style});
    card.mount('#card-element');
    primaryCardElement = card;
}

if (!primaryCardElement) {
    var errorDivNoCard = document.getElementById('card-errors');
    if (errorDivNoCard) {
        errorDivNoCard.textContent = 'Payment form could not load. Please refresh and try again.';
    }
}

function toggleCardInputs(disabled) {
    if (cardNumber && cardExpiry && cardCvc) {
        cardNumber.update({'disabled': disabled});
        cardExpiry.update({'disabled': disabled});
        cardCvc.update({'disabled': disabled});
        return;
    }
    if (card) {
        card.update({'disabled': disabled});
    }
}

function handleStripeChange(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
}

if (cardNumber && cardExpiry && cardCvc) {
    cardNumber.addEventListener('change', handleStripeChange);
    cardExpiry.addEventListener('change', handleStripeChange);
    cardCvc.addEventListener('change', handleStripeChange);
} else if (card) {
    card.addEventListener('change', handleStripeChange);
}

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    if (!primaryCardElement) {
        var errorDivMissing = document.getElementById('card-errors');
        if (errorDivMissing) {
            errorDivMissing.textContent = 'Payment form could not load. Please refresh and try again.';
        }
        return;
    }
    toggleCardInputs(true);
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
        stripeInstance.confirmCardPayment(clientSecret, {
            payment_method: {
                card: primaryCardElement,
            }
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                toggleCardInputs(false);
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    });
});
