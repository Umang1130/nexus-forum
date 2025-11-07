from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
                conn.commit()
            return redirect(url_for('home'))
        except sqlite3.Error as e:
            return f"An error occurred: {e}"

    return render_template('sign-in.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
                user = cursor.fetchone()
                if user:
                    return redirect(url_for('index'))
                else:
                    return "Invalid credentials"
        except sqlite3.Error as e:
            return f"An error occurred: {e}"

    return render_template('login.html')


@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/clubs')
def clubs():
    return render_template('clubs.html')

@app.route('/committee')
def committee():
    return render_template('committee.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/dsi')
def dsi():
    return render_template('dsi.html')

@app.route('/cc')
def cc():
    return render_template('cc.html')

if __name__ == '__main__':
    app.run(debug=True)