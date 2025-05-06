# responsible for rendering HTML templates and returning page views.

from flask import render_template, flash, redirect, request, jsonify, g
from flask_login import login_user
import sqlalchemy as sa
from datetime import datetime, timedelta
from app import app, db
from app.db_models import User
from app.forms import LoginForm

@app.before_request
def before_request():
    g.form = LoginForm()

# TODO: Add new file for context_processor and import here!
# context_processor has been added because we need to reload all the notifications for the users everytime a new route has been called.
# Every time a new route is called the injector will be called! 
@app.context_processor
def inject_notifications():
    notifications = [
        {"sender": "Kushan", "product": "TimTam", "message": "Price dropped at Coles!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
    ]
    return dict(notifications=notifications)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    result = handle_login_post()
    if result:
        return result
    return render_template('index.html', form=g.form)

@app.route('/product', methods=['GET', 'POST'])
def product():
    result = handle_login_post()
    if result:
        return result
    return render_template('product.html', form=g.form)

@app.route('/forecast-prices', methods=['GET', 'POST'])
def forecast():
    result = handle_login_post()
    if result:
        return result
    return render_template('forecast-prices.html', form=g.form)


def handle_login_post():
    form = g.form
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        # failed login
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(request.path)
        # successful login
        login_user(user)
        flash(f'Welcome back, "{form.username.data}"!', 'success')
        return redirect(request.path)
    else:
        for field in [form.username, form.password]:
            for err in field.errors:
                flash(f"{field.label.text}: {err}", 'danger')
    return None

# may should be moved to api_routes.py and access via localhost:5000/api/forecast-data ?
@app.route('/forecast-data')
def forecast_data():

    # TODO: Replace with api response
    forecast = []

    base_date = datetime.today()
    num_datasets = 3  # or any dynamic number

    for d in range(num_datasets):
        dataset = {
            'label': f'Dataset {d + 1}',
            'data': []
        }
        for i in range(7):
            date = base_date + timedelta(days=i)
            dataset['data'].append({
                'date': date.strftime('%Y-%m-%d'),
                'value': 50 + d * 10 + i * 2  # example variation per dataset
            })
        forecast.append(dataset)

        # Below is the format the sample of the forecast object should look like

        # [{
        #       'label': 'Dataset 1',
        #       'data': [
        #                   {'date': '2025-04-30', 'value': 50},
        #                   {'date': '2025-05-01', 'value': 52},
        #                   {'date': '2025-05-02', 'value': 54},
        #                   {'date': '2025-05-03', 'value': 56},
        # ...
        # {
        #       'label': 'Dataset 2',
        #       'data': [
        #                   {'date': '2025-04-30', 'value': 50},
        #                   {'date': '2025-05-01', 'value': 52},
        #                   {'date': '2025-05-02', 'value': 54},
        #                   {'date': '2025-05-03', 'value': 56},
        # ...
        # }]
    return jsonify(forecast)