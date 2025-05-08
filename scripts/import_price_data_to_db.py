import os
import sys
import csv
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, db
from app.db_models import PriceData

# Adjust the CSV path if needed
CSV_PATH = 'mock_price_data_may.csv'


with app.app_context():
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        price_data_list = []
        for row in reader:
            price_data = PriceData(
                product_id=int(row['product_id']),
                price=float(row['price']),
                date=datetime.strptime(row['date'], '%Y-%m-%d').date()
            )
            price_data_list.append(price_data)
        db.session.bulk_save_objects(price_data_list)
        db.session.commit()
    print(f"Imported {len(price_data_list)} rows into price_data table.")
