Personal Finance Tracker
A simple Python-based application to track personal finances, manage budgets, and visualize spending vs. income.

Features
Add income and expense transactions.
Set and manage budgets for different categories.
View spending vs. budget comparison through a bar graph.
Persistent data storage using CSV files.
Requirements
Python 3.6+
Required Libraries: tkinter, matplotlib
Install missing libraries with:

bash
Copy code
pip install matplotlib
How to Use
Run the Application:
bash
Copy code
python app.py
Add Transactions:
Enter transaction type, amount, category, and date.
Click Add Transaction to save.
Set Budgets:
Enter category and budget amount.
Click Set Budget to save.
Visualize Spending:
Click Show Spending vs Budget to view a bar graph.
File Structure
transactions.csv: Stores all transactions.
budgets.csv: Stores category budgets.
