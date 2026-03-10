# Odoo MCP Server - JSON-RPC Integration Documentation

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Status:** Ready for Configuration

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Guide](#setup-guide)
4. [Features](#features)
5. [Usage](#usage)
6. [Agent Skills](#agent-skills)
7. [API Reference](#api-reference)
8. [Integration Examples](#integration-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The Odoo MCP Server provides programmatic access to Odoo ERP via JSON-RPC/XML-RPC, enabling the Personal AI Employee to interact with Odoo for business operations like customer management, invoicing, expense tracking, and more.

### Key Features

- **Customer Management** - Create and retrieve customers
- **Invoice Operations** - Create, read, and post invoices
- **Product Management** - Access product catalog
- **Expense Tracking** - Create and manage expenses
- **Agent Skills** - 5 Odoo-related skills for automation
- **Audit Logging** - All Odoo operations logged
- **JSON-RPC/XML-RPC** - Standard Odoo API protocol

---

## Prerequisites

### 1. Odoo Installation

You must have Odoo 19 Community installed and running.

**Quick Install:**
```bash
cd odoo_integration
./install_odoo_docker.sh
```

See [ODOO_INSTALLATION_DOCS.md](ODOO_INSTALLATION_DOCS.md) for detailed instructions.

### 2. Odoo Database

Create a database in Odoo:
1. Access http://localhost:8069
2. Create new database
3. Set master password
4. Create admin user

### 3. API Access

Odoo's XML-RPC/JSON-RPC API is enabled by default. No additional configuration needed.

---

## Setup Guide

### Step 1: Verify Odoo is Running

```bash
# Check if Odoo is accessible
curl http://localhost:8069

# Or open in browser
open http://localhost:8069
```

### Step 2: Get Odoo Credentials

You'll need:
- **URL**: Odoo server URL (e.g., http://localhost:8069)
- **Database**: Database name (e.g., "odoo")
- **Username**: Admin username (e.g., "admin")
- **Password**: Admin password

### Step 3: Configure Credentials

1. **Copy the template:**
   ```bash
   cd odoo_integration/credentials/
   cp odoo_credentials.json.template odoo_credentials.json
   ```

2. **Edit the credentials file:**
   ```bash
   nano odoo_credentials.json
   ```

3. **Add your credentials:**
   ```json
   {
     "url": "http://localhost:8069",
     "db": "odoo",
     "username": "admin",
     "password": "your_admin_password"
   }
   ```

4. **Secure the file:**
   ```bash
   chmod 600 odoo_credentials.json
   ```

### Step 4: Test Connection

```bash
cd odoo_integration
python3 odoo_mcp_server.py
```

Expected output:
```
============================================================
Odoo MCP Server - Test Client
============================================================

✅ Odoo credentials loaded successfully
✅ Authenticated with Odoo as user ID: 2

📋 Testing operations...

👥 Fetching customers...
Found 5 customers
  - John Smith (john@example.com)
  - Jane Doe (jane@example.com)

💰 Fetching invoices...
Found 3 invoices
  - INV/2026/0001: $1000.0 (posted)

📦 Fetching products...
Found 10 products
  - Consulting Service: $100.0

✅ Test completed successfully!
```

---

## Features

### 1. Customer Management

**Operations:**
- Get list of customers
- Create new customers
- Update customer information
- Search customers by criteria

**Use Cases:**
- Import customers from emails
- Auto-create customers from inquiries
- Sync customer data

### 2. Invoice Operations

**Operations:**
- Get list of invoices
- Create draft invoices
- Post (validate) invoices
- Filter by state (draft, posted, cancel)

**Use Cases:**
- Auto-generate invoices from emails
- Track invoice status
- Send invoice reminders

### 3. Product Management

**Operations:**
- Get product catalog
- Search products
- Get product pricing

**Use Cases:**
- Product lookup for invoicing
- Price quotes
- Inventory checks

### 4. Expense Tracking

**Operations:**
- Get list of expenses
- Create new expenses
- Submit expenses for approval

**Use Cases:**
- Auto-create expenses from receipts
- Track spending
- Expense reporting

---

## Usage

### Python API

```python
from odoo_integration.odoo_mcp_server import OdooClient

# Initialize client
client = OdooClient()

# Authenticate
if client.authenticate():
    print("Connected to Odoo!")

    # Get customers
    customers = client.get_customers(limit=10)
    for customer in customers:
        print(f"Customer: {customer['name']}")

    # Create customer
    partner_id = client.create_customer(
        name="New Customer",
        email="customer@example.com",
        phone="+1234567890"
    )

    # Get invoices
    invoices = client.get_invoices(limit=10, state='posted')
    for invoice in invoices:
        print(f"Invoice: {invoice['name']} - ${invoice['amount_total']}")

    # Create invoice
    invoice_id = client.create_invoice(
        partner_id=partner_id,
        lines=[
            {
                'product_id': 1,
                'quantity': 1,
                'price_unit': 100.0,
                'name': 'Consulting Service'
            }
        ]
    )

    # Post invoice
    client.post_invoice(invoice_id)

    # Get products
    products = client.get_products(limit=10)
    for product in products:
        print(f"Product: {product['name']} - ${product['list_price']}")
```

### Agent Skills

```bash
# Get customers
python3 skills_cli.py --skill GetOdooCustomersSkill --params '{"limit": 10}'

# Create customer
python3 skills_cli.py --skill CreateOdooCustomerSkill --params '{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890"
}'

# Get invoices
python3 skills_cli.py --skill GetOdooInvoicesSkill --params '{"limit": 10, "state": "posted"}'

# Create invoice
python3 skills_cli.py --skill CreateOdooInvoiceSkill --params '{
  "partner_id": 7,
  "lines": [
    {"product_id": 1, "quantity": 1, "price_unit": 100.0, "name": "Service"}
  ]
}'

# Get products
python3 skills_cli.py --skill GetOdooProductsSkill --params '{"limit": 10}'
```

---

## Agent Skills

### 1. GetOdooCustomersSkill

**Description:** Get list of customers from Odoo ERP

**Parameters:**
- `limit` (int, optional, default=10) - Maximum number of customers to fetch

**Returns:**
```json
{
  "count": 5,
  "customers": [
    {
      "id": 7,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1234567890",
      "street": "123 Main St",
      "city": "New York",
      "country_id": [233, "United States"]
    }
  ]
}
```

---

### 2. CreateOdooCustomerSkill

**Description:** Create a new customer in Odoo ERP

**Parameters:**
- `name` (str, required) - Customer name
- `email` (str, optional) - Customer email
- `phone` (str, optional) - Customer phone

**Returns:**
```json
{
  "partner_id": 15,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890"
}
```

---

### 3. GetOdooInvoicesSkill

**Description:** Get list of invoices from Odoo ERP

**Parameters:**
- `limit` (int, optional, default=10) - Maximum number of invoices to fetch
- `state` (str, optional) - Filter by state: draft, posted, cancel

**Returns:**
```json
{
  "count": 3,
  "invoices": [
    {
      "id": 5,
      "name": "INV/2026/0001",
      "partner_id": [7, "John Smith"],
      "invoice_date": "2026-03-10",
      "amount_total": 1000.0,
      "state": "posted"
    }
  ]
}
```

---

### 4. CreateOdooInvoiceSkill

**Description:** Create a new invoice in Odoo ERP

**Parameters:**
- `partner_id` (int, required) - Customer ID
- `lines` (list, required) - Invoice lines with product_id, quantity, price_unit

**Returns:**
```json
{
  "invoice_id": 10,
  "partner_id": 7,
  "line_count": 2
}
```

---

### 5. GetOdooProductsSkill

**Description:** Get list of products from Odoo ERP

**Parameters:**
- `limit` (int, optional, default=10) - Maximum number of products to fetch

**Returns:**
```json
{
  "count": 10,
  "products": [
    {
      "id": 1,
      "name": "Consulting Service",
      "list_price": 100.0,
      "standard_price": 50.0,
      "type": "service"
    }
  ]
}
```

---

## API Reference

### OdooClient Class

```python
class OdooClient:
    def __init__(self):
        """Initialize Odoo client"""

    def load_credentials(self) -> bool:
        """Load credentials from file"""

    def authenticate(self) -> bool:
        """Authenticate with Odoo"""

    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """Execute Odoo method"""

    # Customer Operations
    def get_customers(self, limit: int = 10) -> List[Dict]:
        """Get list of customers"""

    def create_customer(self, name: str, email: str = None, phone: str = None) -> Optional[int]:
        """Create a new customer"""

    # Invoice Operations
    def get_invoices(self, limit: int = 10, state: str = None) -> List[Dict]:
        """Get list of invoices"""

    def create_invoice(self, partner_id: int, lines: List[Dict]) -> Optional[int]:
        """Create a new invoice"""

    def post_invoice(self, invoice_id: int) -> bool:
        """Post (validate) an invoice"""

    # Product Operations
    def get_products(self, limit: int = 10) -> List[Dict]:
        """Get list of products"""

    # Expense Operations
    def get_expenses(self, limit: int = 10) -> List[Dict]:
        """Get list of expenses"""

    def create_expense(self, name: str, amount: float, employee_id: int) -> Optional[int]:
        """Create a new expense"""
```

---

## Integration Examples

### Example 1: Auto-Create Customer from Email

```python
from odoo_integration.odoo_mcp_server import OdooClient
from watcher.gmail_watcher_enhanced import get_email_details

# Get email
email = get_email_details(service, email_id)

# Extract customer info
name = email['from'].split('<')[0].strip()
email_addr = email['from'].split('<')[1].strip('>')

# Create in Odoo
client = OdooClient()
client.authenticate()
partner_id = client.create_customer(name=name, email=email_addr)

print(f"Created customer {name} with ID {partner_id}")
```

### Example 2: Generate Invoice from Email Request

```python
# Parse email for invoice details
subject = email['subject']  # "Invoice for Consulting - $500"
amount = 500.0

# Get or create customer
customers = client.get_customers(limit=100)
customer = next((c for c in customers if c['email'] == email_addr), None)

if not customer:
    partner_id = client.create_customer(name=name, email=email_addr)
else:
    partner_id = customer['id']

# Create invoice
invoice_id = client.create_invoice(
    partner_id=partner_id,
    lines=[{
        'product_id': 1,  # Consulting service
        'quantity': 1,
        'price_unit': amount,
        'name': 'Consulting Service'
    }]
)

# Post invoice
client.post_invoice(invoice_id)

print(f"Created and posted invoice {invoice_id}")
```

### Example 3: Expense Tracking from Receipt

```python
# Parse receipt email
expense_name = "Office Supplies"
expense_amount = 45.99

# Create expense
expense_id = client.create_expense(
    name=expense_name,
    amount=expense_amount,
    employee_id=1  # Your employee ID
)

print(f"Created expense {expense_id}")
```

---

## Best Practices

### 1. Secure Credentials

```bash
# Set proper permissions
chmod 600 odoo_integration/credentials/odoo_credentials.json

# Add to .gitignore
echo "odoo_integration/credentials/odoo_credentials.json" >> .gitignore

# Never commit credentials
git status  # Verify not tracked
```

### 2. Error Handling

```python
try:
    client = OdooClient()
    if not client.authenticate():
        print("Authentication failed")
        return

    customers = client.get_customers()
except Exception as e:
    print(f"Error: {e}")
    # Log error, notify admin, etc.
```

### 3. Batch Operations

```python
# Instead of creating customers one by one
for customer_data in customer_list:
    # Collect all data first
    pass

# Then create in batch
# (Odoo supports batch operations via execute_kw)
```

### 4. Use Transactions

For complex operations involving multiple steps, use Odoo's transaction support to ensure data consistency.

### 5. Monitor API Usage

- Log all API calls
- Track response times
- Monitor for errors
- Set up alerts for failures

---

## Troubleshooting

### Issue: Authentication Failed

**Error:** `❌ Authentication failed`

**Solutions:**
1. Verify Odoo is running: `curl http://localhost:8069`
2. Check credentials are correct
3. Verify database name matches
4. Ensure user has API access rights
5. Check Odoo logs: `docker logs odoo_app`

### Issue: Connection Refused

**Error:** `Connection refused`

**Solutions:**
1. Start Odoo: `cd ~/odoo-config && docker-compose start`
2. Check port is correct (default: 8069)
3. Verify firewall settings
4. Check Docker containers: `docker ps`

### Issue: Method Not Found

**Error:** `Method not found: xyz`

**Solutions:**
1. Verify model name is correct (e.g., 'res.partner', not 'partner')
2. Check method exists in Odoo version
3. Ensure required modules are installed
4. Check user has access rights to the model

### Issue: Access Denied

**Error:** `Access Denied`

**Solutions:**
1. Check user has appropriate access rights
2. Verify user is not archived/inactive
3. Check model-specific permissions
4. Use admin account for testing

### Issue: Slow Performance

**Symptoms:** API calls taking too long

**Solutions:**
1. Optimize search domains (use specific filters)
2. Limit fields returned (use fields parameter)
3. Use batch operations
4. Check Odoo server resources
5. Optimize PostgreSQL

---

## Summary

The Odoo MCP Server provides:

- ✅ **JSON-RPC/XML-RPC Integration** - Standard Odoo API
- ✅ **Customer Management** - Create and retrieve customers
- ✅ **Invoice Operations** - Full invoice lifecycle
- ✅ **Product Management** - Access product catalog
- ✅ **Expense Tracking** - Create and manage expenses
- ✅ **Agent Skills** - 5 Odoo-related skills
- ✅ **Audit Logging** - Complete activity tracking
- ✅ **Comprehensive Documentation** - Setup and usage guides

**Status:** Ready for Configuration
**Version:** 1.0.0
**Last Updated:** 2026-03-10

**Note:** Requires Odoo 19 Community installation and database setup.

---

## Quick Start Checklist

- [ ] Install Odoo 19: `./install_odoo_docker.sh`
- [ ] Create Odoo database
- [ ] Copy credentials template
- [ ] Add your credentials
- [ ] Test connection: `python3 odoo_mcp_server.py`
- [ ] Test Agent Skills
- [ ] Integrate with Personal AI Employee
- [ ] Set up automation workflows

**Ready to integrate! 💼**
