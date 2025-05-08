import csv
import random
from datetime import datetime, timedelta

# Configuration
product_ids = [1, 2, 3]  # Only product 1, 2, 3
start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 5, 31)
price_min, price_max = 3, 8

# Generate a list of all dates in May 2025
dates = []
cur = start_date
while cur <= end_date:
    dates.append(cur.strftime('%Y-%m-%d'))
    cur += timedelta(days=1)

rows = []
id_counter = 1
for product_id in product_ids:
    for date_str in dates:
        price = round(random.uniform(price_min, price_max), 1)
        rows.append({
            'id': id_counter,
            'product_id': product_id,
            'price': price,
            'date': date_str
        })
        id_counter += 1

# Write to CSV file
with open('mock_price_data_may.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'product_id', 'price', 'date'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} rows of mock price_data for May, saved as mock_price_data_may.csv")
