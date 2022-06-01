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


def send_sms_status(status, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Your request as traffic police is  - {status}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    # print(r.json(), r.status_code)


#  charged phase ========================== section ========================

def send_charged_sms(name, amount, date, status, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Hello {name}  \n  your car is been charged {amount} for {status} \n the deadline to pay this charged is on {date} \n have good time !!!',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    # print(r.json(), r.status_code)