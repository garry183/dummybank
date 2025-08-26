#!/usr/bin/env python3
"""
Flask Web Interface for Dummy Bank Application

A web-based interface for the banking system providing:
- User authentication and session management
- Account dashboard with balance and transaction history
- Banking operations (deposit, withdraw, transfer)
- Responsive web interface with Bootstrap styling

Integrates with existing DummyBank class to maintain data compatibility.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from bank import DummyBank

app = Flask(__name__)
app.secret_key = 'dummy_bank_secret_key_change_in_production'  # In production, use environment variable

# Initialize bank instance
bank = DummyBank()

@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise login."""
    if 'account_number' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for existing accounts."""
    if request.method == 'POST':
        account_number = request.form.get('account_number', '').strip()
        password = request.form.get('password', '')
        
        if not account_number or not password:
            flash('Please enter both account number and password.', 'error')
            return render_template('login.html')
        
        # Authenticate user
        if bank.authenticate(account_number, password):
            # Get account info for session
            account_info = bank.get_account_info(account_number, password)
            if 'error' not in account_info:
                session['account_number'] = account_number
                session['account_name'] = account_info['name']
                flash(f'Welcome back, {account_info["name"]}!', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Invalid account number or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page for creating new accounts."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        initial_deposit = request.form.get('initial_deposit', '0').strip()
        
        # Validation
        if not name:
            flash('Name is required.', 'error')
            return render_template('register.html')
        
        if not password:
            flash('Password is required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 4:
            flash('Password must be at least 4 characters long.', 'error')
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
            if 'error' not in result:
                flash(f'Account created successfully! Your account number is {result["account_number"]}.', 'success')
                # Auto-login after registration
                session['account_number'] = result['account_number']
                session['account_name'] = name
                return redirect(url_for('dashboard'))
            else:
                flash(result['error'], 'error')
        except Exception as e:
            flash('Error creating account. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user and clear session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard showing account balance and recent transactions."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    # For dashboard display, we'll show basic account info
    # Users will need to enter password for individual transactions
    account_number = session['account_number']
    account_name = session.get('account_name', 'Account Holder')
    
    # We'll create a special dashboard view that doesn't require real-time balance
    # since that requires password. Instead, we'll prompt for password when needed.
    
    return render_template('dashboard.html', 
                         account_number=account_number,
                         account_name=account_name)

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    """Deposit money form and processing."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Web deposit').strip()
        password = request.form.get('password', '')
        
        if not password:
            flash('Password is required for transactions.', 'error')
            return render_template('deposit.html')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Deposit amount must be positive.', 'error')
                return render_template('deposit.html')
        except ValueError:
            flash('Invalid amount entered.', 'error')
            return render_template('deposit.html')
        
        # Process deposit
        result = bank.deposit(session['account_number'], amount, password, description)
        if 'error' in result:
            flash(result['error'], 'error')
            return render_template('deposit.html')
        
        flash(f'Successfully deposited ${amount:.2f}. New balance: ${result["new_balance"]:.2f}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    """Withdraw money form and processing."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Web withdrawal').strip()
        password = request.form.get('password', '')
        
        if not password:
            flash('Password is required for transactions.', 'error')
            return render_template('withdraw.html')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Withdrawal amount must be positive.', 'error')
                return render_template('withdraw.html')
        except ValueError:
            flash('Invalid amount entered.', 'error')
            return render_template('withdraw.html')
        
        # Process withdrawal
        result = bank.withdraw(session['account_number'], amount, password, description)
        if 'error' in result:
            flash(result['error'], 'error')
            return render_template('withdraw.html')
        
        flash(f'Successfully withdrew ${amount:.2f}. New balance: ${result["new_balance"]:.2f}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('withdraw.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    """Transfer money form and processing."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        to_account = request.form.get('to_account', '').strip()
        amount = request.form.get('amount', '').strip()
        description = request.form.get('description', 'Web transfer').strip()
        password = request.form.get('password', '')
        
        if not password:
            flash('Password is required for transactions.', 'error')
            return render_template('transfer.html')
        
        if not to_account:
            flash('Destination account number is required.', 'error')
            return render_template('transfer.html')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Transfer amount must be positive.', 'error')
                return render_template('transfer.html')
        except ValueError:
            flash('Invalid amount entered.', 'error')
            return render_template('transfer.html')
        
        # Process transfer
        result = bank.transfer(session['account_number'], to_account, amount, password, description)
        if 'error' in result:
            flash(result['error'], 'error')
            return render_template('transfer.html')
        
        flash(f'Successfully transferred ${amount:.2f} to account {to_account}. New balance: ${result["from_new_balance"]:.2f}', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('transfer.html')

@app.route('/check_balance', methods=['POST'])
def check_balance():
    """Check account balance with password verification."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    password = request.form.get('password', '')
    if not password:
        flash('Password is required to check balance.', 'error')
        return redirect(url_for('dashboard'))
    
    result = bank.get_balance(session['account_number'], password)
    if 'error' in result:
        flash(result['error'], 'error')
        return redirect(url_for('dashboard'))
    
    flash(f'Current balance: ${result["balance"]:.2f}', 'success')
    return redirect(url_for('dashboard'))

@app.route('/history', methods=['GET', 'POST'])
def history():
    """View full transaction history."""
    if 'account_number' not in session:
        flash('Please log in to access your account.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        if not password:
            flash('Password is required to view transaction history.', 'error')
            return redirect(url_for('dashboard'))
        
        result = bank.get_transaction_history(session['account_number'], password, 50)  # Show up to 50 transactions
        if 'error' in result:
            flash(result['error'], 'error')
            return redirect(url_for('dashboard'))
        
        return render_template('history.html', 
                             transactions=result['transactions'],
                             total_transactions=result['total_transactions'])
    
    # For GET requests, redirect to dashboard
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    print("=== Dummy Bank Web Interface ===")
    print("Starting Flask web server...")
    print("Visit http://localhost:5000 to access the banking system")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)