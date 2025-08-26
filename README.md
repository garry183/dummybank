# DummyBank - Test Automation Banking Website

A fully functional dummy banking website designed for test automation practice. This website provides all essential banking features with a user-friendly interface and persistent data storage.

## 🌟 Features

### User Management
- **User Registration**: Sign up with name, phone, email, and password
- **User Authentication**: Login with name and password
- **Session Management**: Persistent login state across browser sessions

### Account Management  
- **Account Creation**: Open Savings or Current accounts
- **Multiple Account Types**: Support for both Savings and Current accounts
- **Account Dashboard**: View account details, balances, and transaction history
- **Initial Deposits**: Add money while creating accounts

### Banking Operations
- **Add Money**: Deposit funds to any account
- **Check Balance**: Real-time balance display across all sections
- **Money Transfer**: Transfer funds between accounts (including other users' accounts)
- **Money Withdrawal**: Withdraw funds with balance validation
- **Transaction History**: Complete transaction log with dates and notes

### Investment Options
- **Fixed Deposits (FD)**: 
  - Multiple tenure options (6 months to 5 years)
  - Interest rates from 5% to 9% per annum
  - Automatic maturity calculation
- **Recurring Deposits (RD)**:
  - Monthly installment-based savings
  - Interest rates from 6.5% to 9.5% per annum  
  - Installment tracking and maturity handling

### Technical Features
- **Data Persistence**: All data stored in browser localStorage
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Real-time Updates**: Instant balance and transaction updates
- **Form Validation**: Comprehensive input validation
- **Error Handling**: User-friendly error messages
- **Account Generation**: Automatic unique account number generation

## 🚀 Live Demo

**GitHub Pages URL**: `https://[username].github.io/dummybank/`

## 📱 Screenshots

![Home Page](screenshots/home.png)
![Dashboard](screenshots/dashboard.png)
![Accounts](screenshots/accounts.png)

## 🛠 Setup for GitHub Pages

### Step 1: Enable GitHub Pages
1. Go to your repository settings
2. Scroll to "Pages" section
3. Select "Deploy from a branch"
4. Choose "main" branch and "/ (root)" folder
5. Click "Save"

### Step 2: Access Your Website
Your website will be available at: `https://[your-username].github.io/dummybank/`

## 💻 Local Development

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.x (for local server) or any HTTP server

### Running Locally

**Option 1: Python HTTP Server**
```bash
# Navigate to project directory
cd dummybank

# Start server (Python 3)
python -m http.server 8000

# Or Python 2
python -m SimpleHTTPServer 8000

# Open browser to http://localhost:8000
```

**Option 2: Node.js HTTP Server**
```bash
# Install http-server globally
npm install -g http-server

# Navigate to project directory
cd dummybank

# Start server
http-server

# Open browser to displayed URL
```

**Option 3: VS Code Live Server**
1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## 🎯 Test Automation Ready

This website is specifically designed for test automation practice with:

### Automation-Friendly Features
- **Consistent Element IDs**: All interactive elements have unique, stable IDs
- **Predictable URLs**: Hash-based routing for easy navigation testing
- **Clear Success/Error Messages**: Distinct alert messages for validation
- **Data Attributes**: Elements tagged for easy selector creation
- **Standardized Forms**: Consistent form structure across all features

### Test Scenarios
1. **User Registration & Login Flow**
2. **Account Creation with Different Types**
3. **Money Management Operations**
4. **Inter-account Transfers**
5. **Investment Product Testing**
6. **Balance Verification Workflows**
7. **Transaction History Validation**
8. **Form Validation Testing**
9. **Session Management Testing**
10. **Multi-user Scenario Testing**

### Sample Test Data
```javascript
// Sample user data for testing
const testUsers = [
  {
    name: "John Doe",
    phone: "9876543210", 
    email: "john.doe@example.com",
    password: "password123"
  },
  {
    name: "Jane Smith",
    phone: "9876543211",
    email: "jane.smith@example.com", 
    password: "password456"
  }
];
```

## 📁 Project Structure

```
dummybank/
├── index.html          # Main HTML file with all sections and modals
├── style.css           # Custom CSS styles and responsive design
├── script.js           # JavaScript functionality and data management
└── README.md          # Documentation
```

## 🔧 Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.1.3, Font Awesome 6.0
- **Data Storage**: Browser localStorage
- **Architecture**: Single Page Application (SPA)

## 🎮 How to Use

### For New Users
1. **Visit the website**
2. **Sign Up**: Click "Sign Up" and fill the registration form
3. **Login**: Use your credentials to log in
4. **Create Account**: Open your first Savings or Current account
5. **Add Money**: Deposit initial funds
6. **Explore Features**: Try transfers, withdrawals, and investments

### For Test Automation
1. **Set up your test framework** (Selenium, Playwright, Cypress, etc.)
2. **Use the provided test scenarios**
3. **Target stable element selectors**
4. **Validate success/error messages**
5. **Verify data persistence across sessions**

## 🐛 Known Limitations

1. **Data Storage**: Data is stored in browser localStorage (cleared when browser data is cleared)
2. **Multi-tab Sync**: Data changes in one tab don't auto-refresh in other tabs
3. **Bootstrap Modals**: Some modal interactions may require Bootstrap JS (included via CDN)
4. **Demo Purpose**: This is for testing only - not a real banking application

## 🔒 Security Note

⚠️ **Important**: This is a dummy application for testing purposes only. Do not use real personal information or treat this as a real banking system.

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for:
- Bug fixes
- New features
- UI improvements
- Test automation enhancements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

For issues or questions:
- Create an issue in the GitHub repository
- Check the test scenarios in the documentation
- Review the browser console for error messages

---

**Happy Testing! 🎉**