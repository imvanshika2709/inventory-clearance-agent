import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# Make sure to install openai: pip install openai
import openai

st.set_page_config(page_title="Inventory Clearance AI Agent")

# App title
st.title("Inventory Clearance AI Agent")

# Load inventory data
def load_data(csv_path='inventory_data.csv'):
    return pd.read_csv(csv_path)

def compute_fields(df):
    # Convert purchase_date to datetime
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    # Calculate expiry_date
    df['expiry_date'] = df['purchase_date'] + pd.to_timedelta(df['shelf_life_days'], unit='D')
    # Calculate days_to_expiry
    today = pd.Timestamp(datetime.now().date())
    df['days_to_expiry'] = (df['expiry_date'] - today).dt.days
    # Calculate stock-to-sale ratio (avoid division by zero)
    df['stock_to_sale_ratio'] = df.apply(lambda row: row['stock_quantity'] / row['sold_quantity'] if row['sold_quantity'] > 0 else float('inf'), axis=1)
    return df

def filter_clearance(df, expiry_window, category):
    # Expiring soon
    expiring_soon = df['days_to_expiry'] < expiry_window
    # Overstocked
    overstocked = df['stock_quantity'] > 2 * df['sold_quantity']
    # Combine conditions
    clearance_mask = expiring_soon | overstocked
    filtered = df[clearance_mask]
    # Filter by category if not 'All'
    if category != 'All':
        filtered = filtered[filtered['category'] == category]
    # Ensure always a DataFrame
    return filtered.reset_index(drop=True)

def main():
    df = load_data()
    df = compute_fields(df)

    # Sidebar filters
    st.sidebar.header("Filters")
    categories = ['All'] + sorted(df['category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)
    expiry_window = st.sidebar.slider("Expiry window (days)", min_value=1, max_value=30, value=10)

    # Filtered clearance recommendations
    clearance_df = filter_clearance(df, expiry_window, selected_category)

    st.markdown("## 🛍️ Clearance Recommendations")
    st.write(
        "Products expiring soon or overstocked (stock > 2× sold). Use the filters to refine recommendations."
    )
    show_cols = [
        'product_id', 'product_name', 'category', 'stock_quantity', 'sold_quantity',
        'purchase_date', 'expiry_date', 'days_to_expiry', 'stock_to_sale_ratio', 'cost_price', 'selling_price'
    ]
    # Only use columns that exist in clearance_df
    available_cols = [col for col in show_cols if col in clearance_df.columns]
    if clearance_df.empty:
        st.info("No clearance recommendations for the selected filters.")
    else:
        # Explicitly cast to DataFrame for safety and linter clarity
        try:
            display_df = pd.DataFrame(clearance_df[available_cols])
            st.dataframe(display_df.sort_values(['days_to_expiry', 'stock_to_sale_ratio']))
        except Exception as e:
            st.error(f"Error displaying table: {e}")

    # --- Chat-based section ---
    st.markdown("## 💬 Ask the Inventory Agent")
    st.write("Ask a question about the clearance recommendations above. For example: 'Which products are expiring soonest?' or 'List overstocked items in Electronics.'")

    openai.api_key = "sk-" # actual api key

    user_question = st.text_input("Your question:", key="chat_input")

    if user_question:
        # Prepare the prompt for the OpenAI model
        try:
            chat_df = pd.DataFrame(clearance_df[available_cols])
            csv_data = chat_df.to_csv(index=False)
            system_prompt = (
                "You are an inventory clearance assistant. "
                "You are given a CSV of products recommended for clearance. "
                "Answer the user's question using only the data in the CSV. "
                "If the answer is not in the data, say so."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"CSV Data:\n{csv_data}\n\nQuestion: {user_question}"}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0
            )
            answer = response.choices[0].message['content'].strip()
            st.success(answer)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main() 