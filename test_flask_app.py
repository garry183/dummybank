#!/usr/bin/env python3
"""
Test Suite for Flask Web Application

Tests the web interface functionality including:
- Route handling and authentication
- Form submissions and validation
- Banking operations through web interface
- Error handling and session management
"""

import unittest
import tempfile
import shutil
import os
import sys
from app import app
from bank import DummyBank


class TestFlaskApp(unittest.TestCase):
    """Test the Flask web application."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SECRET_KEY'] = 'test-secret-key'
        
        # Create test client
        self.client = app.test_client()
        
        # Initialize bank with test data directory
        self.bank = DummyBank(data_dir=self.test_dir)
        
        # Replace the global bank instance in app with our test instance
        import app as app_module
        app_module.bank = self.bank
        
        # Create test account
        self.test_account = self.bank.create_account("Test User", 1000.0, "testpass")
        self.test_account_num = self.test_account["account_number"]
        
        # Create another account for transfer tests
        self.test_account2 = self.bank.create_account("Test User 2", 500.0, "testpass2")
        self.test_account_num2 = self.test_account2["account_number"]
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_home_route_redirect(self):
        """Test home route redirects to login when not authenticated."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_login_page_loads(self):
        """Test login page loads correctly."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login to Your Account', response.data)
        self.assertIn(b'Account Number', response.data)
        self.assertIn(b'Password', response.data)
    
    def test_register_page_loads(self):
        """Test registration page loads correctly."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Account', response.data)
        self.assertIn(b'Full Name', response.data)
        self.assertIn(b'Initial Deposit', response.data)
    
    def test_successful_login(self):
        """Test successful login flow."""
        response = self.client.post('/login', data={
            'account_number': self.test_account_num,
            'password': 'testpass'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, Test User', response.data)
        self.assertIn(b'Dashboard', response.data)
    
    def test_failed_login(self):
        """Test failed login with wrong credentials."""
        response = self.client.post('/login', data={
            'account_number': self.test_account_num,
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid account number or password', response.data)
    
    def test_account_registration(self):
        """Test new account registration."""
        response = self.client.post('/register', data={
            'name': 'New User',
            'password': 'newpass',
            'confirm_password': 'newpass',
            'initial_deposit': '250.00'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully', response.data)
        self.assertIn(b'Login', response.data)
    
    def test_registration_password_mismatch(self):
        """Test registration fails with password mismatch."""
        response = self.client.post('/register', data={
            'name': 'Test User',
            'password': 'pass1',
            'confirm_password': 'pass2',
            'initial_deposit': '100.00'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match', response.data)
    
    def test_dashboard_requires_login(self):
        """Test dashboard redirects to login when not authenticated."""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_dashboard_with_login(self):
        """Test dashboard loads correctly when authenticated."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, Test User', response.data)
        self.assertIn(b'$1000.00', response.data)  # Check balance display
    
    def test_deposit_operation(self):
        """Test deposit functionality through web interface."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.post('/deposit', data={
            'amount': '250.00',
            'description': 'Test deposit'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully deposited $250.00', response.data)
        
        # Verify balance updated
        balance_info = self.bank.get_balance(self.test_account_num, 'testpass')
        self.assertEqual(balance_info['balance'], 1250.0)
    
    def test_withdraw_operation(self):
        """Test withdrawal functionality through web interface."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.post('/withdraw', data={
            'amount': '200.00',
            'description': 'Test withdrawal'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully withdrew $200.00', response.data)
        
        # Verify balance updated
        balance_info = self.bank.get_balance(self.test_account_num, 'testpass')
        self.assertEqual(balance_info['balance'], 800.0)
    
    def test_transfer_operation(self):
        """Test transfer functionality through web interface."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.post('/transfer', data={
            'to_account': self.test_account_num2,
            'amount': '150.00',
            'description': 'Test transfer'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully transferred $150.00', response.data)
        
        # Verify balances updated
        balance1 = self.bank.get_balance(self.test_account_num, 'testpass')
        balance2 = self.bank.get_balance(self.test_account_num2, 'testpass2')
        self.assertEqual(balance1['balance'], 850.0)
        self.assertEqual(balance2['balance'], 650.0)
    
    def test_insufficient_funds_withdrawal(self):
        """Test withdrawal fails with insufficient funds."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.post('/withdraw', data={
            'amount': '2000.00',  # More than available balance
            'description': 'Large withdrawal'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Withdrawal failed', response.data)
    
    def test_transaction_history_page(self):
        """Test transaction history page loads correctly."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transaction History', response.data)
        self.assertIn(b'Initial deposit', response.data)  # Should show initial deposit
    
    def test_logout_functionality(self):
        """Test logout clears session and redirects."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logged out successfully', response.data)
        
        # Try to access dashboard after logout
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_invalid_deposit_amount(self):
        """Test deposit fails with invalid amount."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.post('/deposit', data={
            'amount': '-50.00',  # Negative amount
            'description': 'Invalid deposit'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deposit amount must be positive', response.data)
    
    def test_transfer_to_same_account_fails(self):
        """Test transfer to same account fails."""
        with self.client.session_transaction() as session:
            session['account_number'] = self.test_account_num
            session['password'] = 'testpass'
        
        response = self.client.post('/transfer', data={
            'to_account': self.test_account_num,  # Same account
            'amount': '100.00',
            'description': 'Self transfer'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transfer failed', response.data)
    
    def test_404_error_page(self):
        """Test 404 error page."""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
    
    def test_form_validation_empty_fields(self):
        """Test form validation with empty required fields."""
        response = self.client.post('/login', data={
            'account_number': '',
            'password': ''
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter both account number and password', response.data)


class TestWebIntegration(unittest.TestCase):
    """Integration tests for the complete web application."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test-secret-key'
        
        self.client = app.test_client()
        self.bank = DummyBank(data_dir=self.test_dir)
        
        # Replace global bank instance
        import app as app_module
        app_module.bank = self.bank
    
    def tearDown(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_complete_user_workflow(self):
        """Test complete user workflow: register -> login -> operations -> logout."""
        
        # Step 1: Register new account
        register_response = self.client.post('/register', data={
            'name': 'Integration Test User',
            'password': 'integrationpass',
            'confirm_password': 'integrationpass',
            'initial_deposit': '500.00'
        }, follow_redirects=True)
        
        self.assertEqual(register_response.status_code, 200)
        self.assertIn(b'Account created successfully', register_response.data)
        
        # Extract account number from response
        response_text = register_response.data.decode()
        import re
        match = re.search(r'Your account number is: (\d+)', response_text)
        if not match:
            self.fail("Could not extract account number from registration response")
        account_num = match.group(1)
        
        # Step 2: Login with new account
        login_response = self.client.post('/login', data={
            'account_number': account_num,
            'password': 'integrationpass'
        }, follow_redirects=True)
        
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Welcome, Integration Test User', login_response.data)
        
        # Step 3: Make a deposit
        deposit_response = self.client.post('/deposit', data={
            'amount': '200.00',
            'description': 'Integration test deposit'
        }, follow_redirects=True)
        
        self.assertEqual(deposit_response.status_code, 200)
        self.assertIn(b'Successfully deposited $200.00', deposit_response.data)
        
        # Step 4: Make a withdrawal
        withdraw_response = self.client.post('/withdraw', data={
            'amount': '150.00',
            'description': 'Integration test withdrawal'
        }, follow_redirects=True)
        
        self.assertEqual(withdraw_response.status_code, 200)
        self.assertIn(b'Successfully withdrew $150.00', withdraw_response.data)
        
        # Step 5: Check transaction history
        history_response = self.client.get('/transactions')
        self.assertEqual(history_response.status_code, 200)
        self.assertIn(b'Integration test deposit', history_response.data)
        self.assertIn(b'Integration test withdrawal', history_response.data)
        
        # Step 6: Logout
        logout_response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_response.status_code, 200)
        self.assertIn(b'logged out successfully', logout_response.data)


if __name__ == '__main__':
    # Create a test suite combining both test classes
    suite = unittest.TestSuite()
    
    # Add tests from both classes
    suite.addTest(unittest.makeSuite(TestFlaskApp))
    suite.addTest(unittest.makeSuite(TestWebIntegration))
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    if not result.wasSuccessful():
        sys.exit(1)
    else:
        print(f"\n✅ All {result.testsRun} web application tests passed!")