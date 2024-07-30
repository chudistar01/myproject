import os

from flask import Flask, request, jsonify, render_template

from flight_application.db import get_db

import functools

from . import db, register, admin


def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/static', static_folder='static', instance_relative_config=True)

    db_path = os.getenv('DATABASE', '/tmp/flight_application.sqlite')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flight_application.sqlite'),
        DEBUG=True
    )

    db.init_app(app)
    app.register_blueprint(register.user_bp)
    app.register_blueprint(admin.admin_bp)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.before_first_request
    def initialize_database():
        if not os.path.exists(app.config['DATABASE']):
            with app.app_context():
                db.init_db()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/search_flights', methods=['GET', 'POST'])
    def search_flights():
        if request.method == 'POST':
            departure_airport = request.form.get('departure_airport')
            arrival_airport = request.form.get('arrival_airport')
            departure_time = request.form.get('departure_time')

            if not departure_airport or not arrival_airport or not departure_time:
                error = "Missing required parameters"
                return render_template('search_flights.html', error=error), 400

            query = """
            SELECT * FROM _FLIGHT_CREAT
            WHERE departure_airport = :departure_airport
            AND arrival_airport = :arrival_airport
            AND departure_time >= :departure_time
            """

            try:
                db = get_db()
                flights = db.execute(query, {
                    'departure_airport': departure_airport,
                    'arrival_airport': arrival_airport,
                    'departure_time': departure_time
                }).fetchall()

                flights_list = [dict(flight) for flight in flights]

                if not flights_list:
                    return render_template('flights_results.html', message="No available flights")
            
                return render_template('flights_results.html', flights=flights_list)
            except Exception as e:
                error = f"An error occurred: {e}"
                return render_template('search_flights.html', error=error), 500
            finally:
                db.close()
        else:
            return render_template('search_flights.html')
    return app
