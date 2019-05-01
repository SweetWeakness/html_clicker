from flask import Flask, render_template, request

app = Flask(__name__)
clicks = 0
buy = [0, 0]


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
def index():
    return render_template('index.html', item=0)


@app.route('/clicker', methods=['GET', 'POST'])
def clicker():
    global clicks
    if request.method == "POST":
        clicks += 1 + 0.1 * buy[0] + buy[1]
        return render_template('index.html', item=round(clicks, 2))
    else:
        return render_template('index.html')


@app.route('/buy1', methods=['GET', 'POST'])
def buy1():
    global buy, clicks
    if clicks >= 20:
        buy[0] += 1
        clicks -= 20
    return render_template('index.html', item=round(clicks, 2))


@app.route('/buy2', methods=['GET', 'POST'])
def buy2():
    global buy, clicks
    if clicks >= 120:
        buy[1] += 1
        clicks -= 120
    return render_template('index.html', item=round(clicks, 2))


if __name__ == '__main__':
    app.run()
