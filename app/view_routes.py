from flask import Blueprint, render_template, redirect, flash, request, jsonify, g, send_from_directory, current_app
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from datetime import datetime, timedelta
from app.db_models import db, User, Merchant
from app.forms import LoginForm, RegistrationForm
import os

view_bp = Blueprint('view', __name__)

@view_bp.before_request
def before_request():
    g.login_form = LoginForm()
    g.register_form = RegistrationForm()
    if request.accept_mimetypes.accept_html:
        print("Init login_form and register_form")

# TODO: Add new file for context_processor and import here!
# context_processor has been added because we need to reload all the notifications for the users everytime a new route has been called.
# Every time a new route is called the injector will be called! 

@view_bp.context_processor
def inject_notifications():
    notifications = [
        {"sender": "Kushan", "product": "TimTam", "message": "Price dropped at Coles!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
        {"sender": "Alex", "product": "iPhone", "message": "JB Hi-Fi has deals!"},
    ]
    return dict(notifications=notifications)

@view_bp.context_processor
def request_mechants():
    merchants = Merchant.query.all()
    return dict(merchants=merchants)

@view_bp.route('/', methods=['GET', 'POST'])
def index():
    redirect = handle_login_post()
    if redirect:
        return redirect
    return render_template('index.html', login_form=g.login_form, register_form=g.register_form)

@view_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')

@view_bp.route('/product', methods=['GET', 'POST'])
def product():
    redirect = handle_login_post()
    if redirect:
        return redirect
    return render_template('product.html', login_form=g.login_form)

@view_bp.route('/forecast-prices', methods=['GET', 'POST'])
def forecast():
    redirect = handle_login_post()
    if redirect:
        return redirect
    return render_template('forecast-prices.html', login_form=g.login_form)

@login_required
@view_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'bg-warning')
    return redirect(request.referrer)

def handle_login_post():
    form = g.login_form
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        # failed login
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'bg-danger')
            return redirect(request.path)
        # successful login
        login_user(user)
        flash(f'Welcome back, {form.username.data} !', 'bg-success')
        return redirect(request.path)
    else:
        errors = []
        for field in form:
            for err in field.errors:
                errors.append(field.label.text)
        if errors:
            if len(errors) == 1:
                msg = f"{errors[0]} is required."
            else:
                msg = f"{', '.join(errors[:-1])} and {errors[-1]} are required."
            flash(msg.capitalize(), 'bg-danger')
    return None

@view_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(request.referrer)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type=form.user_type.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Success registration
        login_user(user)        # Auto login
        flash(f'Hi {form.username.data}, welcome to Price Trend !', 'bg-success')
        return redirect(request.referrer)
    else:
        empty_errors = []
        other_errors = []
        
        for field in form:
            for err in field.errors:
                if err == 'This field is required.':
                    empty_errors.append(field.label.text)
                else:
                    other_errors.append(err)
        if empty_errors:
            if len(empty_errors) == 1:
                msg = f"{empty_errors[0]} is required."
            else:
                msg = f"{', '.join(empty_errors[:-1])} and {empty_errors[-1]} are required."
            flash(msg.capitalize(), 'bg-danger')
        
        for err in other_errors:
            flash(err, 'bg-danger')
    return redirect(request.referrer)

@view_bp.route('/ERD', methods=['GET', 'POST'])
def ERD():
    return render_template('demo/ERD.html', login_form=g.login_form)

@view_bp.route('/jinja', methods=['GET', 'POST'])
def jinja():
    return render_template('demo/jinja.html', login_form=g.login_form)

@view_bp.route('/marks', methods=['GET', 'POST'])
def marks():
    return render_template('demo/marks.html', login_form=g.login_form)

# may should be moved to api_routes.py and access via localhost:5000/api/forecast-data ?
@view_bp.route('/forecast-data', methods=['GET'])
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