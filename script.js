// DummyBank JavaScript Application

// Global variables
let currentUser = null;
let users = JSON.parse(localStorage.getItem('dummybank_users')) || {};
let accounts = JSON.parse(localStorage.getItem('dummybank_accounts')) || {};
let transactions = JSON.parse(localStorage.getItem('dummybank_transactions')) || {};
let investments = JSON.parse(localStorage.getItem('dummybank_investments')) || {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check if user is already logged in
    const loggedInUser = localStorage.getItem('dummybank_current_user');
    if (loggedInUser) {
        currentUser = loggedInUser;
        showLoggedInState();
        showSection('dashboard');
    } else {
        showSection('home');
    }

    // Add event listeners
    document.getElementById('signup-form').addEventListener('submit', handleSignup);
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('transfer-form').addEventListener('submit', handleTransfer);
}

function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.style.display = 'none');

    // Show the selected section
    const targetSection = document.getElementById(sectionName + '-section');
    if (targetSection) {
        targetSection.style.display = 'block';
        targetSection.classList.add('fade-in');
    }

    // Update navigation
    updateNavigation(sectionName);

    // Load section-specific data
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'accounts':
            loadAccounts();
            break;
        case 'transfer':
            loadTransferOptions();
            break;
        case 'investments':
            loadInvestments();
            break;
    }
}

function updateNavigation(activeSection) {
    // Remove active class from all nav items
    const navItems = document.querySelectorAll('.nav-link');
    navItems.forEach(item => item.classList.remove('active'));

    // Add active class to current section
    const activeNav = document.querySelector(`[onclick="showSection('${activeSection}')"]`);
    if (activeNav) {
        activeNav.classList.add('active');
    }
}

function showLoggedInState() {
    document.getElementById('nav-login').style.display = 'none';
    document.getElementById('nav-signup').style.display = 'none';
    document.getElementById('nav-logout').style.display = 'block';
    document.getElementById('nav-username').style.display = 'block';
    document.getElementById('nav-dashboard').style.display = 'block';
    document.getElementById('nav-accounts').style.display = 'block';
    document.getElementById('nav-transfer').style.display = 'block';
    document.getElementById('nav-investments').style.display = 'block';
    
    document.getElementById('username-display').textContent = `Welcome, ${users[currentUser].name}!`;
}

function showLoggedOutState() {
    document.getElementById('nav-login').style.display = 'block';
    document.getElementById('nav-signup').style.display = 'block';
    document.getElementById('nav-logout').style.display = 'none';
    document.getElementById('nav-username').style.display = 'none';
    document.getElementById('nav-dashboard').style.display = 'none';
    document.getElementById('nav-accounts').style.display = 'none';
    document.getElementById('nav-transfer').style.display = 'none';
    document.getElementById('nav-investments').style.display = 'none';
}

function handleSignup(event) {
    event.preventDefault();
    
    const name = document.getElementById('signup-name').value.trim();
    const phone = document.getElementById('signup-phone').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;

    // Validation
    if (!name || !phone || !email || !password) {
        showAlert('Please fill in all fields', 'danger');
        return;
    }

    if (users[name]) {
        showAlert('User with this name already exists', 'danger');
        return;
    }

    // Create new user
    users[name] = {
        name: name,
        phone: phone,
        email: email,
        password: password,
        createdAt: new Date().toISOString()
    };

    // Save to localStorage
    localStorage.setItem('dummybank_users', JSON.stringify(users));

    showAlert('Account created successfully! Please login.', 'success');
    document.getElementById('signup-form').reset();
    showSection('login');
}

function handleLogin(event) {
    event.preventDefault();
    
    const name = document.getElementById('login-name').value.trim();
    const password = document.getElementById('login-password').value;

    // Validation
    if (!name || !password) {
        showAlert('Please fill in all fields', 'danger');
        return;
    }

    if (!users[name]) {
        showAlert('User not found', 'danger');
        return;
    }

    if (users[name].password !== password) {
        showAlert('Invalid password', 'danger');
        return;
    }

    // Login successful
    currentUser = name;
    localStorage.setItem('dummybank_current_user', currentUser);
    
    showLoggedInState();
    showAlert('Login successful!', 'success');
    document.getElementById('login-form').reset();
    showSection('dashboard');
}

