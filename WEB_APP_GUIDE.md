# Flask Web Application Usage Guide

This guide explains how to run and use the Flask web interface for the Dummy Bank application.

## Quick Start

1. **Install Flask**:
   ```bash
   pip install Flask
   ```

2. **Start the Web Application**:
   ```bash
   python3 app.py
   ```

3. **Access the Application**:
   Open your web browser and navigate to: `http://127.0.0.1:5000`

## Features

### User Registration
- Create new accounts with initial deposit
- Password confirmation validation
- Automatic account number generation

### User Authentication
- Secure login with account number and password
- Session management
- Automatic logout functionality

### Banking Operations
- **Deposit**: Add money to your account
- **Withdraw**: Remove money from your account (with balance validation)
- **Transfer**: Send money to other accounts
- **Transaction History**: View complete transaction records with filtering

### Dashboard Features
- Account balance display
- Recent transaction overview
- Quick action buttons
- Responsive navigation

## Running Tests

### Test the Banking Core
```bash
python3 -m unittest test_bank.py -v
```

### Test the Web Application
```bash
python3 test_flask_app.py
```

## Web Application Structure

```
├── app.py                 # Main Flask application
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login form
│   ├── register.html     # Registration form
│   ├── dashboard.html    # Main dashboard
│   ├── deposit.html      # Deposit form
│   ├── withdraw.html     # Withdrawal form
│   ├── transfer.html     # Transfer form
│   ├── transactions.html # Transaction history
│   ├── 404.html         # Error page
│   └── 500.html         # Error page
├── static/              # Static assets
│   └── css/
│       └── style.css    # Custom styling
└── test_flask_app.py    # Web application tests
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Bootstrap Icons
- **Data Storage**: JSON files (via existing bank.py)
- **Testing**: Python unittest framework

## Security Features

- Password hashing (handled by bank.py)
- Session-based authentication
- Input validation and sanitization
- CSRF protection ready (can be enabled)
- Error handling and user feedback

## Browser Compatibility

The web application is tested and works with:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Development Mode

The application runs in debug mode by default for development. For production use, consider:

1. Setting `debug=False`
2. Using a production WSGI server like Gunicorn
3. Configuring environment variables for secrets
4. Setting up SSL/HTTPS
5. Implementing rate limiting

## API Endpoints

| Route | Method | Description |
|-------|---------|-------------|
| `/` | GET | Home (redirects to login/dashboard) |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/dashboard` | GET | Main dashboard |
| `/deposit` | GET, POST | Deposit money |
| `/withdraw` | GET, POST | Withdraw money |
| `/transfer` | GET, POST | Transfer money |
| `/transactions` | GET | Transaction history |
| `/logout` | GET | User logout |