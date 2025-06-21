import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Number of products to generate
data_size = 100

# Sample data for product names and categories
PRODUCT_NAMES = [
    'Widget', 'Gadget', 'Thingamajig', 'Doodad', 'Gizmo', 'Contraption', 'Device', 'Apparatus', 'Instrument', 'Tool'
]
CATEGORIES = ['Electronics', 'Toys', 'Household', 'Outdoor', 'Clothing', 'Food', 'Books', 'Stationery']

def generate_inventory_data(size=100, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    data = []
    for i in range(1, size + 1):
        product_id = f"P{i:04d}"
        product_name = random.choice(PRODUCT_NAMES) + f" {random.randint(1, 100)}"
        category = random.choice(CATEGORIES)
        stock_quantity = random.randint(10, 200)
        sold_quantity = random.randint(0, stock_quantity)
        # Random purchase date within last 90 days
        purchase_date = datetime.now() - timedelta(days=random.randint(0, 90))
        shelf_life_days = random.randint(7, 90)
        cost_price = round(random.uniform(5, 100), 2)
        selling_price = round(cost_price * random.uniform(1.1, 2.0), 2)
        data.append({
            'product_id': product_id,
            'product_name': product_name,
            'category': category,
            'stock_quantity': stock_quantity,
            'sold_quantity': sold_quantity,
            'purchase_date': purchase_date.strftime('%Y-%m-%d'),
            'shelf_life_days': shelf_life_days,
            'cost_price': cost_price,
            'selling_price': selling_price
        })
    df = pd.DataFrame(data)
    return df

def main():
    """
    Generates inventory data and saves it as inventory_data.csv
    """
    df = generate_inventory_data(data_size)
    df.to_csv('inventory_data.csv', index=False)
    print('Generated inventory_data.csv with', len(df), 'rows.')

if __name__ == "__main__":
    main() 