function logout() {
    currentUser = null;
    localStorage.removeItem('dummybank_current_user');
    showLoggedOutState();
    showSection('home');
    showAlert('Logged out successfully!', 'info');
}

function loadDashboard() {
    if (!currentUser) return;

    const userAccounts = getUserAccounts();
    const summaryHtml = generateAccountSummary(userAccounts);
    document.getElementById('account-summary').innerHTML = summaryHtml;
}

function getUserAccounts() {
    if (!accounts[currentUser]) return [];
    return accounts[currentUser];
}

function generateAccountSummary(userAccounts) {
    if (userAccounts.length === 0) {
        return `
            <div class="text-center">
                <p class="text-muted">No accounts found.</p>
                <button class="btn btn-primary" onclick="showCreateAccountModal()">
                    <i class="fas fa-plus"></i> Open Your First Account
                </button>
            </div>
        `;
    }

    let totalBalance = 0;
    let html = '';

    userAccounts.forEach(account => {
        totalBalance += account.balance;
        html += `
            <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                    <strong>${account.type === 'savings' ? 'Savings' : 'Current'} Account</strong>
                    <div class="text-muted fs-7">${account.accountNumber}</div>
                </div>
                <div class="balance-amount">₹${account.balance.toLocaleString()}</div>
            </div>
        `;
    });

    return `
        <div class="mb-3">
            <div class="d-flex justify-content-between align-items-center">
                <h6>Total Balance</h6>
                <span class="balance-amount">₹${totalBalance.toLocaleString()}</span>
            </div>
        </div>
        <hr>
        ${html}
    `;
}

function loadAccounts() {
    if (!currentUser) return;

    const userAccounts = getUserAccounts();
    let html = '';

    if (userAccounts.length === 0) {
        html = `
            <div class="text-center py-5">
                <i class="fas fa-university fa-3x text-muted mb-3"></i>
                <h5>No accounts found</h5>
                <p class="text-muted">Open your first account to get started with DummyBank</p>
                <button class="btn btn-primary" onclick="showCreateAccountModal()">
                    <i class="fas fa-plus"></i> Open Account
                </button>
            </div>
        `;
    } else {
        userAccounts.forEach(account => {
            const accountClass = account.type === 'savings' ? 'savings-account' : 'current-account';
            html += `
                <div class="card account-card ${accountClass} mb-3">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <h5 class="card-title">
                                    <i class="fas fa-university"></i> 
                                    ${account.type === 'savings' ? 'Savings' : 'Current'} Account
                                </h5>
                                <p class="card-text">
                                    <strong>Account Number:</strong> ${account.accountNumber}<br>
                                    <strong>Balance:</strong> <span class="balance-amount">₹${account.balance.toLocaleString()}</span><br>
                                    <strong>Opened:</strong> ${new Date(account.createdAt).toLocaleDateString()}
                                </p>
                            </div>
                            <div class="col-md-4 text-end">
                                <button class="btn btn-success btn-sm me-1" onclick="showAddMoneyModal('${account.accountNumber}')">
                                    <i class="fas fa-plus"></i> Add Money
                                </button>
                                <button class="btn btn-warning btn-sm me-1" onclick="showWithdrawModal('${account.accountNumber}')">
                                    <i class="fas fa-minus"></i> Withdraw
                                </button>
                                <button class="btn btn-info btn-sm" onclick="showTransactionHistory('${account.accountNumber}')">
                                    <i class="fas fa-history"></i> History
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
    }

    document.getElementById('accounts-list').innerHTML = html;
}

function loadTransferOptions() {
    if (!currentUser) return;

    const userAccounts = getUserAccounts();
    const fromSelect = document.getElementById('from-account');
    const toSelect = document.getElementById('to-account');

    // Clear existing options
    fromSelect.innerHTML = '<option value="">Select Account</option>';
    toSelect.innerHTML = '<option value="">Select Account</option>';

    // Add user's accounts
    userAccounts.forEach(account => {
        const option = `<option value="${account.accountNumber}">${account.type === 'savings' ? 'Savings' : 'Current'} - ${account.accountNumber} (₹${account.balance.toLocaleString()})</option>`;
        fromSelect.innerHTML += option;
        toSelect.innerHTML += option;
    });

    // Add other users' accounts for transfer
    Object.keys(accounts).forEach(username => {
        if (username !== currentUser && accounts[username]) {
            accounts[username].forEach(account => {
                const option = `<option value="${account.accountNumber}">${username}'s ${account.type === 'savings' ? 'Savings' : 'Current'} - ${account.accountNumber}</option>`;
                toSelect.innerHTML += option;
            });
        }
    });
}

