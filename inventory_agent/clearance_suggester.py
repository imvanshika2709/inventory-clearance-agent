import pandas as pd

def load_analyzed_data(csv_path='analyzed_inventory.csv'):
    return pd.read_csv(csv_path)

def suggest_clearance_items(df):
    """
    Suggests items for clearance sale with reasons.
    Reasons: expiring soon, overstocked with low sales, or both.
    """
    suggestions = []
    for _, row in df.iterrows():
        reasons = []
        if row.get('expiring_soon', False):
            reasons.append('Expiring soon')
        if row.get('overstocked_low_sales', False):
            reasons.append('Overstocked with low sales')
        if reasons:
            suggestions.append({
                'product_id': row['product_id'],
                'product_name': row['product_name'],
                'category': row['category'],
                'stock_quantity': row['stock_quantity'],
                'sold_quantity': row['sold_quantity'],
                'days_to_expiry': row['days_to_expiry'],
                'reason': ', '.join(reasons)
            })
    return pd.DataFrame(suggestions)

def main():
    """
    Loads analyzed data, suggests clearance items, and saves them.
    """
    df = load_analyzed_data()
    clearance_df = suggest_clearance_items(df)
    clearance_df.to_csv('clearance_suggestions.csv', index=False)
    print('Clearance suggestions saved as clearance_suggestions.csv')
    print(clearance_df.head())

if __name__ == "__main__":
    main() 