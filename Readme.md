
# 💰 PYUSD Ethereum Transfers Dashboard

This is a **streamlit-powered dashboard** that visualizes real-time and historical on-chain transactions of **PayPal USD (PYUSD)** on the Ethereum network. It allows users to track volume, view transaction trends, analyze top wallets, and more!

---

## 🚀 Project Overview

The dashboard provides insights into the PYUSD token ecosystem, including:

- ✅ Real-time statistics and historical charts  
- 📈 Daily volume and transaction count  
- 🏦 Top senders and receivers  
- 🔥 Activity heatmaps  
- 📂 CSV data download option  
- 🔁 Auto-refresh functionality for live updates

---

## 📊 Key Features

- **Interactive charts** using `Matplotlib` and `Seaborn`  
- **Auto-refresh** to update charts dynamically  
- **CSV Export** for external analysis  
- **Address filtering** and analysis per wallet  
- **Heatmap of day vs hour activity**  
- **Top 10 wallets by volume**

---

## 🧰 Tech Stack

- Python 🐍  
- Streamlit  
- Pandas  
- Matplotlib  
- Seaborn

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/pyusd-dashboard.git
   cd pyusd-dashboard
   ```

2. **Create and activate virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run dashboard.py
   ```

---

## 📁 Project Structure

```
pyusd-dashboard/
├── dashboard.py            # Main Streamlit application
├── pyusd.csv               # Transaction dataset
├── requirements.txt        # Required packages
└── README.md               # This file
```

---

## 📌 Data Source

The `pyusd.csv` file contains historical Ethereum transactions for the **PYUSD token**. Data fields include:

- `block_date`: Date of transaction  
- `from_address` / `to_address`: Sender and receiver  
- `pyusd_amount`: Amount of PYUSD transferred  
- `txn_hash`: Transaction hash  
- `block_number`: Block number  

---

## 📸 Screenshots

<details>
  <summary>📊 Sample Dashboard View</summary>

  ![Dashboard Screenshot](link-to-screenshot-if-available)

</details>

---

## 👤 Author

**Ayobami Akande**  
A brooding Software developer 
Passionate about blockchain analytics, AI, and building tech for impact.

---

## 🛠️ Contributing

Contributions, issues, and suggestions are welcome!  
Feel free to open a pull request or issue.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- PayPal USD (PYUSD)  
- Streamlit Community  
- Etherscan / Data Sources  
