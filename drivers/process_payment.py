import requests, math, random
from django.urls import reverse
from django.shortcuts import redirect


def process_payment(phone_number, full_name, charged_id, amount, current_site):
    hed = {'Authorization': 'Bearer ' + 'FLWSECK_TEST-b967a404c4b9abffbbd0edc04aaacda4-X'}
    redirect_url = reverse('payment_insurance_completed', kwargs={'charged_id': charged_id, 'amount': amount})
    absurl = 'http://' + current_site + redirect_url
    print("url---------------------", absurl)
    data = {
        "tx_ref": str(math.floor(1000000 + random.random() * 9000000)),
        # "tx_ref": "MC-158523s09v5050e88",
        "amount": str(amount),
        "currency": "RWF",
        "payment_options": "mobiremoneyrwanda",
        "redirect_url": absurl,
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": "byiringoroscar@gmail.com",
            "phone_number": str(phone_number),
            "fullname": str(full_name),
        },
        "customizations": {
            "title": "Traffic police",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
        }
    }
    url = 'https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response = response.json()
    print("======================  response ================", response)
    link = response['data']['link']
    return link