function handleTransfer(event) {
    event.preventDefault();

    const fromAccount = document.getElementById('from-account').value;
    const toAccount = document.getElementById('to-account').value;
    const amount = parseFloat(document.getElementById('transfer-amount').value);
    const note = document.getElementById('transfer-note').value || 'Money transfer';

    // Validation
    if (!fromAccount || !toAccount || !amount || amount <= 0) {
        showAlert('Please fill in all required fields with valid amounts', 'danger');
        return;
    }

    if (fromAccount === toAccount) {
        showAlert('Cannot transfer to the same account', 'danger');
        return;
    }

    // Find source account
    const sourceAccount = findAccount(fromAccount);
    if (!sourceAccount || sourceAccount.owner !== currentUser) {
        showAlert('Invalid source account', 'danger');
        return;
    }

    // Check balance
    if (sourceAccount.balance < amount) {
        showAlert('Insufficient balance', 'danger');
        return;
    }

    // Find destination account
    const destAccount = findAccount(toAccount);
    if (!destAccount) {
        showAlert('Invalid destination account', 'danger');
        return;
    }

    // Perform transfer
    sourceAccount.balance -= amount;
    destAccount.balance += amount;

    // Record transactions
    recordTransaction(fromAccount, -amount, `Transfer to ${toAccount}`, note);
    recordTransaction(toAccount, amount, `Transfer from ${fromAccount}`, note);

    // Save data
    saveAccounts();
    saveTransactions();

    showAlert('Transfer successful!', 'success');
    document.getElementById('transfer-form').reset();
    loadTransferOptions();
}

function findAccount(accountNumber) {
    for (const username in accounts) {
        if (accounts[username]) {
            for (const account of accounts[username]) {
                if (account.accountNumber === accountNumber) {
                    return { ...account, owner: username };
                }
            }
        }
    }
    return null;
}

function recordTransaction(accountNumber, amount, type, note) {
    if (!transactions[accountNumber]) {
        transactions[accountNumber] = [];
    }

    transactions[accountNumber].unshift({
        id: generateId(),
        amount: amount,
        type: type,
        note: note,
        date: new Date().toISOString(),
        balance: findAccount(accountNumber).balance + amount
    });

    // Keep only last 100 transactions
    if (transactions[accountNumber].length > 100) {
        transactions[accountNumber] = transactions[accountNumber].slice(0, 100);
    }
}

function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

function generateAccountNumber() {
    return 'DB' + Date.now().toString().substr(-8) + Math.floor(Math.random() * 1000).toString().padStart(3, '0');
}

function saveAccounts() {
    localStorage.setItem('dummybank_accounts', JSON.stringify(accounts));
}

function saveTransactions() {
    localStorage.setItem('dummybank_transactions', JSON.stringify(transactions));
}

function saveInvestments() {
    localStorage.setItem('dummybank_investments', JSON.stringify(investments));
}

function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    // Add new alert at the top of the container
    const container = document.querySelector('.container');
    container.insertAdjacentHTML('afterbegin', alertHtml);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

function populateAccountSelect(selectElement) {
    selectElement.innerHTML = '<option value="">Select Account</option>';
    
    const userAccounts = getUserAccounts();
    userAccounts.forEach(account => {
        const option = `<option value="${account.accountNumber}">${account.type === 'savings' ? 'Savings' : 'Current'} - ${account.accountNumber} (₹${account.balance.toLocaleString()})</option>`;
        selectElement.innerHTML += option;
    });
}

