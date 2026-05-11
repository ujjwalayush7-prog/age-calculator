from flask import Flask, render_template, request
from datetime import date
import calendar

app = Flask(__name__)


ZODIAC_SIGNS = [
    ((1, 20), "Capricorn ♑"),
    ((2, 19), "Aquarius ♒"),
    ((3, 21), "Pisces ♓"),
    ((4, 20), "Aries ♈"),
    ((5, 21), "Taurus ♉"),
    ((6, 21), "Gemini ♊"),
    ((7, 23), "Cancer ♋"),
    ((8, 23), "Leo ♌"),
    ((9, 23), "Virgo ♍"),
    ((10, 23), "Libra ♎"),
    ((11, 22), "Scorpio ♏"),
    ((12, 22), "Sagittarius ♐"),
    ((12, 32), "Capricorn ♑")
]


def get_zodiac_sign(month, day):
    for (m, d), sign in ZODIAC_SIGNS:
        if (month, day) < (m, d):
            return sign
        
def calculate_age(birth_date):
    today = date.today()

    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        months -= 1

        previous_month = today.month - 1 or 12
        days += calendar.monthrange(today.year, previous_month)[1]

    if months < 0:
        years -= 1
        months += 12

    return years, months, days


def next_birthday_countdown(birth_date):
    today = date.today()

    next_birthday = date(today.year, birth_date.month, birth_date.day)

    if next_birthday < today:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)

    remaining_days = (next_birthday - today).days

    return remaining_days

@app.route('/', methods=['GET', 'POST'])
def index():

    result = None
    error = None

    if request.method == 'POST':

        try:
            year = int(request.form['year'])
            month = int(request.form['month'])
            day = int(request.form['day'])

            birth_date = date(year, month, day)

            if birth_date > date.today():
                error = 'Birth date cannot be in the future!'

            else:
                years, months, days = calculate_age(birth_date)

                total_days_alive = (date.today() - birth_date).days

                zodiac = get_zodiac_sign(month, day)

                birthday_countdown = next_birthday_countdown(birth_date)

                result = {
                    'years': years,
                    'months': months,
                    'days': days,
                    'total_days_alive': total_days_alive,
                    'zodiac': zodiac,
                    'birthday_countdown': birthday_countdown
                }

        except ValueError:
            error = 'Please enter a valid date!'

    return render_template(
        'index.html',
        result=result,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
