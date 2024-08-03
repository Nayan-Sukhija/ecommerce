from datetime import datetime
import random


def generate_order_no():
    ran = random.randint(a=0, b=99999)
    return str(datetime.today()).split()[0].replace('-', '')+str(ran)