// Modal show functions
function showCreateAccountModal() {
    const modal = new bootstrap.Modal(document.getElementById('createAccountModal'));
    modal.show();
}

function showAddMoneyModal(accountNumber = null) {
    const modal = new bootstrap.Modal(document.getElementById('addMoneyModal'));
    const select = document.getElementById('modal-add-money-account');
    
    // Populate account options
    populateAccountSelect(select);
    
    // Pre-select account if provided
    if (accountNumber) {
        select.value = accountNumber;
    }
    
    modal.show();
}

function showWithdrawModal(accountNumber = null) {
    const modal = new bootstrap.Modal(document.getElementById('withdrawModal'));
    const select = document.getElementById('modal-withdraw-account');
    
    // Populate account options
    populateAccountSelect(select);
    
    // Pre-select account if provided
    if (accountNumber) {
        select.value = accountNumber;
    }
    
    modal.show();
}

function showFDModal() {
    const modal = new bootstrap.Modal(document.getElementById('fdModal'));
    const select = document.getElementById('modal-fd-account');
    populateAccountSelect(select);
    modal.show();
}

function showRDModal() {
    const modal = new bootstrap.Modal(document.getElementById('rdModal'));
    const select = document.getElementById('modal-rd-account');
    populateAccountSelect(select);
    modal.show();
}

// Modal action functions
function createAccount() {
    const accountType = document.querySelector('input[name="accountType"]:checked').value;
    const initialDeposit = parseFloat(document.getElementById('modal-initial-deposit').value) || 0;

    if (initialDeposit < 0) {
        showAlert('Initial deposit cannot be negative', 'danger');
        return;
    }

    // Initialize user accounts if not exists
    if (!accounts[currentUser]) {
        accounts[currentUser] = [];
    }

    // Create new account
    const newAccount = {
        accountNumber: generateAccountNumber(),
        type: accountType,
        balance: initialDeposit,
        createdAt: new Date().toISOString()
    };

    accounts[currentUser].push(newAccount);
    
    // Record initial deposit transaction if amount > 0
    if (initialDeposit > 0) {
        recordTransaction(newAccount.accountNumber, initialDeposit, 'Initial Deposit', 'Account opening deposit');
    }

    saveAccounts();
    saveTransactions();

    showAlert(`${accountType === 'savings' ? 'Savings' : 'Current'} account created successfully! Account Number: ${newAccount.accountNumber}`, 'success');
    
    // Close modal and refresh accounts
    const modal = bootstrap.Modal.getInstance(document.getElementById('createAccountModal'));
    modal.hide();
    document.getElementById('create-account-form').reset();
    
    loadAccounts();
    loadDashboard();
}

function addMoney() {
    const accountNumber = document.getElementById('modal-add-money-account').value;
    const amount = parseFloat(document.getElementById('modal-add-money-amount').value);
    const note = document.getElementById('modal-add-money-note').value || 'Money added';

    if (!accountNumber || !amount || amount <= 0) {
        showAlert('Please fill in all required fields', 'danger');
        return;
    }

    // Find and update account
    const userAccounts = getUserAccounts();
    const account = userAccounts.find(acc => acc.accountNumber === accountNumber);
    
    if (!account) {
        showAlert('Account not found', 'danger');
        return;
    }

    account.balance += amount;
    recordTransaction(accountNumber, amount, 'Money Added', note);

    saveAccounts();
    saveTransactions();

    showAlert(`₹${amount.toLocaleString()} added successfully!`, 'success');
    
    // Close modal and refresh
    const modal = bootstrap.Modal.getInstance(document.getElementById('addMoneyModal'));
    modal.hide();
    document.getElementById('modal-add-money-form').reset();
    
    loadAccounts();
    loadDashboard();
}

