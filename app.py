#!/usr/bin/env python3
"""
Flask Web Interface for Dummy Bank Application

A web interface for the banking system that provides:
- User authentication and session management
- Account dashboard and balance display
- Banking operations (deposit, withdraw, transfer)
- Transaction history viewing
- Responsive design with Bootstrap styling
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from bank import DummyBank

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'dummy-bank-secret-key-2024'  # Change this in production

# Initialize bank instance
bank = DummyBank()

@app.route('/')
def home():
    """Home page - redirect to dashboard if logged in, otherwise login."""
    if 'account_number' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for user authentication."""
    if request.method == 'POST':
        account_number = request.form.get('account_number', '').strip()
        password = request.form.get('password', '').strip()
        
        if not account_number or not password:
            flash('Please enter both account number and password.', 'error')
            return render_template('login.html')
        
        # Authenticate user
        if bank.authenticate(account_number, password):
            session['account_number'] = account_number
            session['password'] = password  # Store for subsequent operations
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid account number or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page for creating new accounts."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        initial_deposit = request.form.get('initial_deposit', '0').strip()
        
        # Validation
        if not name or not password:
            flash('Name and password are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        try:
            initial_deposit = float(initial_deposit) if initial_deposit else 0.0
            if initial_deposit < 0:
                flash('Initial deposit cannot be negative.', 'error')
                return render_template('register.html')
        except ValueError:
            flash('Invalid initial deposit amount.', 'error')
            return render_template('register.html')
        
        # Create account
        try:
            result = bank.create_account(name, initial_deposit, password)
            flash(f'Account created successfully! Your account number is: {result["account_number"]}', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard showing account information."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    account_number = session['account_number']
    password = session['password']
    
    # Get account information
    account_info = bank.get_account_info(account_number, password)
    if 'error' in account_info:
        flash('Error retrieving account information.', 'error')
        return redirect(url_for('login'))
    
    # Get recent transactions
    transaction_history = bank.get_transaction_history(account_number, password, limit=5)
    recent_transactions = transaction_history.get('transactions', [])
    
    return render_template('dashboard.html', 
                         account_info=account_info, 
                         recent_transactions=recent_transactions)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    """Deposit money into account."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Deposit').strip()
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Deposit amount must be positive.', 'error')
                return render_template('deposit.html')
            
            result = bank.deposit(session['account_number'], amount, session['password'], description)
            if 'error' in result:
                flash(f'Deposit failed: {result["error"]}', 'error')
            else:
                flash(f'Successfully deposited ${amount:.2f}. New balance: ${result["new_balance"]:.2f}', 'success')
                return redirect(url_for('dashboard'))
        except ValueError:
            flash('Invalid amount entered.', 'error')
    
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    """Withdraw money from account."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Withdrawal').strip()
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Withdrawal amount must be positive.', 'error')
                return render_template('withdraw.html')
            
            result = bank.withdraw(session['account_number'], amount, session['password'], description)
            if 'error' in result:
                flash(f'Withdrawal failed: {result["error"]}', 'error')
            else:
                flash(f'Successfully withdrew ${amount:.2f}. New balance: ${result["new_balance"]:.2f}', 'success')
                return redirect(url_for('dashboard'))
        except ValueError:
            flash('Invalid amount entered.', 'error')
    
    return render_template('withdraw.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    """Transfer money to another account."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        to_account = request.form.get('to_account', '').strip()
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Transfer').strip()
        
        if not to_account:
            flash('Recipient account number is required.', 'error')
            return render_template('transfer.html')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Transfer amount must be positive.', 'error')
                return render_template('transfer.html')
            
            result = bank.transfer(session['account_number'], to_account, amount, session['password'], description)
            if 'error' in result:
                flash(f'Transfer failed: {result["error"]}', 'error')
            else:
                flash(f'Successfully transferred ${amount:.2f} to account {to_account}. New balance: ${result["new_balance"]:.2f}', 'success')
                return redirect(url_for('dashboard'))
        except ValueError:
            flash('Invalid amount entered.', 'error')
    
    return render_template('transfer.html')

@app.route('/transactions')
def transactions():
    """View transaction history."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    account_number = session['account_number']
    password = session['password']
    
    # Get transaction history
    limit = request.args.get('limit', 20, type=int)
    transaction_history = bank.get_transaction_history(account_number, password, limit=limit)
    
    if 'error' in transaction_history:
        flash('Error retrieving transaction history.', 'error')
        transactions_list = []
    else:
        transactions_list = transaction_history.get('transactions', [])
    
    return render_template('transactions.html', transactions=transactions_list, limit=limit)

@app.route('/logout')
def logout():
    """Log out user and clear session."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)