import matplotlib.ticker as ticker
from matplotlib import pyplot as plt
import statistics
import sqlite3


def lineplot(x_data, y_data, x_label="", y_label="", title="",
             x_major=30, x_minor=7, y_major=5, y_minor=1):
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data, lw=2, color='#539caf', alpha=1)

    # Label the axes and provide a title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    #  Устанавливаем интервал основных и
    #  вспомогательных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_major))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(x_minor))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(y_major))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(y_minor))

    #  Добавляем линии основной сетки:
    ax.grid(which='major',
            color='black')

    #  Включаем видимость вспомогательных делений:
    ax.minorticks_on()
    #  Теперь можем отдельно задавать внешний вид
    #  вспомогательной сетки:
    ax.grid(which='minor',
            color='gray',
            linestyle=':')


def median(year):
    con = sqlite3.connect("data/base.db")
    cur = con.cursor()
    temps = cur.execute(f"SELECT t FROM data WHERE year = {year}").fetchall()
    temps = [el[0] for el in temps]
    medians = []
    for i in range(1, len(temps)):
        medians.append(statistics.median(temps[:i]))

    plt.plot(range(1, 365), medians)
    plt.savefig('medians.png')


def years_median():
    con = sqlite3.connect("data/base.db")
    cur = con.cursor()
    medians = []
    for i in range(1,21):
        temps = cur.execute(f"SELECT t FROM data WHERE year = {i}").fetchall()
        temps = [el[0] for el in temps]
        medians.append(statistics.median(temps))

    lineplot(range(1, 21), medians, title='Изменение медианы в одном городе')
    plt.savefig('year_median.png')


def draw_plot(temps):
    lineplot(range(1, len(temps) + 1), temps, x_label='дни недели',
             y_label='температуры', title='Динамика температуры за неделю')
    plt.savefig('static/week.png')


def draw_plot_month(temps):
    lineplot(range(1, len(temps) + 1), temps, x_label='дни недели',
             y_label='температуры', title='Динамика температуры за месяц')
    plt.savefig('static/week.png')


# with open('data/Portovyi_774_Clear.json') as data:
#     data = json.load(data)
#
# lineplot(range(365), data[:365], 'дни', 'температура', 'aaaaaaaa')

# for i in range(1, 21):
#     median(i)
# plt.legend(list(range(1, 21)))
# plt.show()

# years_median()
# plt.show()
