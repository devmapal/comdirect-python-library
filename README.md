# Comdirect Python API Client

[![PyPI version](https://img.shields.io/pypi/v/comdirect-client.svg)](https://pypi.org/project/comdirect-client/)
[![Tests](https://github.com/mcdax/comdirect-python-library/actions/workflows/tests.yml/badge.svg)](https://github.com/mcdax/comdirect-python-library/actions/workflows/tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, asynchronous Python client library for the Comdirect Banking API. Built with type safety, automatic token refresh, and comprehensive error handling.

> **Note**: This code is AI-generated but has been thoroughly manually tested and reviewed.

## Features

- ✅ **Full OAuth2 + TAN Authentication Flow** - Handles all 5 authentication steps automatically
- ✅ **Automatic Token Refresh** - Background task refreshes tokens 120s before expiration
- ✅ **Optional Token Persistence** - Save/restore tokens to disk to avoid reauthentication after app restart
- ✅ **Type-Safe Models** - Strongly typed dataclasses for all API responses
- ✅ **Async/Await** - Built on `httpx` and `asyncio` for high performance
- ✅ **Comprehensive Logging** - Detailed logging with sensitive data sanitization
- ✅ **Reauth Callbacks** - Custom callbacks when reauthentication is needed
- ✅ **Error Handling** - Specific exceptions for different failure scenarios
- ✅ **Context Manager Support** - Automatic resource cleanup

## API Documentation References

This client implements the official Comdirect REST API:

- [Comdirect REST API Documentation (PDF)](https://kunde.comdirect.de/cms/media/comdirect_REST_API_Dokumentation.pdf)
- [Comdirect REST API Swagger Specification (JSON)](https://kunde.comdirect.de/cms/media/comdirect_rest_api_swagger.json)

---

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Account Balances](#account-balances)
  - [Transactions](#transactions)
- [Token Management](#token-management)
  - [Automatic Token Refresh](#automatic-token-refresh)
  - [Token Persistence](#token-persistence)
  - [On-Demand Token Refresh](#on-demand-token-refresh)
  - [Reauth Callback](#reauth-callback)
  - [Token Lifecycle](#token-lifecycle)
- [Persistent Client Usage](#persistent-client-usage)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Security Notes](#security-notes)

---

## Project Structure

```
comdirect-lib/
├── comdirect_client/           # Main package
│   ├── __init__.py             # Package exports
│   ├── client.py               # ComdirectClient implementation
│   ├── models.py               # Data models (AccountBalance, Transaction)
│   ├── exceptions.py           # Custom exceptions
│   └── token_storage.py        # Token persistence
│
├── examples/
│   └── basic_usage.py          # Complete usage example with real authentication
│
├── tests/
│   ├── conftest.py             # Pytest fixtures and mocking setup
│   ├── test_comdirect_bdd.py   # BDD step definitions (pytest-bdd)
│   └── test_token_storage.py   # Token persistence tests (19 test cases)
│
├── comdirect_api.feature       # Gherkin BDD specification (39 scenarios, 457 lines)
├── COMDIRECT_API.md            # Detailed API documentation (815 lines)
├── pyproject.toml              # Poetry dependencies and configuration
├── test.sh                     # Quick integration test script
├── .env.example                # Environment variable template
└── README.md                   # This file
```

### Key Components

- **`client.py`**: Core API client with OAuth2 flow, token refresh, and API methods
- **`models.py`**: Type-safe dataclasses (`AccountBalance`, `Transaction`, `AmountValue`)
- **`exceptions.py`**: Specific exception types for different failure scenarios
- **`token_storage.py`**: Token persistence for avoiding reauthentication after restart
- **`comdirect_api.feature`**: Comprehensive BDD specification (living documentation)
- **`COMDIRECT_API.md`**: Deep dive into Comdirect API endpoints and flows

---

## Installation

### Prerequisites

- **Python 3.9+** (tested with Python 3.9-3.12)

### Using pip (Recommended)

Install directly from PyPI:

```bash
pip install comdirect-client
```

### For Development

If you want to contribute or modify the library:

#### Using Poetry

```bash
# Clone the repository
git clone https://github.com/mcdax/comdirect-python-library.git
cd comdirect-lib

# Install production dependencies
poetry install

# Install with development dependencies (tests, linting, etc.)
poetry install --with dev

# Activate virtual environment
poetry shell
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/mcdax/comdirect-python-library.git
cd comdirect-lib

# Install in editable mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Dependencies

**Production:**

- `httpx ^0.27.0` - Async HTTP client
- `pydantic ^2.0.0` - Data validation

**Development:**

- `pytest ^8.0.0` - Testing framework
- `pytest-asyncio ^0.23.0` - Async test support
- `pytest-bdd ^7.0.0` - BDD testing with Gherkin
- `pytest-mock ^3.12.0` - Mocking utilities
- `black ^24.0.0` - Code formatter
- `mypy ^1.8.0` - Type checker
- `ruff ^0.2.0` - Fast Python linter

---

## Running Tests

### Quick Integration Test (Real API)

The fastest way to test with the real Comdirect API:

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your Comdirect credentials
nano .env  # or vim, code, etc.
# Required variables:
#   COMDIRECT_CLIENT_ID=your_client_id
#   COMDIRECT_CLIENT_SECRET=your_client_secret
#   COMDIRECT_USERNAME=your_username
#   COMDIRECT_PASSWORD=your_password

# 3. Run integration test
chmod +x test.sh
./test.sh
```

**What happens:**

1. Authenticates with Comdirect API
2. **Waits for Push-TAN approval** on your smartphone (5-60 seconds)
3. Fetches account balances
4. Fetches transactions for first account
5. Tests automatic token refresh

**Expected output:**

```
INFO: Starting authentication flow
INFO: OAuth2 token obtained: 1a2b3c4d...
INFO: Waiting for TAN approval (P_TAN_PUSH)
INFO: TAN approved via P_TAN_PUSH
INFO: Authentication successful
INFO: Token refresh task started

Found 2 accounts:
  Account 1: Girokonto - Balance: 1234.56 EUR
  Account 2: Tagesgeld - Balance: 5678.90 EUR

Retrieved 15 transactions
  2024-11-09: -12.50 EUR (Direct Debit)
  ...
```

### BDD Tests (Mocked)

Run comprehensive BDD tests with mocked API responses:

```bash
# Install dev dependencies
poetry install --with dev

# Run all BDD tests
poetry run pytest tests/test_comdirect_bdd.py -v

# Run specific scenario
poetry run pytest tests/test_comdirect_bdd.py -k "token refresh" -v

# Run with coverage report
poetry run pytest --cov=comdirect_client --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

**BDD Coverage (39 scenarios):**

- ✅ Complete 5-step OAuth2 + TAN authentication flow
- ✅ Automatic token refresh (background task)
- ✅ On-demand token refresh (after 401 responses)
- ✅ Account balance retrieval
- ✅ Transaction retrieval with filters
- ✅ Pagination support
- ✅ Error handling and logging
- ✅ Reauth callback mechanism

### Unit Tests

```bash
# Run all tests
poetry run pytest tests/ -v

# Run with markers
poetry run pytest tests/ -m "not slow" -v

# Verbose output
poetry run pytest tests/ -vv -s
```

### Code Quality Tools

```bash
# Type checking
poetry run mypy comdirect_client

# Linting
poetry run ruff check .

# Auto-fix linting issues
poetry run ruff check --fix .

# Code formatting
poetry run black .

# Check formatting without changes
poetry run black --check .
```

---

## Quick Start

### 1. Install the Package

```bash
pip install comdirect-client
```

### 2. Basic Usage Example

```python
import asyncio
import os
from comdirect_client.client import ComdirectClient


async def main():
    # Initialize client
    async with ComdirectClient(
        client_id=os.getenv("COMDIRECT_CLIENT_ID"),
        client_secret=os.getenv("COMDIRECT_CLIENT_SECRET"),
        username=os.getenv("COMDIRECT_USERNAME"),
        password=os.getenv("COMDIRECT_PASSWORD"),
    ) as client:
        
        # Authenticate (triggers Push-TAN on your smartphone)
        print("Authenticating...")
        await client.authenticate()
        print("✓ Authenticated!")
        
        # Fetch account balances
        balances = await client.get_account_balances()
        print(f"\nFound {len(balances)} accounts:")
        for balance in balances:
            print(f"  {balance.account_display_id}: {balance.balance.value} {balance.balance.unit}")
         
         # Fetch all transactions for first account (up to 500 most recent)
         if balances:
             transactions = await client.get_transactions(
                 account_id=balances[0].accountId
             )
             print(f"\nFound {len(transactions)} transactions:")
             for tx in transactions[:5]:  # Show first 5
                 # Use booking date if available, otherwise fall back to valuta date
                 display_date = tx.bookingDate if tx.bookingDate else tx.valutaDate
                 print(f"  {display_date}: {tx.amount.value} {tx.amount.unit}")



if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Set Up Your Credentials

```bash
# Set environment variables
export COMDIRECT_CLIENT_ID="your_client_id"
export COMDIRECT_CLIENT_SECRET="your_client_secret"
export COMDIRECT_USERNAME="your_username"
export COMDIRECT_PASSWORD="your_password"

# Run your script
python your_script.py
```

### 4. Run the Included Example (Development Only)

If you've cloned the repository:

```bash
# Export credentials
export $(cat .env | xargs)

# Run example (requires Push-TAN approval on smartphone)
poetry run python examples/basic_usage.py

# Or use the test script
./test.sh
```

**Expected Flow:**

1. Script starts → Sends authentication request
2. **Your smartphone receives Push-TAN notification** (approve within 60s)
3. After approval → Fetches account data
4. Displays balances and recent transactions

---

## API Reference

### Client Initialization

```python
from comdirect_client.client import ComdirectClient

client = ComdirectClient(
    client_id: str,                     # OAuth2 client ID (required)
    client_secret: str,                 # OAuth2 client secret (required)
    username: str,                      # Comdirect username (required)
    password: str,                      # Comdirect password (required)
    base_url: str = "https://api.comdirect.de",  # API base URL
    token_storage_path: Optional[str] = None,    # File path for token persistence
    reauth_callback: Optional[Callable[[str], None]] = None,  # Called when reauth needed
    token_refresh_threshold_seconds: int = 120,  # Refresh 120s before expiry
    timeout_seconds: float = 30.0,     # HTTP request timeout
)
```

### Authentication

#### `authenticate()`

Performs the complete OAuth2 + TAN authentication flow (5 steps):

1. Password credentials grant → Initial token
2. Session status retrieval → Session UUID
3. TAN challenge creation → Triggers Push-TAN
4. TAN approval polling → Waits up to 60 seconds
5. Session activation + token exchange → Banking token

```python
await client.authenticate()
# Waits for Push-TAN approval on smartphone
# Raises TANTimeoutError if no approval within 60 seconds
# Raises AuthenticationError if credentials invalid
```

**What happens:**

- Sends authentication request to Comdirect API
- Creates TAN challenge (Push-TAN/Photo-TAN/SMS-TAN)
- **User must approve TAN on smartphone within 60 seconds**
- Polls for approval every 1 second
- Activates session and obtains banking token
- Starts automatic token refresh background task

#### `is_authenticated()`

Check if client has valid authentication token:

```python
if client.is_authenticated():
    print("Authenticated!")
else:
    print("Not authenticated - call authenticate() first")
```

#### `get_token_expiry()`

Get token expiration datetime:

```python
from datetime import datetime

expiry: Optional[datetime] = client.get_token_expiry()
if expiry:
    seconds_remaining = (expiry - datetime.now()).total_seconds()
    print(f"Token expires in {seconds_remaining:.0f} seconds")
```

#### `refresh_token()`

Manually refresh access token (usually done automatically):

```python
success: bool = await client.refresh_token()
if success:
    print("Token refreshed successfully")
else:
    print("Token refresh failed - reauthentication needed")
```

**Note:** The client automatically refreshes tokens in the background 120 seconds before expiration. Manual refresh is rarely needed.

---

### Account Balances

#### `get_account_balances()`

Retrieve balances for all accounts:

```python
from comdirect_client.models import AccountBalance

balances: list[AccountBalance] = await client.get_account_balances()

for balance in balances:
    print(f"Account ID: {balance.accountId}")                    # UUID
    print(f"Display ID: {balance.account_display_id}")          # Formatted account number
    print(f"Type: {balance.account_type}")                      # GIRO, DEPOT, FESTGELD, etc.
    print(f"Balance: {balance.balance.value} {balance.balance.unit}")  # Current balance
    print(f"Available: {balance.available_cash_amount.value}")  # Available cash
    print(f"Date: {balance.balanceDate}")                       # ISO date
    print()
```

**Method Signature:**

```python
async def get_account_balances(
    with_attributes: bool = True,
    without_attributes: Optional[str] = None
) -> list[AccountBalance]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `with_attributes` | `bool` | `True` | Include account master data in response |
| `without_attributes` | `Optional[str]` | `None` | Comma-separated list of attributes to exclude (e.g., `"account"`) |

**Query Parameter Examples:**

```python
# Include all attributes (default)
balances = await client.get_account_balances()

# Exclude account master data
balances = await client.get_account_balances(with_attributes=False)

# Custom exclusion
balances = await client.get_account_balances(
    without_attributes="balance,currency"
)
```

**Response Fields:**

- `accountId` (str) - Account UUID (use for `get_transactions()`)
- `account_display_id` (str) - Formatted account number (e.g., "DE12345...")
- `account_type` (str) - Account type: `GIRO`, `DEPOT`, `FESTGELD`, `CALL_MONEY`, etc.
- `balance` (AmountValue) - Current balance with currency
- `available_cash_amount` (AmountValue) - Available funds
- `balanceDate` (str) - Balance date (ISO format)

**Errors:**

- `TokenExpiredError` - Authentication expired
- `NetworkTimeoutError` - Request timed out

---

### Transactions

#### `get_transactions()`

Retrieve **all available** transactions for a specific account (up to 500 per call):

```python
from comdirect_client.models import Transaction

transactions: list[Transaction] = await client.get_transactions(
    account_id="account-uuid-here",                   # Required: Account UUID
    transaction_state="BOOKED",                       # Optional: Filter by state
    transaction_direction="CREDIT_AND_DEBIT",         # Optional: Filter by direction
)

for tx in transactions:
    # Use booking date if available, otherwise fall back to valuta date
    display_date = tx.bookingDate if tx.bookingDate else tx.valutaDate
    print(f"Date: {display_date}")                 # Booking date or valuta date
    print(f"Amount: {tx.amount.value} {tx.amount.unit}")  # Transaction amount
    if tx.transactionType:
        print(f"Type: {tx.transactionType.text}")  # Transaction type description
    # Remittance information is parsed into structured lines
    print("Remittance lines:")
    for line in tx.remittance_lines:
        print(f"  - {line}")
    print()
```

**Method Signature:**

```python
async def get_transactions(
    account_id: str,
    transaction_state: Optional[str] = None,
    transaction_direction: Optional[str] = None,
    paging_count: Optional[int] = None,
    min_booking_date: Optional[date] = None,
    max_booking_date: Optional[date] = None,
    with_attributes: bool = True,
    without_attributes: Optional[str] = None
) -> list[Transaction]
```

**Parameters:**

| Parameter | Type | Values | Default | Description |
|-----------|------|--------|---------|-------------|
| `account_id` | `str` | UUID | **Required** | Account UUID from `AccountBalance.accountId` |
| `transaction_state` | `Optional[str]` | `"BOOKED"`, `"NOTBOOKED"`, `"BOTH"` | `None` | Filter by booking state |
| `transaction_direction` | `Optional[str]` | `"CREDIT"`, `"DEBIT"`, `"CREDIT_AND_DEBIT"` | `None` | Filter by direction |
| `paging_count` | `Optional[int]` | 1-500 | `500` | Number of results per page (max: 500) |
| `min_booking_date` | `Optional[date]` | `date` object | `None` | Start date for filtering (YYYY-MM-DD) |
| `max_booking_date` | `Optional[date]` | `date` object | `None` | End date for filtering (YYYY-MM-DD) |
| `with_attributes` | `bool` | - | `True` | Include account details in response |
| `without_attributes` | `Optional[str]` | attribute names | `None` | Comma-separated attributes to exclude |

**Transaction States:**

- `BOOKED` - Only confirmed/booked transactions
- `NOTBOOKED` - Only pending/unbooked transactions
- `BOTH` - All transactions (booked + pending)

**Transaction Directions:**

- `CREDIT` - Only incoming transactions (deposits)
- `DEBIT` - Only outgoing transactions (withdrawals)
- `CREDIT_AND_DEBIT` - Both incoming and outgoing

**📅 Date Filtering:**

The library supports server-side date filtering using `min_booking_date` and `max_booking_date` parameters:

```python
from datetime import date

# Fetch transactions for a specific date range
transactions = await client.get_transactions(
    account_id="...",
    min_booking_date=date(2024, 1, 1),
    max_booking_date=date(2024, 12, 31)
)
print(f"Retrieved {len(transactions)} transactions for 2024")
```

**📄 Pagination:**

The library supports pagination via the `paging_count` parameter:

- **Default page size**: `paging_count` defaults to **500** (API maximum)
- **Library behavior**: By default, `get_transactions()` fetches up to 500 transactions in one call

```python
# Fetch up to 500 most recent transactions (default)
transactions = await client.get_transactions(account_id="...")
print(f"Retrieved {len(transactions)} transactions (up to 500)")

# Fetch with custom page size
transactions = await client.get_transactions(
    account_id="...",
    paging_count=100
)
```

**Response Fields:**

- `bookingDate` (Optional[date]) - Booking date - **May be None for pending transactions**
- `valutaDate` (str) - Value date (ISO format string) - Use as fallback if `bookingDate` is not available
- `amount` (Optional[AmountValue]) - Transaction amount (positive for credit, negative for debit)
- `transactionType` (Optional[EnumText]) - Transaction type with `key` and `text` fields
- `remittance_lines` (property) - List of parsed remittance lines (property that returns `remittanceLines`)
- `remittanceLines` (list[str]) - Parsed remittance lines extracted from the raw `remittanceInfo` field
- `creditor` (Optional[AccountInformation]) - Creditor account information
- `debtor` (Optional[AccountInformation]) - Debtor account information
- `directDebitCreditorId` (Optional[str]) - Direct debit creditor identifier
- `directDebitMandateId` (Optional[str]) - Direct debit mandate reference

**💡 Tip: Handle Missing Booking Dates**

For pending transactions, `bookingDate` may be `None`. Always use `valutaDate` as a fallback:

```python
# Recommended pattern
for tx in transactions:
    # Use booking date if available, otherwise fall back to valuta date
    display_date = tx.bookingDate if tx.bookingDate else tx.valutaDate
    print(f"Date: {display_date}")
```

**⚠️ Important: Date Filtering NOT Supported**

The Comdirect API does **not support** `from_date`/`to_date` parameters for banking transactions. To filter by date, retrieve all transactions and filter client-side:

```python
from datetime import datetime, timedelta

# Fetch all transactions
all_transactions = await client.get_transactions(account_id="...")

# Filter client-side for last 30 days (using booking_date or valuta_date as fallback)
cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
recent = [tx for tx in all_transactions if (tx.booking_date or tx.valuta_date or "") >= cutoff_date]

print(f"Found {len(recent)} transactions in last 30 days")
```

---

### Advanced: Pagination and API Limits

The Comdirect API uses server-side pagination with a hard limit of 500 transactions per request.

**Key points:**

- Default page size is 500 transactions (API maximum).
- The library's `get_transactions()` method defaults to `paging-count=500` to maximize results in a single call.
- You cannot retrieve more than 500 transactions for an account in one request.
- Use date filtering (`min_booking_date`/`max_booking_date`) to retrieve transactions across different time periods.

To access more than 500 transactions, use date-based filtering to split your queries across multiple date ranges (see examples below).

#### Fetching More Than 500 Transactions

⚠️ **Important:** The comdirect API has a hard limit of 500 transactions per request. To retrieve more than 500 transactions, use date-based filtering to split your queries across multiple date ranges.

**Strategy 1: Use Native Date Filtering**

The library now supports native date filtering via `min_booking_date` and `max_booking_date` parameters. Use this to fetch transactions across multiple date ranges:

```python
from datetime import date, timedelta
from typing import List

async def fetch_all_transactions_by_date(
    client, 
    account_uuid: str,
    start_date: date,
    end_date: date,
    chunk_days: int = 30
) -> List[Transaction]:
    """
    Fetch transactions across multiple date ranges to bypass the 500 limit.
    
    Strategy: Break large date ranges into smaller chunks (e.g., 30-day periods)
    and use native date filtering.
    """
    all_transactions = []
    current_date = start_date
    
    while current_date <= end_date:
        # Calculate date range (e.g., 30-day chunks)
        chunk_end = min(current_date + timedelta(days=chunk_days), end_date)
        
        print(f"Fetching transactions from {current_date} to {chunk_end}")
        
        # Fetch transactions for this date range using native date filtering
        transactions = await client.get_transactions(
            account_id=account_uuid,
            min_booking_date=current_date,
            max_booking_date=chunk_end,
            paging_count=500  # Maximum per request
        )
        
        all_transactions.extend(transactions)
        print(f"  Found {len(transactions)} transactions in this period")
        
        # Move to next chunk
        current_date = chunk_end + timedelta(days=1)
    
    # Remove duplicates (in case of overlapping date ranges)
    seen_refs = set()
    unique_transactions = []
    for tx in all_transactions:
        # Use bookingDate if available, otherwise valutaDate as fallback
        date_key = tx.bookingDate if tx.bookingDate else tx.valutaDate
        ref = (date_key, tx.amount.value if tx.amount else None, tx.reference)
        if ref not in seen_refs:
            seen_refs.add(ref)
            unique_transactions.append(tx)
    
    return unique_transactions

# Usage example:
transactions = await fetch_all_transactions_by_date(
    client,
    account_uuid="YOUR_ACCOUNT_UUID",
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31),
    chunk_days=30  # Fetch in 30-day chunks
)
print(f"Total transactions retrieved: {len(transactions)}")
```

**Strategy 2: Historical Data Export (Recommended for Large Datasets)**

If you need transaction history beyond what the API provides:

1. **Use Comdirect's Web Interface**: Log in to comdirect.de and export transactions as CSV/PDF for historical analysis
2. **Combine API + Historical Data**: 
   - Use the API for recent transactions (last 500)
   - Use exported CSV files for older historical data
3. **Regular Polling**: Set up a scheduled job to fetch and store transactions daily/weekly, building your own historical database

```python
import sqlite3
from datetime import datetime, timedelta

async def poll_and_store_transactions(client, account_uuid: str, db_path: str):
    """
    Fetch recent transactions and store them in a local database.
    Run this daily to build a complete transaction history.
    """
    # Fetch up to 500 most recent transactions
    transactions = await client.get_transactions(account_uuid)
    
    # Store in SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            booking_date TEXT,
            valuta_date TEXT,
            amount REAL,
            currency TEXT,
            reference TEXT,
            remittance_info TEXT,
            creditor_name TEXT,
            PRIMARY KEY (booking_date, valuta_date, amount, reference)
        )
    """)
    
    # Insert new transactions (ignore duplicates)
    for tx in transactions:
        cursor.execute("""
            INSERT OR IGNORE INTO transactions 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(tx.bookingDate) if tx.bookingDate else None,
            tx.valutaDate,
            float(tx.amount.value) if tx.amount else None,
            tx.amount.unit if tx.amount else None,
            tx.reference,
            " | ".join(tx.remittance_lines) if tx.remittance_lines else None,
            tx.creditor.holderName if tx.creditor else None
        ))
    
    conn.commit()
    conn.close()
    print(f"Stored {len(transactions)} transactions (duplicates ignored)")

# Run daily via cron job or scheduler
await poll_and_store_transactions(client, account_uuid, "transactions.db")
```

**Key Takeaways:**

- ✅ **For most use cases**: Use `get_transactions()` to fetch up to 500 transactions
- ✅ **For >500 transactions**: Use date-based filtering (`min_booking_date`/`max_booking_date`) with multiple API calls
- ✅ **For specific date ranges**: Use native date filtering parameters
- ✅ **For historical analysis**: Implement regular polling and store transactions locally
- ⚠️ **Note**: The API has a hard limit of 500 transactions per request, so use date filtering to retrieve larger datasets

---

## Token Management

### Automatic Token Refresh

The client automatically refreshes access tokens in the background:

**How it works:**

1. After successful authentication, starts background asyncio task
2. Calculates refresh time: `token_expiry - 120 seconds` (configurable)
3. Sleeps until refresh time
4. Automatically calls `POST /oauth/token` with `grant_type=refresh_token`
5. Updates `access_token` and `refresh_token` (both tokens rotate!)
6. Repeats indefinitely

**Configuration:**

```python
client = ComdirectClient(
    ...,
    token_refresh_threshold_seconds=120,  # Refresh 120s before expiry (default)
)
```

**Timeline Example:**

```
T+0:     authenticate() → token expires at T+599s
T+479s:  Background task wakes up (599 - 120 = 479)
T+479s:  POST /oauth/token → new token expires at T+1078s
T+958s:  Next automatic refresh (1078 - 120 = 958)
...
```

**Failure Handling:**

- If refresh fails → Invokes `reauth_callback` (if configured)
- Clears all tokens
- Stops background refresh task

### Token Persistence

The client supports optional file-based token persistence to avoid reauthentication after application restart. Tokens are stored securely with restricted file permissions (0o600 - owner read/write only).

**Security Note:** Token persistence stores authentication tokens to disk. Ensure the storage directory is on an encrypted filesystem and has appropriate access controls. In production, consider encrypting tokens at rest using your application's encryption layer.

**Enable Token Persistence:**

```python
import asyncio
from comdirect_client.client import ComdirectClient

async def main():
    # Enable token persistence by providing a storage path
    async with ComdirectClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        token_storage_path="/secure/path/comdirect_tokens.json",
    ) as client:
        
        # First run: Authenticate and tokens are automatically saved
        try:
            await client.authenticate()
            print("✓ Authenticated and tokens saved to disk")
        except FileNotFoundError:
            print("✗ Token storage directory doesn't exist")
        
        # Subsequent runs: Tokens are automatically loaded from disk
        # If tokens are valid, authenticate() returns immediately without 2FA
        # If tokens are expired, they're silently discarded and new auth is needed

if __name__ == "__main__":
    asyncio.run(main())
```

**How Token Persistence Works:**

1. **Initialization**: Client loads saved tokens on startup (if they exist and aren't expired)
2. **Auto-Save**: After authentication or token refresh, tokens are automatically saved to disk
3. **Expiry Validation**: Expired tokens are rejected during load and reauthentication is triggered
4. **File Security**: Token file has restricted permissions (0o600 - owner only)
5. **On Logout**: Token file is automatically deleted via `client.close()` or context manager

**Persistent Storage Format:**

Tokens are stored as JSON with ISO format datetime:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_token_value_here",
  "token_expiry": "2025-12-10T15:30:45.123456"
}
```

**Recovery Scenarios:**

```python
# Scenario 1: Tokens exist and are valid
async with ComdirectClient(..., token_storage_path="...") as client:
    await client.authenticate()  # Returns immediately, no 2FA needed!
    balances = await client.get_account_balances()

# Scenario 2: Tokens expired, need reauthentication
async with ComdirectClient(..., token_storage_path="...") as client:
    await client.authenticate()  # Triggers new 2FA flow
    # Old expired tokens are automatically cleared

# Scenario 3: First run, no tokens saved yet
async with ComdirectClient(..., token_storage_path="...") as client:
    await client.authenticate()  # Normal 2FA flow
    # Tokens saved to disk for next run

# Scenario 4: Storage directory doesn't exist
async with ComdirectClient(..., token_storage_path="/nonexistent/path") as client:
    await client.authenticate()  # Works normally, but won't persist
    # TokenStorageError logged as warning
```

**Error Handling:**

```python
from comdirect_client.exceptions import TokenStorageError

try:
    async with ComdirectClient(..., token_storage_path="...") as client:
        await client.authenticate()
except TokenStorageError as e:
    print(f"Token storage failed: {e}")
    # Token persistence unavailable, but client works normally
except FileNotFoundError:
    print("Token storage directory doesn't exist - create it first")
    import os
    os.makedirs(os.path.dirname(token_storage_path), exist_ok=True)
```

**Disabling Token Persistence:**

```python
# Simply omit the token_storage_path parameter (or set to None)
async with ComdirectClient(
    client_id="...",
    client_secret="...",
    username="...",
    password="...",
    # No token_storage_path - tokens not persisted
) as client:
    await client.authenticate()
```

### On-Demand Token Refresh

If an API call receives `401 Unauthorized`, the client automatically:

1. Attempts token refresh
2. Retries the original request with new token
3. If refresh fails → Invokes `reauth_callback` and raises `TokenExpiredError`

This provides a **dual refresh strategy**:

- **Proactive**: Background task (before expiration)
- **Reactive**: On 401 errors (after expiration)

### Reauth Callback

Configure a callback to handle reauthentication needs:

```python
def reauth_handler(reason: str):
    """Called when reauthentication is needed."""
    print(f"Reauthentication required: {reason}")
    # Send notification, trigger new auth flow, restart service, etc.
    
    # Reasons:
    # - "token_refresh_failed" - Background refresh failed
    # - "automatic_refresh_failed" - Background task error
    # - "api_request_unauthorized" - API returned 401 after refresh attempt

client = ComdirectClient(
    ...,
    reauth_callback=reauth_handler,
)
```

**Use cases:**

- Send email/Slack notification to admin
- Trigger new authentication flow
- Log metrics/alerting
- Gracefully restart service

### Token Lifecycle

Tokens expire every ~10 minutes (599s). The client automatically refreshes 120 seconds before expiration, ensuring seamless API calls. When a token refresh occurs, both `access_token` and `refresh_token` rotate on the Comdirect API side.

---

## Persistent Client Usage

**The ComdirectClient should be kept alive (persistent) throughout your application's lifecycle for best functionality.**

### Why Keep the Client Alive?

The client has a **background token refresh task** that automatically refreshes tokens 120 seconds before they expire. This task runs as an asyncio background coroutine and is critical for maintaining uninterrupted access to the Comdirect API.

**If the client instance is destroyed:**

- The background refresh task is cancelled
- Tokens will expire after ~10 minutes (599 seconds)
- A new TAN approval will be required for your next session
- This defeats the purpose of automatic token refresh

### Best Practice: Create Once, Reuse Everywhere

```python
import asyncio
from comdirect_client.client import ComdirectClient

# Global client instance - created once at application startup
client: ComdirectClient | None = None

async def init_client():
    """Initialize the client once at startup."""
    global client
    client = ComdirectClient(
        client_id="your_client_id",
        client_secret="your_client_secret",
        username="your_username",
        password="your_password",
        token_storage_path="/path/to/tokens.json",  # Persist across restarts
    )
    
    # Authenticate once - requires TAN approval
    await client.authenticate()
    print("Client authenticated and ready!")
    
    # The background refresh task is now running automatically
    # Tokens will be refreshed 120s before expiry

async def get_balances():
    """Use the persistent client for API calls."""
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.get_account_balances()

async def get_transactions(account_id: str):
    """Another API call using the same client instance."""
    if not client:
        raise RuntimeError("Client not initialized")
    return await client.get_transactions(account_id)

async def shutdown():
    """Clean up when application shuts down."""
    if client:
        await client.close()
```

### What Happens with Token Storage?

When you configure `token_storage_path`:

1. **First run**: Authenticate with TAN, tokens are saved to disk
2. **Subsequent runs**: Tokens are loaded from disk on client creation
3. **Background refresh starts automatically** when valid tokens are loaded
4. **No new TAN approval needed** as long as tokens haven't expired

```python
# Application startup
client = ComdirectClient(
    ...,
    token_storage_path="/path/to/tokens.json",
)

# If valid tokens exist in storage:
# - Tokens are automatically loaded
# - Refresh task starts immediately
# - No authenticate() call needed!

if client.is_authenticated():
    print("Tokens restored from storage - ready to use!")
    balances = await client.get_account_balances()
else:
    print("No valid tokens - TAN approval required")
    await client.authenticate()
```

### Anti-Pattern: Creating New Client Per Request

**Do NOT do this** - it defeats the purpose of automatic token refresh:

```python
# BAD: Client is destroyed after each request
async def get_balance_bad():
    async with ComdirectClient(...) as client:
        await client.authenticate()  # TAN approval needed
        return await client.get_account_balances()
    # Client destroyed here! Refresh task cancelled!

# After ~10 minutes, calling get_balance_bad() again requires new TAN approval
```

### Framework Integration Examples

**FastAPI / Starlette:**

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from comdirect_client.client import ComdirectClient

client: ComdirectClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = ComdirectClient(
        ...,
        token_storage_path="/app/data/tokens.json",
    )
    if not client.is_authenticated():
        await client.authenticate()
    yield
    await client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/balances")
async def get_balances():
    return await client.get_account_balances()
```

**Long-running Service:**

```python
async def main():
    client = ComdirectClient(
        ...,
        token_storage_path="tokens.json",
        reauth_callback=lambda reason: print(f"Reauth needed: {reason}"),
    )
    
    if not client.is_authenticated():
        await client.authenticate()
    
    # Run indefinitely - tokens refresh automatically
    while True:
        balances = await client.get_account_balances()
        print(f"Current balance: {balances[0].balance.value}")
        await asyncio.sleep(3600)  # Check every hour

asyncio.run(main())
```

---

## Data Models

All API responses are parsed into type-safe dataclasses defined in `comdirect_client.models`:

### AccountBalance

```python
from dataclasses import dataclass
from comdirect_client.models import AccountBalance, AmountValue

@dataclass
class AccountBalance:
    accountId: str                      # Account UUID (use for get_transactions)
    account_display_id: str             # Formatted account number
    account_type: str                   # Account type (GIRO, DEPOT, etc.)
    balance: AmountValue                # Current balance
    available_cash_amount: AmountValue  # Available cash
    balanceDate: str                    # Balance date (ISO format)
```

**Example:**

```python
balance = balances[0]
print(balance.accountId)           # "B5A9F0C8-B421-..."
print(balance.account_display_id)  # "DE12 3456 7890 1234 5678 90"
print(balance.account_type)        # "GIRO"
print(balance.balance.value)       # 1234.56
print(balance.balance.unit)        # "EUR"
```

### Transaction

```python
@dataclass
class Transaction:
    bookingDate: Optional[date]         # Booking date, may be None for pending transactions
    valutaDate: str                     # Value date (ISO format string)
    amount: Optional[AmountValue]       # Transaction amount
    transactionType: Optional[EnumText] # Transaction type with key and text
    remittanceLines: list[str]          # Parsed remittance lines
    creditor: Optional[AccountInformation]  # Creditor account information
    debtor: Optional[AccountInformation]    # Debtor account information
    directDebitCreditorId: Optional[str]     # Direct debit creditor identifier
    directDebitMandateId: Optional[str]      # Direct debit mandate reference
    # ... and more fields

    @property
    def remittance_lines(self) -> list[str]:
        """Convenience property that returns remittanceLines."""
        return self.remittanceLines
```

**Example:**

```python
tx = transactions[0]
print(tx.bookingDate)     # date(2024, 11, 9) or None
print(tx.valutaDate)      # "2024-11-09"
print(tx.amount.value)     # -12.50 (negative = debit)
print(tx.amount.unit)      # "EUR"
if tx.transactionType:
    print(tx.transactionType.text)  # "DIRECT_DEBIT"
print(tx.remittance_lines) # ["SPC*Mandragora Bochum", "Order 123-4567890-1234567"]
```

### AmountValue

```python
@dataclass
class AmountValue:
    value: float    # Numeric value
    unit: str       # Currency code (EUR, USD, etc.)
```

**Example:**

```python
amount = balance.balance
print(f"{amount.value} {amount.unit}")  # "1234.56 EUR"
```

---

## Error Handling

The library provides specific exceptions for different error scenarios, all defined in `comdirect_client.exceptions`:

### Exception Types

```python
from comdirect_client.exceptions import (
    AuthenticationError,      # Invalid credentials or auth failure
    ValidationError,          # Invalid request parameters (422)
    ServerError,              # Server error on API side (500)
    TANTimeoutError,          # TAN approval timeout (60 seconds)
    TokenExpiredError,        # Token expired and refresh failed
    SessionActivationError,   # Session activation failed
    AccountNotFoundError,     # Account UUID doesn't exist
    NetworkTimeoutError,      # Network request timeout
)
```

**Exception Hierarchy:**

```
ComdirectAPIError (base)
├── AuthenticationError       
├── ValidationError          
├── ServerError             
├── AccountNotFoundError   
├── TANTimeoutError
├── SessionActivationError
├── TokenExpiredError
└── NetworkTimeoutError
```

---

## Logging

The library uses Python's standard `logging` module with comprehensive logging throughout the codebase.

### Configure Logging

```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Get logger for specific module
logger = logging.getLogger("comdirect_client.client")
logger.setLevel(logging.DEBUG)  # Set DEBUG for detailed logs
```

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| **DEBUG** | Detailed technical info | `Request ID: 123456789` |
| **INFO** | High-level flow events | `Authentication successful` |
| **WARNING** | Recoverable issues | `Token refresh failed - token expired` |
| **ERROR** | Critical failures | `Authentication failed: Invalid credentials` |

---

## License

MIT License - see LICENSE file for details

## Disclaimer

This is an unofficial client library. Use at your own risk. The authors are not affiliated with Comdirect Bank AG.
