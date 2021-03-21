from flask import Flask, render_template, redirect
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tenet'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/forecastForDay', methods=['GET', 'POST'])
def SDF():
    form = AskDayForm()
    if form.validate_on_submit():
        day = form.day.data
        city = form.city.data
        print(type(day))

        #cursor.execute("INSERT INTO schedule VALUES(%s, %s, %s, %s, %s, %s, %s)",
         #              (lastID + 1, classroom, start_time, end_time, description, form.choices.data[0], number,))
        #connection.commit()
        #cursor.close()
        return redirect('/')
    # TODO: ловим ошибки числа города
    return render_template('forecastForDay.html', title='Прогноз на определенный день', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')