function withdrawMoney() {
    const accountNumber = document.getElementById('modal-withdraw-account').value;
    const amount = parseFloat(document.getElementById('modal-withdraw-amount').value);
    const note = document.getElementById('modal-withdraw-note').value || 'Money withdrawn';

    if (!accountNumber || !amount || amount <= 0) {
        showAlert('Please fill in all required fields', 'danger');
        return;
    }

    // Find account
    const userAccounts = getUserAccounts();
    const account = userAccounts.find(acc => acc.accountNumber === accountNumber);
    
    if (!account) {
        showAlert('Account not found', 'danger');
        return;
    }

    if (account.balance < amount) {
        showAlert('Insufficient balance', 'danger');
        return;
    }

    account.balance -= amount;
    recordTransaction(accountNumber, -amount, 'Money Withdrawn', note);

    saveAccounts();
    saveTransactions();

    showAlert(`₹${amount.toLocaleString()} withdrawn successfully!`, 'success');
    
    // Close modal and refresh
    const modal = bootstrap.Modal.getInstance(document.getElementById('withdrawModal'));
    modal.hide();
    document.getElementById('modal-withdraw-form').reset();
    
    loadAccounts();
    loadDashboard();
}

function openFD() {
    const accountNumber = document.getElementById('modal-fd-account').value;
    const amount = parseFloat(document.getElementById('modal-fd-amount').value);
    const tenureMonths = parseInt(document.getElementById('modal-fd-tenure').value);

    if (!accountNumber || !amount || !tenureMonths || amount < 1000) {
        showAlert('Please fill in all fields with valid amounts (minimum ₹1,000)', 'danger');
        return;
    }

    // Find source account
    const userAccounts = getUserAccounts();
    const account = userAccounts.find(acc => acc.accountNumber === accountNumber);
    
    if (!account || account.balance < amount) {
        showAlert('Insufficient balance in source account', 'danger');
        return;
    }

    // Interest rates
    const interestRates = { 6: 5, 12: 6, 24: 7, 36: 8, 60: 9 };
    const interestRate = interestRates[tenureMonths];
    
    // Calculate maturity amount
    const maturityAmount = amount * (1 + (interestRate * tenureMonths) / (100 * 12));
    
    // Deduct from source account
    account.balance -= amount;
    
    // Create FD
    if (!investments[currentUser]) {
        investments[currentUser] = [];
    }

    const fd = {
        id: generateId(),
        type: 'FD',
        amount: amount,
        interestRate: interestRate,
        tenure: tenureMonths,
        maturityAmount: Math.round(maturityAmount),
        startDate: new Date().toISOString(),
        maturityDate: new Date(Date.now() + tenureMonths * 30 * 24 * 60 * 60 * 1000).toISOString(),
        status: 'Active',
        sourceAccount: accountNumber
    };

    investments[currentUser].push(fd);
    
    // Record transaction
    recordTransaction(accountNumber, -amount, 'Fixed Deposit', `FD opened - ID: ${fd.id}`);

    saveAccounts();
    saveInvestments();
    saveTransactions();

    showAlert(`Fixed Deposit of ₹${amount.toLocaleString()} opened successfully! Maturity Amount: ₹${fd.maturityAmount.toLocaleString()}`, 'success');
    
    // Close modal and refresh
    const modal = bootstrap.Modal.getInstance(document.getElementById('fdModal'));
    modal.hide();
    document.getElementById('modal-fd-form').reset();
    
    loadInvestments();
    loadAccounts();
    loadDashboard();
}

