import functools

from flask import (
    Blueprint, jsonify, g, flash, redirect, render_template, request, session, url_for
    )
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from flight_application.db import get_db

user_bp = Blueprint('users', __name__, url_prefix='/users')


@user_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        role = data.get('role', 'user')

        if not data.get('username') or not data.get('password'):
            flash('Username and password are required', 'error')
            return render_template('register.html'), 400

        hashed_password = generate_password_hash(password)
        db = get_db()

        try:

            user = db.execute('SELECT id FROM Users WHERE username = ?',(username,)).fetchone()

            if user is not None:
                flash(f'User {username} is already registered.', 'error')
                return render_template('register.html'), 400

            db.execute(
                'INSERT INTO Users (username, password, role) VALUES (?, ?, ?)',
                (username, hashed_password, role)
                )
            db.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            print(f'An error occurred: {e}')
            flash('An unexpected error occurred. Please try again later.', 'error')
            return render_template('register.html'), 500

    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']

        if not username or not password:
            flash('Username and password are required.', 'error'), 400
            return render_template('login.html')

        db = get_db()
        cursor = db.cursor()
        
        user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()

        cursor.close()


        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            
            if user['role'] == 'admin':
                return render_template('admin_dashboard.html')

            else:
                return render_template('user_dashboard.html')
        else:
            flash('Invalid username or password')
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@user_bp.route('/book_flight', methods=['GET', 'POST'])
def book_flight():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        flight_number = request.form.get('flight_number')

        if not first_name or not last_name or not email or not flight_number:
            flash('Missing required field', 'error')
            return render_template('book_flight.html'), 400

        try:
            db = get_db()
            cursor = db.cursor()

            # Retrieve flight ID based on flight number
            cursor.execute("SELECT flight_id FROM _FLIGHT_CREAT WHERE flight_number = ?", (flight_number,))
            flight = cursor.fetchone()

            if not flight:
                flash('Flight number not found', 'error')
                return render_template('book_flight.html'), 400

            flight_id = flight[0]

            # Check if passenger already exists
            cursor.execute("SELECT passenger_id FROM Passengers WHERE email = ?", (email,))
            passenger = cursor.fetchone()

            if passenger:
                passenger_id = passenger[0]
            else:
                # Insert new passenger and retrieve their ID
                cursor.execute(
                    "INSERT INTO Passengers (first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?)",
                    (first_name, last_name, email, phone_number)
                )
                passenger_id = cursor.lastrowid

            # Insert booking
            booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = 'Confirmed'
            cursor.execute(
                "INSERT INTO Bookings (flight_id, passenger_id, booking_time, status) VALUES (?, ?, ?, ?)",
                (flight_id, passenger_id, booking_time, status)
            )

            db.commit()
            flash('Booking successful', 'success')
            return render_template('book_flight.html'), 200

        except Exception as e:
            error = f"An error occurred: {str(e)}"
            flash(error, 'error')
            return render_template('book_flight.html'), 500

        finally:
            cursor.close()
            db.close()
    return render_template('book_flight.html')
