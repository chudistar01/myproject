from flask import request, render_template, flash
from datetime import datetime
from your_app import get_db  # Import your database connection function

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
            cursor.execute("SELECT flight_id FROM _Flight_CREATE WHERE flight_number = ?", (flight_number,))
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
