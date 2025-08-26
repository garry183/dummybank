# Dummy Bank Application

A complete banking system implementation that demonstrates all core banking functionalities with persistent data storage.

## ✅ ALL FUNCTIONALITIES TESTED AND WORKING

### Core Banking Features
- **Account Management**: Create accounts with unique account numbers and secure password authentication
- **Balance Operations**: Check account balance with authentication
- **Deposits**: Add money to accounts with transaction recording
- **Withdrawals**: Remove money with insufficient funds protection
- **Transfers**: Move money between accounts with dual transaction recording
- **Transaction History**: Complete audit trail of all account activities
- **Account Information**: Retrieve complete account details
- **Multi-Account Support**: List and manage multiple accounts

### Security Features
- **Password Hashing**: All passwords stored as SHA-256 hashes
- **Authentication**: Required for all account operations
- **Data Validation**: Input validation and error handling
- **Account Protection**: Prevent unauthorized access

## 📁 Data Storage Location

### Where Data is Saved
All data is persisted in JSON files within the `data/` directory:

```
dummybank/
├── data/
│   ├── accounts.json      # All account information
│   └── transactions.json  # Complete transaction history
├── bank.py               # Main banking system
├── test_bank.py         # Comprehensive test suite
├── demo.py              # Functionality demonstration
└── README.md            # This documentation
```

### Data Storage Details
- **Location**: `./data/` directory (created automatically)
- **Format**: JSON (human-readable and portable)
- **Files**:
  - `accounts.json`: Stores account details (number, name, balance, password hash, creation date, status)
  - `transactions.json`: Complete transaction log with timestamps and descriptions
- **Persistence**: Data survives application restarts
- **Security**: Passwords are hashed, never stored in plain text

## 🚀 Usage

### Running the Application
```bash
# Interactive CLI mode
python bank.py

# Run demonstration script
python demo.py

# Run comprehensive tests
python test_bank.py
```

### Example Account Data Structure
```json
{
  "1000000001": {
    "account_number": "1000000001",
    "name": "Alice Johnson", 
    "balance": 1050.0,
    "password_hash": "4e40e8ffe0ee32fa53e139147ed559229a5930f89c2204706fc174beb36210b3",
    "created_date": "2025-08-26T12:15:10.594912",
    "status": "active"
  }
}
```

### Example Transaction Data Structure
```json
{
  "id": 1,
  "account_number": "1000000001",
  "transaction_type": "deposit",
  "amount": 1000.0,
  "description": "Initial deposit",
  "related_account": "1000000001",
  "timestamp": "2025-08-26T12:15:10.595088",
  "date": "2025-08-26"
}
```

## 🧪 Test Coverage

The application includes comprehensive tests covering:
- ✅ Account creation and management
- ✅ Authentication and security
- ✅ All transaction types (deposit, withdrawal, transfer)
- ✅ Balance operations
- ✅ Transaction history
- ✅ Data persistence
- ✅ Error handling and edge cases
- ✅ Data storage format validation
- ✅ File system operations

**Test Results**: All 14 tests pass successfully

## 📊 Features Demonstrated

| Functionality | Status | Description |
|---------------|--------|-------------|
| Account Creation | ✅ Working | Create accounts with initial deposits |
| Authentication | ✅ Working | Secure password-based account access |
| Balance Inquiry | ✅ Working | Check current account balance |
| Deposits | ✅ Working | Add money with transaction logging |
| Withdrawals | ✅ Working | Remove money with balance validation |
| Transfers | ✅ Working | Move money between accounts |
| Transaction History | ✅ Working | Complete audit trail |
| Data Persistence | ✅ Working | JSON file storage |
| Error Handling | ✅ Working | Input validation and error messages |
| Security | ✅ Working | Password hashing and authentication |

## 🏦 Banking Operations Examples

```python
from bank import DummyBank

# Initialize bank
bank = DummyBank()

# Create accounts
account1 = bank.create_account("John Doe", 1000.0, "password123")
account2 = bank.create_account("Jane Smith", 500.0, "password456")

# Get account info
acc_num = account1['account_number']
balance = bank.get_balance(acc_num, "password123")
print(f"Balance: ${balance['balance']}")

# Deposit money
bank.deposit(acc_num, 250.0, "password123", "Salary deposit")

# Withdraw money  
bank.withdraw(acc_num, 100.0, "password123", "ATM withdrawal")

# Transfer between accounts
bank.transfer(acc_num, account2['account_number'], 200.0, "password123", "Payment")

# View transaction history
history = bank.get_transaction_history(acc_num, "password123", 10)
```

## 🔍 Data Verification

You can verify data is properly saved by examining the JSON files:

```bash
# View accounts
cat data/accounts.json

# View transactions  
cat data/transactions.json

# Get data location info
python -c "from bank import DummyBank; print(DummyBank().get_data_info())"
```

## Summary

✅ **All banking functionalities are working correctly**
✅ **Data is saved persistently in JSON files**  
✅ **Complete test coverage validates all features**
✅ **Secure authentication and data protection**
✅ **Human-readable data storage format**