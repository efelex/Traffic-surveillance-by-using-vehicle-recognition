import requests


def send_sms(user_code, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Confirm pin to verify account - {user_code}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    # print(r.json(), r.status_code)


def send_pin(user_code, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Confirm pin to verify account - {user_code}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