function openRD() {
    const accountNumber = document.getElementById('modal-rd-account').value;
    const monthlyAmount = parseFloat(document.getElementById('modal-rd-amount').value);
    const tenureMonths = parseInt(document.getElementById('modal-rd-tenure').value);

    if (!accountNumber || !monthlyAmount || !tenureMonths || monthlyAmount < 500) {
        showAlert('Please fill in all fields with valid amounts (minimum ₹500)', 'danger');
        return;
    }

    // Find source account
    const userAccounts = getUserAccounts();
    const account = userAccounts.find(acc => acc.accountNumber === accountNumber);
    
    if (!account || account.balance < monthlyAmount) {
        showAlert('Insufficient balance for first installment', 'danger');
        return;
    }

    // Interest rates
    const interestRates = { 12: 6.5, 24: 7.5, 36: 8.5, 60: 9.5 };
    const interestRate = interestRates[tenureMonths];
    
    // Calculate maturity amount (compound interest formula for RD)
    const totalAmount = monthlyAmount * tenureMonths;
    const maturityAmount = totalAmount * (1 + (interestRate * tenureMonths) / (100 * 12));
    
    // Deduct first installment
    account.balance -= monthlyAmount;
    
    // Create RD
    if (!investments[currentUser]) {
        investments[currentUser] = [];
    }

    const rd = {
        id: generateId(),
        type: 'RD',
        monthlyAmount: monthlyAmount,
        paidAmount: monthlyAmount,
        interestRate: interestRate,
        tenure: tenureMonths,
        maturityAmount: Math.round(maturityAmount),
        startDate: new Date().toISOString(),
        maturityDate: new Date(Date.now() + tenureMonths * 30 * 24 * 60 * 60 * 1000).toISOString(),
        nextInstallment: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
        status: 'Active',
        sourceAccount: accountNumber,
        installmentsPaid: 1
    };

    investments[currentUser].push(rd);
    
    // Record transaction
    recordTransaction(accountNumber, -monthlyAmount, 'Recurring Deposit', `RD opened - ID: ${rd.id} (1st installment)`);

    saveAccounts();
    saveInvestments();
    saveTransactions();

    showAlert(`Recurring Deposit of ₹${monthlyAmount.toLocaleString()}/month opened successfully! Maturity Amount: ₹${rd.maturityAmount.toLocaleString()}`, 'success');
    
    // Close modal and refresh
    const modal = bootstrap.Modal.getInstance(document.getElementById('rdModal'));
    modal.hide();
    document.getElementById('modal-rd-form').reset();
    
    loadInvestments();
    loadAccounts();
    loadDashboard();
}

