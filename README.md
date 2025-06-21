# inventory-clearance-agent
#  Inventory Clearance AI Agent

An AI-powered Streamlit app that helps retailers analyze their inventory and recommend products for clearance sales. It uses product expiry dates and stock-to-sale ratios to suggest which items are either overstocked or expiring soon.

---

##  Features

-  Load inventory from a CSV file
-  Identify near-expiry products
-  Detect overstocked items (stock > 2× sold)
-  Chat with an AI agent to answer natural language questions like:
  - *"Which products are expiring this week?"*
  - *"List overstocked items in Electronics."*

---

##  Files

- `app.py` – Streamlit app
- `inventory_data.csv` – Sample inventory data
- `requirements.txt` – Python dependencies

---

##  To Run Locally:

1. **Clone the repo**
   ```bash
   git clone https://github.com/imvanshika2709/inventory-clearance-agent.git
   cd inventory-clearance-agent
