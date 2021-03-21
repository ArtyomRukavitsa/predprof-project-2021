from flask import Flask, render_template, redirect
from forms import *
import sqlite3
from graph import *
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tenet'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
DAY = 0
CITY = ""
T = 0
T_ARRAY = []
DAYS = []
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


def findT(array):
    delta_arr = []
    for i in range(0, len(array) - 1):
        delta_arr.append((array[i + 1][0] - array[i][0]) / 2.0)

    print(array)
    print(delta_arr)
    prediction = array[-1][0] + sum(delta_arr) / float(len(delta_arr))
    return prediction


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/forecastForDay', methods=['GET', 'POST'])
def forecastForDay():
    global DAY, CITY, T
    form = AskWeekForm()
    if form.validate_on_submit():
        day = form.day.data
        city = form.city.data
        print(day.day, day.month, day.year)
        con = sqlite3.connect('db/base.db', check_same_thread=False)
        cur = con.cursor()
        array = cur.execute("""SELECT t FROM data WHERE day=? AND month=?""", [day.day, day.month]).fetchall()
        T = findT(array)
        DAY = day
        CITY = cur.execute("""SELECT city FROM cities WHERE id=?""", [city]).fetchall()[0][0]
        con.commit()
        con.close()
        return redirect('/dayResult')
    # TODO: ловим ошибки числа города
    return render_template('forecastForDay.html', title='Прогноз на определенный день', form=form, word='день')


@app.route('/forecastForWeek', methods=['GET', 'POST'])
def forecastForWeek():
    global DAY, CITY, T_ARRAY
    form = AskDayForm()
    if form.validate_on_submit():
        DAYS.clear()
        T_ARRAY.clear()
        day = form.day.data
        city = form.city.data
        con = sqlite3.connect('db/base.db', check_same_thread=False)
        cur = con.cursor()
        id_ = cur.execute("""SELECT id FROM data WHERE day=? AND month=?""", [day.day, day.month]).fetchall()[0][0]
        for i in range(7):
            day = cur.execute("""SELECT day FROM data WHERE id=?""", [id_]).fetchall()[0][0]
            month = cur.execute("""SELECT month FROM data WHERE id=?""", [id_]).fetchall()[0][0]
            array = cur.execute("""SELECT t FROM data WHERE day=? AND month=?""", [day, month]).fetchall()
            DAYS.append([day, month])
            T_ARRAY.append(round(findT(array), 3))
            id_ += 1
        print(DAYS)
        #DAY = day
        CITY = cur.execute("""SELECT city FROM cities WHERE id=?""", [city]).fetchall()[0][0]
        con.commit()
        con.close()
        return redirect('/weekResult')
    # TODO: ловим ошибки числа города
    return render_template('forecastForDay.html', title='Прогноз на неделю', form=form, word='неделю')


@app.route('/forecastForMonth', methods=['GET', 'POST'])
def forecastForMonth():
    monthArr = ['январь', 'февраль', 'март', 'апрель', 'май',
                'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    dayInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    global DAY, CITY, T_ARRAY
    form = AskMonthForm()
    if form.validate_on_submit():
        DAYS.clear()
        T_ARRAY.clear()
        month = monthArr.index(form.month.data.lower()) + 1
        city = form.city.data
        con = sqlite3.connect('db/base.db', check_same_thread=False)
        cur = con.cursor()
        print(month, city)
        print(cur.execute("""SELECT id FROM data WHERE day=1 AND month=? AND id_city=?""", [month, city]).fetchall())
        id_ = cur.execute("""SELECT id FROM data WHERE day=1 AND month=? AND id_city=?""", [month, city]).fetchall()[0][0]
        for i in range(dayInMonth[month - 1]):
            day = cur.execute("""SELECT day FROM data WHERE id=?""", [id_]).fetchall()[0][0]
            month = cur.execute("""SELECT month FROM data WHERE id=?""", [id_]).fetchall()[0][0]
            array = cur.execute("""SELECT t FROM data WHERE day=? AND month=?""", [day, month]).fetchall()
            DAYS.append([day, month])
            T_ARRAY.append(round(findT(array), 3))
            id_ += 1
        print(DAYS)
        #DAY = day
        CITY = cur.execute("""SELECT city FROM cities WHERE id=?""", [city]).fetchall()[0][0]
        con.commit()
        con.close()
        return redirect('/monthResult')
    # TODO: ловим ошибки числа города
    return render_template('forecastForMonth.html', title='Прогноз на месяц', form=form, word='месяц')


@app.route('/dayResult')
def dayResult():
    return render_template('showForecastForDay.html', title='Прогноз на определенный день', city=CITY, day=DAY, t=round(T, 3))


@app.route('/weekResult')
def weekResult():
    draw_plot(T_ARRAY)
    return render_template('showForecastForMonth.html', title='Прогноз на неделю', city=CITY, day=DAYS,
                           t=T_ARRAY, length=len(DAYS))


@app.route('/monthResult')
def monthResult():
    draw_plot_month(T_ARRAY)
    return render_template('showForecastForMonth.html', title='Прогноз на месяц', city=CITY, day=DAYS,
                           t=T_ARRAY, length=len(DAYS))


@app.route('/median/<int:city>')
def median(city):
    years_median(city)
    return render_template('showMedian.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')