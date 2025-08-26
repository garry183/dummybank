#!/usr/bin/env python3
"""
Test suite for Dummy Bank Application

Tests all banking functionalities:
- Account creation and management
- Authentication
- Deposits and withdrawals
- Money transfers
- Transaction history
- Data persistence
"""

import unittest
import os
import shutil
import tempfile
import json
from bank import DummyBank


class TestDummyBank(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.bank = DummyBank(data_dir=self.test_dir)
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_data_storage_initialization(self):
        """Test that data files are properly created and initialized."""
        info = self.bank.get_data_info()
        
        # Check that data directory exists
        self.assertTrue(os.path.exists(info["data_directory"]))
        
        # Check that data files exist
        self.assertTrue(info["accounts_exist"])
        self.assertTrue(info["transactions_exist"])
        
        # Check file contents are valid JSON
        with open(info["accounts_file"], 'r') as f:
            accounts = json.load(f)
            self.assertIsInstance(accounts, dict)
        
        with open(info["transactions_file"], 'r') as f:
            transactions = json.load(f)
            self.assertIsInstance(transactions, list)
    
    def test_account_creation(self):
        """Test account creation functionality."""
        # Test normal account creation
        result = self.bank.create_account("John Doe", 100.0, "password123")
        
        self.assertEqual(result["status"], "Account created successfully")
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["balance"], 100.0)
        self.assertTrue("account_number" in result)
        
        # Verify account exists in storage
        accounts = self.bank._load_accounts()
        self.assertIn(result["account_number"], accounts)
        
        # Test account creation with no initial deposit
        result2 = self.bank.create_account("Jane Smith", 0.0, "password456")
        self.assertEqual(result2["balance"], 0.0)
        
        # Test invalid initial deposit
        with self.assertRaises(ValueError):
            self.bank.create_account("Invalid User", -50.0, "password")
    
    def test_authentication(self):
        """Test account authentication."""
        # Create test account
        account = self.bank.create_account("Test User", 50.0, "testpass")
        account_num = account["account_number"]
        
        # Test valid authentication
        self.assertTrue(self.bank.authenticate(account_num, "testpass"))
        
        # Test invalid password
        self.assertFalse(self.bank.authenticate(account_num, "wrongpass"))
        
        # Test invalid account number
        self.assertFalse(self.bank.authenticate("9999999999", "testpass"))
    
    def test_balance_inquiry(self):
        """Test balance checking functionality."""
        # Create test account
        account = self.bank.create_account("Balance User", 200.0, "balancepass")
        account_num = account["account_number"]
        
        # Test valid balance inquiry
        result = self.bank.get_balance(account_num, "balancepass")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["balance"], 200.0)
        self.assertEqual(result["name"], "Balance User")
        
        # Test invalid authentication
        result = self.bank.get_balance(account_num, "wrongpass")
        self.assertIn("error", result)
    
    def test_deposit(self):
        """Test deposit functionality."""
        # Create test account
        account = self.bank.create_account("Deposit User", 100.0, "depositpass")
        account_num = account["account_number"]
        
        # Test valid deposit
        result = self.bank.deposit(account_num, 50.0, "depositpass", "Test deposit")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["transaction_type"], "deposit")
        self.assertEqual(result["amount"], 50.0)
        self.assertEqual(result["old_balance"], 100.0)
        self.assertEqual(result["new_balance"], 150.0)
        
        # Verify balance updated
        balance = self.bank.get_balance(account_num, "depositpass")
        self.assertEqual(balance["balance"], 150.0)
        
        # Test invalid deposit amount
        result = self.bank.deposit(account_num, -10.0, "depositpass")
        self.assertIn("error", result)
        
        # Test invalid authentication
        result = self.bank.deposit(account_num, 25.0, "wrongpass")
        self.assertIn("error", result)
    
    def test_withdrawal(self):
        """Test withdrawal functionality."""
        # Create test account
        account = self.bank.create_account("Withdraw User", 200.0, "withdrawpass")
        account_num = account["account_number"]
        
        # Test valid withdrawal
        result = self.bank.withdraw(account_num, 75.0, "withdrawpass", "Test withdrawal")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["transaction_type"], "withdrawal")
        self.assertEqual(result["amount"], 75.0)
        self.assertEqual(result["old_balance"], 200.0)
        self.assertEqual(result["new_balance"], 125.0)
        
        # Verify balance updated
        balance = self.bank.get_balance(account_num, "withdrawpass")
        self.assertEqual(balance["balance"], 125.0)
        
        # Test insufficient funds
        result = self.bank.withdraw(account_num, 500.0, "withdrawpass")
        self.assertIn("error", result)
        self.assertIn("Insufficient funds", result["error"])
        
        # Test invalid withdrawal amount
        result = self.bank.withdraw(account_num, -25.0, "withdrawpass")
        self.assertIn("error", result)
        
        # Test invalid authentication
        result = self.bank.withdraw(account_num, 10.0, "wrongpass")
        self.assertIn("error", result)
    
    def test_transfer(self):
        """Test money transfer functionality."""
        # Create test accounts
        account1 = self.bank.create_account("Transfer User 1", 300.0, "transfer1pass")
        account2 = self.bank.create_account("Transfer User 2", 100.0, "transfer2pass")
        
        acc1_num = account1["account_number"]
        acc2_num = account2["account_number"]
        
        # Test valid transfer
        result = self.bank.transfer(acc1_num, acc2_num, 80.0, "transfer1pass", "Test transfer")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["amount"], 80.0)
        self.assertEqual(result["from_old_balance"], 300.0)
        self.assertEqual(result["from_new_balance"], 220.0)
        self.assertEqual(result["to_old_balance"], 100.0)
        self.assertEqual(result["to_new_balance"], 180.0)
        
        # Verify balances updated
        balance1 = self.bank.get_balance(acc1_num, "transfer1pass")
        balance2 = self.bank.get_balance(acc2_num, "transfer2pass")
        self.assertEqual(balance1["balance"], 220.0)
        self.assertEqual(balance2["balance"], 180.0)
        
        # Test insufficient funds
        result = self.bank.transfer(acc1_num, acc2_num, 500.0, "transfer1pass")
        self.assertIn("error", result)
        self.assertIn("Insufficient funds", result["error"])
        
        # Test transfer to non-existent account
        result = self.bank.transfer(acc1_num, "9999999999", 50.0, "transfer1pass")
        self.assertIn("error", result)
        
        # Test transfer to same account
        result = self.bank.transfer(acc1_num, acc1_num, 50.0, "transfer1pass")
        self.assertIn("error", result)
        
        # Test invalid authentication
        result = self.bank.transfer(acc1_num, acc2_num, 50.0, "wrongpass")
        self.assertIn("error", result)
    
    def test_transaction_history(self):
        """Test transaction history functionality."""
        # Create test account and perform transactions
        account = self.bank.create_account("History User", 100.0, "historypass")
        account_num = account["account_number"]
        
        # Perform some transactions
        self.bank.deposit(account_num, 50.0, "historypass", "Deposit 1")
        self.bank.withdraw(account_num, 25.0, "historypass", "Withdrawal 1")
        self.bank.deposit(account_num, 30.0, "historypass", "Deposit 2")
        
        # Get transaction history
        result = self.bank.get_transaction_history(account_num, "historypass", 10)
        self.assertEqual(result["status"], "success")
        self.assertGreaterEqual(len(result["transactions"]), 4)  # Initial deposit + 3 transactions
        
        # Verify transaction details
        transactions = result["transactions"]
        self.assertTrue(any(t["description"] == "Deposit 1" for t in transactions))
        self.assertTrue(any(t["description"] == "Withdrawal 1" for t in transactions))
        self.assertTrue(any(t["description"] == "Deposit 2" for t in transactions))
        
        # Test with limit
        result = self.bank.get_transaction_history(account_num, "historypass", 2)
        self.assertEqual(len(result["transactions"]), 2)
        
        # Test invalid authentication
        result = self.bank.get_transaction_history(account_num, "wrongpass")
        self.assertIn("error", result)
    
    def test_account_info(self):
        """Test account information retrieval."""
        # Create test account
        account = self.bank.create_account("Info User", 150.0, "infopass")
        account_num = account["account_number"]
        
        # Get account info
        result = self.bank.get_account_info(account_num, "infopass")
        self.assertEqual(result["info"], "success")
        self.assertEqual(result["name"], "Info User")
        self.assertEqual(result["balance"], 150.0)
        self.assertEqual(result["status"], "active")
        self.assertTrue("created_date" in result)
        
        # Test invalid authentication
        result = self.bank.get_account_info(account_num, "wrongpass")
        self.assertIn("error", result)
    
    def test_list_all_accounts(self):
        """Test listing all accounts functionality."""
        # Create multiple accounts
        account1 = self.bank.create_account("User 1", 100.0, "pass1")
        account2 = self.bank.create_account("User 2", 200.0, "pass2")
        account3 = self.bank.create_account("User 3", 300.0, "pass3")
        
        # List all accounts
        result = self.bank.list_all_accounts()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total_accounts"], 3)
        
        # Verify account details in list
        accounts = result["accounts"]
        account_numbers = [acc["account_number"] for acc in accounts]
        self.assertIn(account1["account_number"], account_numbers)
        self.assertIn(account2["account_number"], account_numbers)
        self.assertIn(account3["account_number"], account_numbers)
    
    def test_data_persistence(self):
        """Test that data is properly persisted to files."""
        # Create account and perform transactions
        account = self.bank.create_account("Persistence User", 100.0, "persistpass")
        account_num = account["account_number"]
        
        self.bank.deposit(account_num, 50.0, "persistpass", "Test persistence")
        
        # Create new bank instance with same data directory
        new_bank = DummyBank(data_dir=self.test_dir)
        
        # Verify data persisted
        balance = new_bank.get_balance(account_num, "persistpass")
        self.assertEqual(balance["balance"], 150.0)
        
        history = new_bank.get_transaction_history(account_num, "persistpass")
        self.assertEqual(len(history["transactions"]), 2)  # Initial deposit + test deposit
    
    def test_edge_cases(self):
        """Test various edge cases and error conditions."""
        # Test with zero amounts
        account = self.bank.create_account("Edge User", 100.0, "edgepass")
        account_num = account["account_number"]
        
        # Zero deposit
        result = self.bank.deposit(account_num, 0.0, "edgepass")
        self.assertIn("error", result)
        
        # Zero withdrawal
        result = self.bank.withdraw(account_num, 0.0, "edgepass")
        self.assertIn("error", result)
        
        # Zero transfer
        account2 = self.bank.create_account("Edge User 2", 50.0, "edgepass2")
        result = self.bank.transfer(account_num, account2["account_number"], 0.0, "edgepass")
        self.assertIn("error", result)


