# responsible for rendering HTML templates and returning page views.

from flask import render_template, jsonify
from datetime import datetime, timedelta
from app import app

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

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('product.html')

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

@app.route('/forecast-prices')
def forecast():
    return render_template('forecast-prices.html')