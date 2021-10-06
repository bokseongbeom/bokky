import string
import random
from datetime import datetime

class makeRandomString:
    """ Random 스트링 생성"""
#    def __init__(self):

    def makeString(self, Length = 10):
        result = ""
        result += random.choice(string.ascii_uppercase)
        string_pool = string.ascii_letters + string.digits
        for i in range(Length-1):
            result += random.choice(string_pool)

        print(result)
#    def makeEmail(self):

    def makePhonenum(self, Length = 10):
        phonenum = f"010"
        for i in range(0,2):
            phonenum += f"-{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
        print(phonenum)

    def makeDate(self, Length = 10):
        today_year = datetime.today().strftime('%Y')
        for i in range(1,100):

            Year = f"{random.randint(1900, int(today_year))}"
            Month = f"{random.randint(1, 12)}"
            Day = f"{random.randint(1,30)}"
            DATE = Year + '-' + Month + '-' + Day
            print(DATE)

if __name__ == '__main__':
    dbu = makeRandomString()
    dbu.makePhonenum()