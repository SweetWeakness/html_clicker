from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)
clicks = 0
buy = [0, 0]
stat = 0
text = "sad"


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    global clicks, stat, buy, text

    text = request.form['text']
    print(text)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute('''
    SELECT count(name1) FROM users 
    WHERE name1 = '%(txt)s' ''' % {"txt": text})
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute('''
        INSERT INTO users (name1, buy1, buy2, clicks, stat1)
         values (?,?,?,?,?)''', [text, 0, 0, 0, 0])
        conn.commit()
        print('new guy!')
    else:
        cur.execute('''
            SELECT users.buy1, users.buy2, clicks, users.stat1 FROM users
            WHERE name1 = '%(txt)s' ''' % {"txt": text})

        for row in cur:
            buy_1, buy_2, clicks, stat = row
            buy[0], buy[1], clicks, stat = buy_1, buy_2, clicks, stat
        print('old guy!')
    conn.close()
    speed = 1 + 0.1 * buy[0] + buy[1]
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
        return render_template('index.html', item="{} clicks".format(round(clicks, 2)),
                               speed=speed, stat=stat)
    else:
        return render_template('index.html')


@app.route('/savepoint', methods=['GET', 'POST'])
def savepoint():
    global clicks, buy, stat
    speed = 1 + 0.1 * buy[0] + buy[1]
    if request.method == "POST":
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute('''
        UPDATE users set
        buy1 = '%(one)s', buy2 = '%(two)s', clicks = '%(clk)s', stat1 = '%(st)s'
        WHERE name1 = '%(txt)s' ''' % {"one": buy[0], "two": buy[1], "clk": clicks, "st": stat, "txt": text})
        conn.commit()
        conn.close()
    return render_template('index.html', item="{} clicks".format(round(clicks, 2)),
                           speed=speed, stat=stat)

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
