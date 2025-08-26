#!/usr/bin/env python3
"""
Dummy Bank Application

A simple banking system that demonstrates core banking functionalities:
- Account creation and management
- Deposits and withdrawals
- Money transfers
- Transaction history
- Data persistence using JSON files

Data Storage:
- accounts.json: Stores all account information
- transactions.json: Stores transaction history
"""

import json
import os
import hashlib
import datetime
from typing import Dict, List, Optional, Union


class DummyBank:
    def __init__(self, data_dir: str = "data"):
        """Initialize the dummy bank with data directory."""
        self.data_dir = data_dir
        self.accounts_file = os.path.join(data_dir, "accounts.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize JSON data files if they don't exist."""
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'w') as f:
                json.dump({}, f, indent=2)
        
        if not os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'w') as f:
                json.dump([], f, indent=2)
    
    def _load_accounts(self) -> Dict:
        """Load accounts from JSON file."""
        try:
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_accounts(self, accounts: Dict):
        """Save accounts to JSON file."""
        with open(self.accounts_file, 'w') as f:
            json.dump(accounts, f, indent=2)
    
    def _load_transactions(self) -> List:
        """Load transactions from JSON file."""
        try:
            with open(self.transactions_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_transactions(self, transactions: List):
        """Save transactions to JSON file."""
        with open(self.transactions_file, 'w') as f:
            json.dump(transactions, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_account_number(self) -> str:
        """Generate a unique account number."""
        accounts = self._load_accounts()
        account_num = 1000000001
        while str(account_num) in accounts:
            account_num += 1
        return str(account_num)
    
    def create_account(self, name: str, initial_deposit: float = 0.0, password: str = "password") -> Dict:
        """Create a new bank account."""
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        
        accounts = self._load_accounts()
        account_number = self._generate_account_number()
        
        account = {
            "account_number": account_number,
            "name": name,
            "balance": initial_deposit,
            "password_hash": self._hash_password(password),
            "created_date": datetime.datetime.now().isoformat(),
            "status": "active"
        }
        
        accounts[account_number] = account
        self._save_accounts(accounts)
        
        # Record initial deposit transaction if > 0
        if initial_deposit > 0:
            self._record_transaction(
                account_number, "deposit", initial_deposit, 
                "Initial deposit", account_number
            )
        
        return {
            "account_number": account_number,
            "name": name,
            "balance": initial_deposit,
            "status": "Account created successfully"
        }
    
    def authenticate(self, account_number: str, password: str) -> bool:
        """Authenticate account holder."""
        accounts = self._load_accounts()
        account = accounts.get(account_number)
        
        if not account:
            return False
        
        return account["password_hash"] == self._hash_password(password)
    
    def get_balance(self, account_number: str, password: str) -> Dict:
        """Get account balance."""
        if not self.authenticate(account_number, password):
            return {"error": "Invalid account number or password"}
        
        accounts = self._load_accounts()
        account = accounts.get(account_number)
        
        return {
            "account_number": account_number,
            "name": account["name"],
            "balance": account["balance"],
            "status": "success"
        }
    
    def deposit(self, account_number: str, amount: float, password: str, description: str = "Deposit") -> Dict:
        """Deposit money to account."""
        if amount <= 0:
            return {"error": "Deposit amount must be positive"}
        
        if not self.authenticate(account_number, password):
            return {"error": "Invalid account number or password"}
        
        accounts = self._load_accounts()
        account = accounts[account_number]
        
        old_balance = account["balance"]
        account["balance"] += amount
        accounts[account_number] = account
        self._save_accounts(accounts)
        
        # Record transaction
        self._record_transaction(account_number, "deposit", amount, description, account_number)
        
        return {
            "account_number": account_number,
            "transaction_type": "deposit",
            "amount": amount,
            "old_balance": old_balance,
            "new_balance": account["balance"],
            "status": "success"
        }
    
    def withdraw(self, account_number: str, amount: float, password: str, description: str = "Withdrawal") -> Dict:
        """Withdraw money from account."""
        if amount <= 0:
            return {"error": "Withdrawal amount must be positive"}
        
        if not self.authenticate(account_number, password):
            return {"error": "Invalid account number or password"}
        
        accounts = self._load_accounts()
        account = accounts[account_number]
        
        if account["balance"] < amount:
            return {"error": "Insufficient funds"}
        
        old_balance = account["balance"]
        account["balance"] -= amount
        accounts[account_number] = account
        self._save_accounts(accounts)
        
        # Record transaction
        self._record_transaction(account_number, "withdrawal", amount, description, account_number)
        
        return {
            "account_number": account_number,
            "transaction_type": "withdrawal",
            "amount": amount,
            "old_balance": old_balance,
            "new_balance": account["balance"],
            "status": "success"
        }
    
    def transfer(self, from_account: str, to_account: str, amount: float, 
                password: str, description: str = "Transfer") -> Dict:
        """Transfer money between accounts."""
        if amount <= 0:
            return {"error": "Transfer amount must be positive"}
        
        if from_account == to_account:
            return {"error": "Cannot transfer to the same account"}
        
        if not self.authenticate(from_account, password):
            return {"error": "Invalid account number or password"}
        
        accounts = self._load_accounts()
        
        if to_account not in accounts:
            return {"error": "Destination account does not exist"}
        
        from_acc = accounts[from_account]
        to_acc = accounts[to_account]
        
        if from_acc["balance"] < amount:
            return {"error": "Insufficient funds"}
        
        # Perform transfer
        old_from_balance = from_acc["balance"]
        old_to_balance = to_acc["balance"]
        
        from_acc["balance"] -= amount
        to_acc["balance"] += amount
        
        accounts[from_account] = from_acc
        accounts[to_account] = to_acc
        self._save_accounts(accounts)
        
        # Record transactions
        self._record_transaction(
            from_account, "transfer_out", amount, 
            f"{description} to {to_account}", to_account
        )
        self._record_transaction(
            to_account, "transfer_in", amount, 
            f"{description} from {from_account}", from_account
        )
        
        return {
            "from_account": from_account,
            "to_account": to_account,
            "amount": amount,
            "from_old_balance": old_from_balance,
            "from_new_balance": from_acc["balance"],
            "to_old_balance": old_to_balance,
            "to_new_balance": to_acc["balance"],
            "status": "success"
        }
    
    def _record_transaction(self, account_number: str, transaction_type: str, 
                          amount: float, description: str, related_account: str = None):
        """Record a transaction in the transaction history."""
        transactions = self._load_transactions()
        
        transaction = {
            "id": len(transactions) + 1,
            "account_number": account_number,
            "transaction_type": transaction_type,
            "amount": amount,
            "description": description,
            "related_account": related_account,
            "timestamp": datetime.datetime.now().isoformat(),
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        
        transactions.append(transaction)
        self._save_transactions(transactions)
    
    def get_transaction_history(self, account_number: str, password: str, 
                              limit: int = 10) -> Dict:
        """Get transaction history for an account."""
        if not self.authenticate(account_number, password):
            return {"error": "Invalid account number or password"}
        
        transactions = self._load_transactions()
        account_transactions = [
            t for t in transactions 
            if t["account_number"] == account_number
        ]
        
        # Sort by timestamp (most recent first)
        account_transactions.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Limit results
        if limit > 0:
            account_transactions = account_transactions[:limit]
        
        return {
            "account_number": account_number,
            "transactions": account_transactions,
            "total_transactions": len(account_transactions),
            "status": "success"
        }
    
    def get_account_info(self, account_number: str, password: str) -> Dict:
        """Get complete account information."""
        if not self.authenticate(account_number, password):
            return {"error": "Invalid account number or password"}
        
        accounts = self._load_accounts()
        account = accounts[account_number]
        
        return {
            "account_number": account_number,
            "name": account["name"],
            "balance": account["balance"],
            "created_date": account["created_date"],
            "status": account["status"],
            "info": "success"
        }
    
    def list_all_accounts(self) -> Dict:
        """List all accounts (for admin purposes - no password needed)."""
        accounts = self._load_accounts()
        
        account_list = []
        for acc_num, acc_data in accounts.items():
            account_list.append({
                "account_number": acc_num,
                "name": acc_data["name"],
                "balance": acc_data["balance"],
                "status": acc_data["status"],
                "created_date": acc_data["created_date"]
            })
        
        return {
            "accounts": account_list,
            "total_accounts": len(account_list),
            "status": "success"
        }
    
    def get_data_info(self) -> Dict:
        """Get information about where data is stored."""
        return {
            "data_directory": os.path.abspath(self.data_dir),
            "accounts_file": os.path.abspath(self.accounts_file),
            "transactions_file": os.path.abspath(self.transactions_file),
            "accounts_exist": os.path.exists(self.accounts_file),
            "transactions_exist": os.path.exists(self.transactions_file),
            "status": "success"
        }


if __name__ == "__main__":
    # Simple CLI interface for testing
    bank = DummyBank()
    
    print("=== Dummy Bank System ===")
    print("Data is stored in:", bank.get_data_info()["data_directory"])
    
    while True:
        print("\nOptions:")
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Transaction History")
        print("7. List All Accounts")
        print("8. Data Info")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        try:
            if choice == "1":
                name = input("Enter name: ").strip()
                initial_deposit = float(input("Enter initial deposit (0 for none): ").strip() or "0")
                password = input("Enter password: ").strip() or "password"
                result = bank.create_account(name, initial_deposit, password)
                print(f"Account created: {result}")
            
            elif choice == "2":
                account_num = input("Enter account number: ").strip()
                password = input("Enter password: ").strip()
                result = bank.get_balance(account_num, password)
                print(f"Balance info: {result}")
            
            elif choice == "3":
                account_num = input("Enter account number: ").strip()
                password = input("Enter password: ").strip()
                amount = float(input("Enter deposit amount: ").strip())
                result = bank.deposit(account_num, amount, password)
                print(f"Deposit result: {result}")
            
            elif choice == "4":
                account_num = input("Enter account number: ").strip()
                password = input("Enter password: ").strip()
                amount = float(input("Enter withdrawal amount: ").strip())
                result = bank.withdraw(account_num, amount, password)
                print(f"Withdrawal result: {result}")
            
            elif choice == "5":
                from_account = input("Enter from account number: ").strip()
                to_account = input("Enter to account number: ").strip()
                password = input("Enter password for from account: ").strip()
                amount = float(input("Enter transfer amount: ").strip())
                result = bank.transfer(from_account, to_account, amount, password)
                print(f"Transfer result: {result}")
            
            elif choice == "6":
                account_num = input("Enter account number: ").strip()
                password = input("Enter password: ").strip()
                limit = int(input("Enter number of transactions to show (10): ").strip() or "10")
                result = bank.get_transaction_history(account_num, password, limit)
                print(f"Transaction history: {result}")
            
            elif choice == "7":
                result = bank.list_all_accounts()
                print(f"All accounts: {result}")
            
            elif choice == "8":
                result = bank.get_data_info()
                print(f"Data information: {result}")
            
            elif choice == "9":
                print("Thank you for using Dummy Bank!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")