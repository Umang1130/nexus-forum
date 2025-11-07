from flask import Flask, render_template, request, url_for, redirect, session, flash
import sqlite3
import os

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/static')
app.secret_key = os.urandom(24)  # Required for session management

@app.route('/')
def home():
    return render_template('index.html', current_user=session.get('user'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""insert into users(name, email, password) values(?,?,?)""", (name, email, password))
                conn.commit()
                flash('You have successfully signed up!')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            print(f"An error occurred : {e}")

    return render_template('sign-in.html', current_user=session.get('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("""select * from users where email = ? and password = ?""", (email, password))
                user = cursor.fetchone()

                if user:
                    session['user'] = {'name': user[1], 'email': user[2]}
                    return redirect(url_for('home'))
                else:
                    flash('Invalid email or password')
                    return redirect(url_for('login'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('login'))

    return render_template('login.html', logged_in='user' in session)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/clubs')
def clubs():
    return render_template('clubs.html', current_user=session.get('user'))

@app.route('/events')
def events():
    return render_template('events.html', current_user=session.get('user'))

@app.route('/committee')
def committee():
    return render_template('committee.html', current_user=session.get('user'))

@app.route('/faculty')
def faculty():
    return render_template('faculty.html', current_user=session.get('user'))

@app.route('/dsi')
def dsi():
    return render_template('dsi.html', current_user=session.get('user'))

@app.route('/cc')
def cc():
    return render_template('cc.html', current_user=session.get('user'))

@app.route('/webnest')
def webnest():
    return render_template('webnest.html', current_user=session.get('user'))

if __name__ == '__main__':
    app.run(debug=True)