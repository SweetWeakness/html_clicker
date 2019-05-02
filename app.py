from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)
clicks = 0
buy = [0, 0]
stat = 0


def buy1():
    global buy
    if clicks >= 20:
        buy[0] += 1
        clicks -= 20


def buy2():
    global buy
    if clicks >= 120:
        buy[1] += 1
        clicks -= 120


@app.route('/')
@app.route('/login')
def hello():
    return render_template('hello.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    global clicks, stat, buy
    speed = 1 + 0.1 * buy[0] + buy[1]
    data = request.args
    print(*data)
    return render_template('index.html',
                           item="{} clicks".format(round(clicks, 2)),
                           speed=speed, stat=stat)


@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    global clicks, buy, stat
    speed = 1 + 0.1 * buy[0] + buy[1]
    if request.method == "POST":
        clicks += 1 + 0.1 * buy[0] + buy[1]
        stat += 1
        return render_template('index.html', item="{} clicks".format(round(clicks, 2)), speed=speed, stat=stat)
    else:
        return render_template('index.html')


@app.route('/buy1', methods=['GET', 'POST'])
def buy1():
    global buy, clicks, stat
    speed = 1 + 0.1 * buy[0] + buy[1]
    item = "Not enough clicks (You have {})".format(round(clicks, 2))
    message = "Nice! You bought +0.1 perfomance"
    if clicks >= 20:
        buy[0] += 1
        clicks -= 20
        speed += 0.1
    else:
        return render_template('index.html', item=item, speed=speed, stat=stat)

    return render_template('index.html', item=round(clicks, 2), message=message, speed=speed, stat=stat)


@app.route('/buy2', methods=['GET', 'POST'])
def buy2():
    global buy, clicks, stat
    speed = 1 + 0.1 * buy[0] + buy[1]
    item = "Not enough clicks (You have {})".format(round(clicks, 2))
    message = "Nice! You bought +1 perfomance"
    if clicks >= 120:
        buy[1] += 1
        clicks -= 120
        speed += 1
    else:
        return render_template('index.html', item=item, speed=speed, stat=stat)
    return render_template('index.html', item=round(clicks, 2), message=message, speed=speed, stat=stat)


if __name__ == '__main__':
    app.run()
