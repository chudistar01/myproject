from functools import wraps

from flask import (
    Blueprint, flash, jsonify, g, redirect, render_template, request, session, url_for
    )
from werkzeug.security import check_password_hash, generate_password_hash

from flight_application.db import get_db

from datetime import datetime


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admins')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or session.get('role') != 'admin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/create_flight', methods=['GET', 'POST'])
@admin_required
def create_flight():
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        price = request.form['price']
        available_seats = request.form['available_seats']

        db = get_db()

        try:
            departure_time = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M')
            arrival_time = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            error="Invalid datetime format. Use 'YYYY-MM-DDTHH:MM'"
            return render_template('create_flight.html', error=error)

        try:
            cursor = db.cursor()
            cursor.execute(
            """
            INSERT INTO _fLIGHT_CREAT (
                flight_number,
                departure_airport,
                arrival_airport,
                departure_time,
                arrival_time,
                price,
                available_seats
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                flight_number,
                departure_airport,
                arrival_airport,
                departure_time,
                arrival_time,
                price,
                available_seats)
            )
            db.commit()
            flight_name = cursor.lastrowid
            success = f"Flight with flight name: {flight_number} created successfully"
            return render_template('create_flight.html', success=success)
        finally:
            db.close()

    return render_template('create_flight.html')

@admin_bp.route('/delete_flight_form', methods=['GET'])
@admin_required
def delete_flight_form():
    return render_template('delete_flight_form.html')


@admin_bp.route('/delete_flight', methods=['POST'])
@admin_required
def delete_flight():
    flight_number = request.form.get('flight_number')

    if not flight_number:
        flash('Flight number is required', 'error')
        return redirect(url_for('admin_bp.delete_flight_form'))

    db = get_db()
    cursor = db.cursor()


    cursor.execute('SELECT * FROM _FLIGHT_CREAT WHERE flight_number = ?', (flight_number,))
    flight = cursor.fetchone()

    if flight is None:
        flash('Flight not found', 'error')
        db.close()
        return redirect(url_for('admin_bp.delete_flight_form'))

    cursor.execute("DELETE FROM _FLIGHT_CREAT  WHERE flight_number = ?", (flight_number,))
    db.commit()
    db.close()

    flash('Flight deleted successfully!')
    return redirect(url_for('admin_bp.delete_flight_form'))
