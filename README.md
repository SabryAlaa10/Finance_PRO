# 💎 Finance PRO Dashboard

A comprehensive personal finance management application built with Streamlit.

## 🌟 Features

- **📊 Dashboard**: Real-time KPIs and financial overview
- **➕ Add Transaction**: Easy transaction entry with dynamic categories
- **💸 Expense Analysis**: Detailed expense tracking and visualization
- **💰 Income Tracking**: Monitor income sources including Freelancing (Mostaql)
- **📈 Investments**: Portfolio management and performance tracking
- **🏦 Wallets & Banks**: Multi-wallet management
- **📄 PDF Reports**: Generate weekly and monthly financial reports

## 🚀 Live Demo

[Finance PRO on Streamlit Cloud](https://your-app-url.streamlit.app)

## 💻 Local Installation

1. Clone the repository:
```bash
git clone https://github.com/SabryAlaa10/Finance_PRO.git
cd Finance_PRO
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Login credentials:
   - Username: `saleh`
   - Password: `saleh109`

## 📁 Project Structure

```
Finance_PRO/
├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── data/
│   └── transactions.csv        # Transaction data
├── ui/
│   ├── dashboard.py           # Dashboard page
│   ├── add_transaction.py     # Add transaction page
│   ├── expenses.py            # Expense analysis
│   ├── income.py              # Income tracking
│   ├── investments.py         # Investment portfolio
│   ├── wallets.py             # Wallets management
│   └── styles.py              # CSS styles
└── logic/
    ├── data_loader.py         # Data operations
    ├── kpis.py                # KPI calculations
    ├── calculations.py        # Financial calculations
    └── report_generator.py    # PDF report generation
```

## 🎯 Key Features

### Dynamic Categories
Categories automatically update based on transaction type:
- **Income**: Freelancing (Mostaql), Salary, Pocket Money, etc.
- **Expense**: Food, Transport, Personal, Subscriptions, etc.
- **Investment**: Gold, Stock Trading, Crypto, Real Estate, etc.

### Professional Reports
- High-quality PDF reports with charts
- Weekly and monthly summaries
- Income/Expense breakdowns
- Transaction details

### Modern UI
- Animated login page
- Professional design with gradients
- Interactive charts
- Responsive layout

## 📊 Technologies

- **Frontend**: Streamlit
- **Data**: Pandas, CSV
- **Visualization**: Plotly
- **Reports**: ReportLab, Kaleido
- **Language**: Python 3.8+

## 🔐 Security

- Password-protected login
- Local data storage
- No external API dependencies

## 📝 License

MIT License - feel free to use and modify

## 👨‍💻 Developer

**Sabry Alaa**
- GitHub: [@SabryAlaa10](https://github.com/SabryAlaa10)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Made with ❤️ using Streamlit
