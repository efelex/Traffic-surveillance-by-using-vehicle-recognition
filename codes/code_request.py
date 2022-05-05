import random


def request_pin():
    number_list = [x for x in range(10)]
    code_items = []
    for i in range(5):
        num = random.choice(number_list)
        code_items.append(num)
    code_string = "".join(str(item) for item in code_items)
    return code_string
