import string
import random
from datetime import datetime


MailList = ['naver.com', 'gmail.com', 'hongik.ac.kr', 'hanmail.net']

class makeRandomString:
    """ Random 스트링 생성"""
#    def __init__(self):

def makeString():
    result = ""
    result += random.choice(string.ascii_uppercase)
    string_pool = string.ascii_letters + string.digits
    for i in range(1, random.randint(5, 10)):
        result += random.choice(string_pool)

    return result

def makeEmail(string = 'abc'):
    string += f"@{random.choice(MailList)}"

    return string

def makeDate():
    today_year = datetime.today().strftime('%Y')

    Year = f"{random.randint(1900, int(today_year))}"
    Month = f"{random.randint(1, 12)}"
    Day = f"{random.randint(1,30)}"
    DATE = Year + '-' + Month + '-' + Day

    return DATE

def makePhonenum():
    phonenum = f"010"
    for i in range(0,2):
        phonenum += f"-{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"

    return phonenum


print(makeEmail('abdd'))

if __name__ == '__main__':
    dbu = makeRandomString()
