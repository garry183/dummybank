# Flask Web Interface Usage Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install Flask
   ```

2. **Start the Web Server**
   ```bash
   python app.py
   ```

3. **Access the Application**
   Open your web browser and navigate to: `http://localhost:5000`

## Features

### 🔐 Authentication System
- **Login**: Existing account holders can log in using their account number and password
- **Registration**: New users can create accounts with optional initial deposits
- **Session Management**: Secure session-based authentication
- **Password Security**: All passwords are hashed using SHA-256

### 🏦 Banking Operations
- **Balance Inquiry**: Check account balance with password verification
- **Deposits**: Add money to your account with transaction descriptions
- **Withdrawals**: Withdraw money with balance validation
- **Transfers**: Send money between accounts
- **Transaction History**: View complete transaction records

### 🎨 User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Bootstrap Styling**: Professional and modern interface
- **Interactive Forms**: Client-side validation and user feedback
- **Flash Messages**: Real-time notifications for all operations
- **Navigation**: Intuitive menu system with user account display

## Page Guide

### Login Page (`/login`)
- Enter your account number and password
- Click "Sign In" to access your account
- New users can click "Create New Account"

### Registration Page (`/register`)
- Fill in your full name
- Create a secure password (minimum 4 characters)
- Optionally add an initial deposit
- Accept terms and conditions
- Account number is automatically generated

### Dashboard (`/dashboard`)
- Welcome message with account information
- Quick action buttons for all banking operations
- Account status and service information
- Security notice about password requirements

### Deposit Page (`/deposit`)
- Enter deposit amount
- Add optional description
- Provide password for authorization
- Immediate processing and balance update

### Withdrawal Page (`/withdraw`)
- Enter withdrawal amount
- Add optional description
- Password required for security
- Balance validation prevents overdrafts

### Transfer Page (`/transfer`)
- Enter destination account number
- Specify transfer amount
- Add optional description
- Password verification required
- Transfer summary before confirmation

### Transaction History (`/history`)
- Complete list of all transactions
- Filtered by transaction type (deposit, withdrawal, transfer)
- Date and time stamps
- Transaction descriptions and amounts
- Related account information for transfers

## Security Features

- **Password Protection**: All financial operations require password verification
- **Session Security**: User sessions expire for security
- **Input Validation**: Server-side and client-side form validation
- **Error Handling**: Secure error messages without exposing sensitive data
- **Data Encryption**: Passwords stored as SHA-256 hashes

## Integration with CLI

The web interface is fully compatible with the existing CLI system:

- **Shared Data**: Both interfaces use the same JSON data files
- **Account Compatibility**: Accounts created in CLI work in web interface and vice versa
- **Transaction Sync**: All transactions are recorded in the same format
- **No Conflicts**: Both interfaces can be used simultaneously

## Data Storage

- **Location**: `data/accounts.json` and `data/transactions.json`
- **Format**: Human-readable JSON format
- **Persistence**: Data persists between sessions
- **Backup**: Easy to backup by copying JSON files

## Troubleshooting

### Common Issues

1. **Page not loading**: Ensure Flask is installed and app.py is running
2. **Login fails**: Verify account number and password are correct
3. **Transactions fail**: Check password and account balance
4. **Styling issues**: Bootstrap CSS may be blocked - fallback styles included

### Error Messages

- **Invalid credentials**: Check account number and password
- **Insufficient funds**: Ensure adequate balance for withdrawals/transfers  
- **Account not found**: Verify destination account exists for transfers
- **Session expired**: Re-login if session times out

## Development

### File Structure
```
dummybank/
├── app.py                 # Main Flask application
├── bank.py                # Core banking logic (unchanged)
├── templates/             # HTML templates
│   ├── base.html         # Base template with Bootstrap
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── deposit.html      # Deposit form
│   ├── withdraw.html     # Withdrawal form
│   ├── transfer.html     # Transfer form
│   └── history.html      # Transaction history
├── static/               # Static files
│   └── css/
│       └── style.css     # Custom styles
└── data/                 # Data storage (auto-created)
    ├── accounts.json     # Account information
    └── transactions.json # Transaction history
```

### Configuration

- **Secret Key**: Change the Flask secret key in production
- **Port**: Default port is 5000, configurable in app.py
- **Debug Mode**: Disable debug mode in production
- **Data Directory**: Can be customized in DummyBank initialization

### Extending the Interface

The Flask application is designed to be easily extensible:

- **New Routes**: Add routes in app.py
- **New Templates**: Create HTML templates in templates/
- **Custom Styling**: Add CSS to static/css/
- **Additional Features**: Leverage existing DummyBank methods

## Production Deployment

For production use:

1. **Change Secret Key**: Use environment variable for Flask secret key
2. **Use WSGI Server**: Deploy with Gunicorn or similar WSGI server
3. **Enable HTTPS**: Use SSL/TLS certificates
4. **Database**: Consider migrating from JSON to proper database
5. **Logging**: Implement proper logging for monitoring
6. **Backup**: Set up automated backups of data files

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure the CLI version works correctly
4. Check the Flask application logs for error details