function loadInvestments() {
    if (!currentUser) return;

    const userInvestments = investments[currentUser] || [];
    let html = '';

    if (userInvestments.length === 0) {
        html = `
            <div class="text-center py-5">
                <i class="fas fa-chart-line fa-3x text-muted mb-3"></i>
                <h5>No investments found</h5>
                <p class="text-muted">Start investing to secure your future</p>
            </div>
        `;
    } else {
        userInvestments.forEach(investment => {
            const cardClass = investment.type === 'FD' ? 'fd-card' : 'rd-card';
            const icon = investment.type === 'FD' ? 'fas fa-piggy-bank' : 'fas fa-calendar-check';
            
            let details = '';
            if (investment.type === 'FD') {
                details = `
                    <strong>Amount:</strong> ₹${investment.amount.toLocaleString()}<br>
                    <strong>Interest Rate:</strong> ${investment.interestRate}%<br>
                    <strong>Maturity Amount:</strong> ₹${investment.maturityAmount.toLocaleString()}
                `;
            } else {
                details = `
                    <strong>Monthly Amount:</strong> ₹${investment.monthlyAmount.toLocaleString()}<br>
                    <strong>Paid Amount:</strong> ₹${investment.paidAmount.toLocaleString()}<br>
                    <strong>Installments:</strong> ${investment.installmentsPaid}/${investment.tenure}<br>
                    <strong>Interest Rate:</strong> ${investment.interestRate}%<br>
                    <strong>Maturity Amount:</strong> ₹${investment.maturityAmount.toLocaleString()}
                `;
            }

            html += `
                <div class="card investment-card ${cardClass} mb-3">
                    <div class="card-body">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <h5 class="card-title">
                                    <i class="${icon}"></i> 
                                    ${investment.type === 'FD' ? 'Fixed Deposit' : 'Recurring Deposit'}
                                    <span class="badge bg-${investment.status === 'Active' ? 'success' : 'secondary'} ms-2">
                                        ${investment.status}
                                    </span>
                                </h5>
                                <p class="card-text">
                                    <strong>ID:</strong> ${investment.id}<br>
                                    ${details}<br>
                                    <strong>Start Date:</strong> ${new Date(investment.startDate).toLocaleDateString()}<br>
                                    <strong>Maturity Date:</strong> ${new Date(investment.maturityDate).toLocaleDateString()}
                                </p>
                            </div>
                            <div class="col-md-4 text-end">
                                ${investment.type === 'RD' && investment.status === 'Active' ? 
                                    `<button class="btn btn-success btn-sm" onclick="payRDInstallment('${investment.id}')">
                                        <i class="fas fa-calendar-plus"></i> Pay Installment
                                    </button>` : 
                                    ''
                                }
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
    }

    document.getElementById('investments-list').innerHTML = html;
}

function payRDInstallment(rdId) {
    const userInvestments = investments[currentUser] || [];
    const rd = userInvestments.find(inv => inv.id === rdId);
    
    if (!rd || rd.type !== 'RD' || rd.status !== 'Active') {
        showAlert('Invalid RD or RD is not active', 'danger');
        return;
    }

    // Check if RD is already completed
    if (rd.installmentsPaid >= rd.tenure) {
        showAlert('RD is already completed', 'info');
        return;
    }

    // Find source account
    const userAccounts = getUserAccounts();
    const account = userAccounts.find(acc => acc.accountNumber === rd.sourceAccount);
    
    if (!account || account.balance < rd.monthlyAmount) {
        showAlert('Insufficient balance in source account', 'danger');
        return;
    }

    // Deduct installment
    account.balance -= rd.monthlyAmount;
    rd.paidAmount += rd.monthlyAmount;
    rd.installmentsPaid += 1;
    
    // Update next installment date
    rd.nextInstallment = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString();
    
    // Check if RD is completed
    if (rd.installmentsPaid >= rd.tenure) {
        rd.status = 'Matured';
        // Credit maturity amount to source account
        account.balance += rd.maturityAmount;
        recordTransaction(rd.sourceAccount, rd.maturityAmount, 'RD Matured', `RD matured - ID: ${rd.id}`);
        showAlert(`Congratulations! Your RD has matured. ₹${rd.maturityAmount.toLocaleString()} has been credited to your account.`, 'success');
    } else {
        showAlert(`Installment of ₹${rd.monthlyAmount.toLocaleString()} paid successfully!`, 'success');
    }
    
    // Record transaction
    recordTransaction(rd.sourceAccount, -rd.monthlyAmount, 'RD Installment', `RD installment - ID: ${rd.id} (${rd.installmentsPaid}/${rd.tenure})`);

    saveAccounts();
    saveInvestments();
    saveTransactions();
    
    loadInvestments();
    loadAccounts();
    loadDashboard();
}

function showTransactionHistory(accountNumber) {
    const accountTransactions = transactions[accountNumber] || [];
    
    let html = '';
    if (accountTransactions.length === 0) {
        html = `
            <div class="text-center py-4">
                <i class="fas fa-receipt fa-3x text-muted mb-3"></i>
                <h6>No transactions found</h6>
                <p class="text-muted">Start using your account to see transaction history</p>
            </div>
        `;
    } else {
        html = '<div class="list-group">';
        accountTransactions.forEach(transaction => {
            const isCredit = transaction.amount > 0;
            const amountClass = isCredit ? 'credit' : 'debit';
            const icon = isCredit ? 'fas fa-arrow-down text-success' : 'fas fa-arrow-up text-danger';
            
            html += `
                <div class="list-group-item transaction-item">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                                <i class="${icon} me-2"></i>
                                <strong>${transaction.type}</strong>
                            </div>
                            <p class="mb-1">${transaction.note}</p>
                            <small class="text-muted">${new Date(transaction.date).toLocaleString()}</small>
                        </div>
                        <div class="text-end">
                            <div class="transaction-amount ${amountClass} mb-1">
                                ${isCredit ? '+' : ''}₹${Math.abs(transaction.amount).toLocaleString()}
                            </div>
                            <small class="text-muted">Balance: ₹${transaction.balance.toLocaleString()}</small>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }

    document.getElementById('transaction-history-content').innerHTML = `
        <h6>Transaction History - Account: ${accountNumber}</h6>
        ${html}
    `;

    const modal = new bootstrap.Modal(document.getElementById('transactionModal'));
    modal.show();
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});