class TestDataLocation(unittest.TestCase):
    """Test data storage location and format."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.bank = DummyBank(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_data_files_location(self):
        """Test that data files are created in the correct location."""
        info = self.bank.get_data_info()
        
        # Check paths
        expected_accounts_file = os.path.join(self.test_dir, "accounts.json")
        expected_transactions_file = os.path.join(self.test_dir, "transactions.json")
        
        self.assertEqual(info["accounts_file"], os.path.abspath(expected_accounts_file))
        self.assertEqual(info["transactions_file"], os.path.abspath(expected_transactions_file))
    
    def test_data_format(self):
        """Test that data is stored in the correct JSON format."""
        # Create account and perform transaction
        account = self.bank.create_account("Format User", 100.0, "formatpass")
        account_num = account["account_number"]
        self.bank.deposit(account_num, 25.0, "formatpass", "Format test")
        
        # Check accounts.json format
        with open(self.bank.accounts_file, 'r') as f:
            accounts_data = json.load(f)
        
        self.assertIsInstance(accounts_data, dict)
        self.assertIn(account_num, accounts_data)
        
        account_data = accounts_data[account_num]
        required_fields = ["account_number", "name", "balance", "password_hash", "created_date", "status"]
        for field in required_fields:
            self.assertIn(field, account_data)
        
        # Check transactions.json format
        with open(self.bank.transactions_file, 'r') as f:
            transactions_data = json.load(f)
        
        self.assertIsInstance(transactions_data, list)
        self.assertGreater(len(transactions_data), 0)
        
        transaction = transactions_data[0]
        required_fields = ["id", "account_number", "transaction_type", "amount", "description", "timestamp", "date"]
        for field in required_fields:
            self.assertIn(field, transaction)


if __name__ == "__main__":
    print("Running Dummy Bank Test Suite...")
    print("="*50)
    
    # Run all tests
    unittest.main(verbosity=2)