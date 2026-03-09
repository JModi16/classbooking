#!/usr/bin/env python
import os
import sys

# Load env.py
if os.path.isfile('env.py'):
    exec(open('env.py').read())

import stripe

sk = os.environ.get('STRIPE_SECRET_KEY')
pk = os.environ.get('STRIPE_PUBLIC_KEY')

print(f"Secret Key: {sk}")
print(f"Secret Key Length: {len(sk) if sk else 0}")
print(f"Public Key: {pk}")
print(f"Public Key Length: {len(pk) if pk else 0}")

if sk:
    stripe.api_key = sk
    try:
        pi = stripe.PaymentIntent.create(amount=1999, currency='gbp')
        print(f"✅ Stripe API works! Created PI: {pi.id}")
    except Exception as e:
        print(f"❌ Stripe Error: {type(e).__name__}: {str(e)}")
else:
    print("❌ No Stripe Secret Key found!")
