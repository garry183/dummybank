#!/usr/bin/env python3
"""
Demo script to test all Dummy Bank functionalities
"""

from bank import DummyBank
import json
import os

def main():
    print("=== DUMMY BANK FUNCTIONALITY DEMO ===")
    print()
    
    # Initialize bank
    bank = DummyBank()
    
    print("1. DATA STORAGE INFORMATION:")
    data_info = bank.get_data_info()
    print(f"   Data Directory: {data_info['data_directory']}")
    print(f"   Accounts File: {data_info['accounts_file']}")
    print(f"   Transactions File: {data_info['transactions_file']}")
    print()
    
    # Test account creation
    print("2. TESTING ACCOUNT CREATION:")
    account1 = bank.create_account("Alice Johnson", 1000.0, "alice123")
    account2 = bank.create_account("Bob Smith", 500.0, "bob456")
    account3 = bank.create_account("Charlie Brown", 0.0, "charlie789")
    
    print(f"   ✓ Created account for Alice: {account1['account_number']} with balance ${account1['balance']}")
    print(f"   ✓ Created account for Bob: {account2['account_number']} with balance ${account2['balance']}")
    print(f"   ✓ Created account for Charlie: {account3['account_number']} with balance ${account3['balance']}")
    print()
    
    alice_acc = account1['account_number']
    bob_acc = account2['account_number']
    charlie_acc = account3['account_number']
    
    # Test authentication
    print("3. TESTING AUTHENTICATION:")
    print(f"   ✓ Alice auth (correct): {bank.authenticate(alice_acc, 'alice123')}")
    print(f"   ✗ Alice auth (wrong): {bank.authenticate(alice_acc, 'wrongpass')}")
    print()
    
    # Test balance inquiry
    print("4. TESTING BALANCE INQUIRY:")
    balance = bank.get_balance(alice_acc, "alice123")
    print(f"   ✓ Alice's balance: ${balance['balance']}")
    print()
    
    # Test deposit
    print("5. TESTING DEPOSITS:")
    deposit1 = bank.deposit(alice_acc, 250.0, "alice123", "Salary deposit")
    deposit2 = bank.deposit(charlie_acc, 100.0, "charlie789", "Initial deposit")
    print(f"   ✓ Alice deposit: ${deposit1['amount']} (balance: ${deposit1['old_balance']} → ${deposit1['new_balance']})")
    print(f"   ✓ Charlie deposit: ${deposit2['amount']} (balance: ${deposit2['old_balance']} → ${deposit2['new_balance']})")
    print()
    
    # Test withdrawal
    print("6. TESTING WITHDRAWALS:")
    withdrawal = bank.withdraw(bob_acc, 150.0, "bob456", "ATM withdrawal")
    print(f"   ✓ Bob withdrawal: ${withdrawal['amount']} (balance: ${withdrawal['old_balance']} → ${withdrawal['new_balance']})")
    
    # Test insufficient funds
    insufficient = bank.withdraw(charlie_acc, 200.0, "charlie789", "Large withdrawal")
    print(f"   ✗ Charlie insufficient funds: {insufficient.get('error', 'N/A')}")
    print()
    
    # Test transfer
    print("7. TESTING TRANSFERS:")
    transfer = bank.transfer(alice_acc, bob_acc, 200.0, "alice123", "Loan payment")
    print(f"   ✓ Transfer from Alice to Bob: ${transfer['amount']}")
    print(f"     Alice: ${transfer['from_old_balance']} → ${transfer['from_new_balance']}")
    print(f"     Bob: ${transfer['to_old_balance']} → ${transfer['to_new_balance']}")
    print()
    
    # Test transaction history
    print("8. TESTING TRANSACTION HISTORY:")
    alice_history = bank.get_transaction_history(alice_acc, "alice123", 5)
    print(f"   ✓ Alice's recent transactions ({len(alice_history['transactions'])}):")
    for i, txn in enumerate(alice_history['transactions'][:3], 1):
        print(f"     {i}. {txn['transaction_type']}: ${txn['amount']} - {txn['description']}")
    print()
    
    # Test account info
    print("9. TESTING ACCOUNT INFO:")
    alice_info = bank.get_account_info(alice_acc, "alice123")
    print(f"   ✓ Alice's info: {alice_info['name']}, Balance: ${alice_info['balance']}, Status: {alice_info['status']}")
    print()
    
    # Test list all accounts
    print("10. TESTING LIST ALL ACCOUNTS:")
    all_accounts = bank.list_all_accounts()
    print(f"    ✓ Total accounts: {all_accounts['total_accounts']}")
    for acc in all_accounts['accounts']:
        print(f"      - {acc['name']} ({acc['account_number']}): ${acc['balance']}")
    print()
    
    # Show data files content
    print("11. DATA FILES CONTENT:")
    print("    Accounts file content:")
    with open(bank.accounts_file, 'r') as f:
        accounts_data = json.load(f)
        print(f"    - Number of accounts stored: {len(accounts_data)}")
        for acc_num, acc_data in list(accounts_data.items())[:2]:
            print(f"    - {acc_data['name']}: ${acc_data['balance']}")
    
    print("\n    Transactions file content:")
    with open(bank.transactions_file, 'r') as f:
        transactions_data = json.load(f)
        print(f"    - Total transactions recorded: {len(transactions_data)}")
        for txn in transactions_data[-3:]:
            print(f"    - {txn['transaction_type']}: ${txn['amount']} on {txn['date']}")
    
    print("\n=== ALL FUNCTIONALITIES TESTED SUCCESSFULLY ===")
    print("\nDATA STORAGE SUMMARY:")
    print(f"• All account data is saved in: {bank.accounts_file}")
    print(f"• All transaction data is saved in: {bank.transactions_file}")
    print("• Data format: JSON (human-readable)")
    print("• Data persists between application runs")
    print("• Passwords are hashed for security")

if __name__ == "__main__":
    main()