import pandas as pd
from datetime import datetime, timedelta

# Load the inventory data
def load_inventory_data(csv_path='inventory_data.csv'):
    return pd.read_csv(csv_path)

def add_expiry_info(df):
    """
    Adds expiry_date and days_to_expiry columns to the DataFrame.
    """
    # Convert purchase_date to datetime
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    # Calculate expiry_date
    df['expiry_date'] = df['purchase_date'] + pd.to_timedelta(df['shelf_life_days'], unit='D')
    # Calculate days_to_expiry from today
    today = pd.Timestamp(datetime.now().date())
    df['days_to_expiry'] = (df['expiry_date'] - today).dt.days
    return df

def flag_expiring_soon(df, days=10):
    """
    Flags items expiring in less than 'days' days.
    """
    df['expiring_soon'] = df['days_to_expiry'] < days
    return df

def flag_overstocked_low_sales(df):
    """
    Flags items where stock_quantity > 2 * sold_quantity.
    """
    df['overstocked_low_sales'] = df['stock_quantity'] > 2 * df['sold_quantity']
    return df

def analyze_inventory(csv_path='inventory_data.csv'):
    df = load_inventory_data(csv_path)
    df = add_expiry_info(df)
    df = flag_expiring_soon(df)
    df = flag_overstocked_low_sales(df)
    return df

def main():
    """
    Loads, analyzes, and saves the analyzed inventory data.
    """
    df = analyze_inventory()
    df.to_csv('analyzed_inventory.csv', index=False)
    print('Analyzed inventory saved as analyzed_inventory.csv')
    print(df.head())

if __name__ == "__main__":
    main() 