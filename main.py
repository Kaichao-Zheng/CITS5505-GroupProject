from app import app, db
from app.db_models import User, Merchant, Upload, Product, PriceData, Share
from datetime import date
import sqlalchemy as sa

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'db': db, 'date': date, 'User': User, 'Merchant': Merchant, 'Upload': Upload, 'Product': Product, 'PriceData': PriceData, 'Share': Share}
