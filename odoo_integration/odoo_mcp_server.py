#!/usr/bin/env python3
"""
Odoo MCP Server
Model Context Protocol server for Odoo integration via JSON-RPC
"""

import sys
import json
import xmlrpc.client
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from audit_logger import AuditLogger, EventType

# Configuration
CREDENTIALS_PATH = Path(__file__).parent / "credentials" / "odoo_credentials.json"

# Setup audit logger
audit_logger = AuditLogger("odoo_mcp_server")


class OdooClient:
    """
    Odoo JSON-RPC Client

    Provides programmatic access to Odoo via XML-RPC/JSON-RPC
    """

    def __init__(self):
        self.url = None
        self.db = None
        self.username = None
        self.password = None
        self.uid = None
        self.common = None
        self.models = None
        self.authenticated = False

    def load_credentials(self) -> bool:
        """Load Odoo credentials from file"""
        try:
            if not CREDENTIALS_PATH.exists():
                print(f"❌ Credentials file not found: {CREDENTIALS_PATH}")
                print("Please create odoo_credentials.json with your Odoo credentials")
                return False

            with open(CREDENTIALS_PATH, 'r') as f:
                creds = json.load(f)

            # Validate required fields
            required_fields = ['url', 'db', 'username', 'password']
            missing_fields = [field for field in required_fields if field not in creds]

            if missing_fields:
                print(f"❌ Missing required credentials: {', '.join(missing_fields)}")
                return False

            self.url = creds['url']
            self.db = creds['db']
            self.username = creds['username']
            self.password = creds['password']

            print("✅ Odoo credentials loaded successfully")
            return True

        except Exception as e:
            print(f"❌ Error loading credentials: {e}")
            return False

    def authenticate(self) -> bool:
        """Authenticate with Odoo"""
        try:
            if not self.url:
                if not self.load_credentials():
                    return False

            # Connect to common endpoint
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')

            # Authenticate
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})

            if not self.uid:
                print("❌ Authentication failed")
                audit_logger.log_auth_event("odoo_xmlrpc", False)
                return False

            # Connect to object endpoint
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

            print(f"✅ Authenticated with Odoo as user ID: {self.uid}")
            self.authenticated = True
            audit_logger.log_auth_event("odoo_xmlrpc", True, {"uid": self.uid})
            return True

        except Exception as e:
            print(f"❌ Authentication error: {e}")
            audit_logger.log_auth_event("odoo_xmlrpc", False, {"error": str(e)})
            return False

    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """
        Execute Odoo method

        Args:
            model: Odoo model name (e.g., 'res.partner', 'account.move')
            method: Method name (e.g., 'search', 'read', 'create')
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method

        Returns:
            Method result
        """
        if not self.authenticated:
            raise Exception("Not authenticated with Odoo")

        return self.models.execute_kw(
            self.db, self.uid, self.password,
            model, method, args, kwargs
        )

    # Customer/Partner Operations

    def get_customers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of customers"""
        try:
            # Search for partners that are customers
            partner_ids = self.execute(
                'res.partner', 'search',
                [['customer_rank', '>', 0]],
                {'limit': limit}
            )

            # Read partner details
            partners = self.execute(
                'res.partner', 'read',
                partner_ids,
                ['name', 'email', 'phone', 'street', 'city', 'country_id']
            )

            audit_logger.log_event(
                "odoo_customers_fetched",
                f"Fetched {len(partners)} customers",
                details={"count": len(partners)}
            )

            return partners

        except Exception as e:
            print(f"❌ Error fetching customers: {e}")
            audit_logger.log_error("odoo_fetch_error", str(e), None)
            return []

    def create_customer(self, name: str, email: str = None, phone: str = None) -> Optional[int]:
        """Create a new customer"""
        try:
            partner_id = self.execute(
                'res.partner', 'create',
                {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'customer_rank': 1
                }
            )

            print(f"✅ Created customer: {name} (ID: {partner_id})")
            audit_logger.log_event(
                "odoo_customer_created",
                f"Created customer: {name}",
                details={"partner_id": partner_id, "name": name}
            )

            return partner_id

        except Exception as e:
            print(f"❌ Error creating customer: {e}")
            audit_logger.log_error("odoo_create_error", str(e), None)
            return None

    # Invoice Operations

    def get_invoices(self, limit: int = 10, state: str = None) -> List[Dict[str, Any]]:
        """
        Get list of invoices

        Args:
            limit: Maximum number of invoices to fetch
            state: Filter by state ('draft', 'posted', 'cancel')
        """
        try:
            # Build search domain
            domain = [['move_type', '=', 'out_invoice']]
            if state:
                domain.append(['state', '=', state])

            # Search for invoices
            invoice_ids = self.execute(
                'account.move', 'search',
                domain,
                {'limit': limit, 'order': 'date desc'}
            )

            # Read invoice details
            invoices = self.execute(
                'account.move', 'read',
                invoice_ids,
                ['name', 'partner_id', 'invoice_date', 'amount_total', 'state']
            )

            audit_logger.log_event(
                "odoo_invoices_fetched",
                f"Fetched {len(invoices)} invoices",
                details={"count": len(invoices), "state": state}
            )

            return invoices

        except Exception as e:
            print(f"❌ Error fetching invoices: {e}")
            audit_logger.log_error("odoo_fetch_error", str(e), None)
            return []

    def create_invoice(self, partner_id: int, lines: List[Dict[str, Any]]) -> Optional[int]:
        """
        Create a new invoice

        Args:
            partner_id: Customer ID
            lines: List of invoice line dictionaries with keys:
                   - product_id: Product ID
                   - quantity: Quantity
                   - price_unit: Unit price
                   - name: Description (optional)

        Returns:
            Invoice ID if successful, None otherwise
        """
        try:
            # Prepare invoice lines
            invoice_lines = []
            for line in lines:
                invoice_lines.append((0, 0, {
                    'product_id': line.get('product_id'),
                    'quantity': line.get('quantity', 1),
                    'price_unit': line.get('price_unit', 0),
                    'name': line.get('name', 'Product/Service')
                }))

            # Create invoice
            invoice_id = self.execute(
                'account.move', 'create',
                {
                    'move_type': 'out_invoice',
                    'partner_id': partner_id,
                    'invoice_line_ids': invoice_lines
                }
            )

            print(f"✅ Created invoice ID: {invoice_id}")
            audit_logger.log_event(
                "odoo_invoice_created",
                f"Created invoice for partner {partner_id}",
                details={"invoice_id": invoice_id, "partner_id": partner_id}
            )

            return invoice_id

        except Exception as e:
            print(f"❌ Error creating invoice: {e}")
            audit_logger.log_error("odoo_create_error", str(e), None)
            return None

    def post_invoice(self, invoice_id: int) -> bool:
        """Post (validate) an invoice"""
        try:
            self.execute(
                'account.move', 'action_post',
                [invoice_id]
            )

            print(f"✅ Posted invoice ID: {invoice_id}")
            audit_logger.log_event(
                "odoo_invoice_posted",
                f"Posted invoice {invoice_id}",
                details={"invoice_id": invoice_id}
            )

            return True

        except Exception as e:
            print(f"❌ Error posting invoice: {e}")
            audit_logger.log_error("odoo_post_error", str(e), None)
            return False

    # Product Operations

    def get_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of products"""
        try:
            # Search for products
            product_ids = self.execute(
                'product.product', 'search',
                [],
                {'limit': limit}
            )

            # Read product details
            products = self.execute(
                'product.product', 'read',
                product_ids,
                ['name', 'list_price', 'standard_price', 'type']
            )

            audit_logger.log_event(
                "odoo_products_fetched",
                f"Fetched {len(products)} products",
                details={"count": len(products)}
            )

            return products

        except Exception as e:
            print(f"❌ Error fetching products: {e}")
            audit_logger.log_error("odoo_fetch_error", str(e), None)
            return []

    # Expense Operations

    def get_expenses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of expenses"""
        try:
            # Search for expenses
            expense_ids = self.execute(
                'hr.expense', 'search',
                [],
                {'limit': limit, 'order': 'date desc'}
            )

            # Read expense details
            expenses = self.execute(
                'hr.expense', 'read',
                expense_ids,
                ['name', 'employee_id', 'total_amount', 'date', 'state']
            )

            audit_logger.log_event(
                "odoo_expenses_fetched",
                f"Fetched {len(expenses)} expenses",
                details={"count": len(expenses)}
            )

            return expenses

        except Exception as e:
            print(f"❌ Error fetching expenses: {e}")
            audit_logger.log_error("odoo_fetch_error", str(e), None)
            return []

    def create_expense(self, name: str, amount: float, employee_id: int) -> Optional[int]:
        """Create a new expense"""
        try:
            expense_id = self.execute(
                'hr.expense', 'create',
                {
                    'name': name,
                    'unit_amount': amount,
                    'employee_id': employee_id
                }
            )

            print(f"✅ Created expense: {name} (ID: {expense_id})")
            audit_logger.log_event(
                "odoo_expense_created",
                f"Created expense: {name}",
                details={"expense_id": expense_id, "amount": amount}
            )

            return expense_id

        except Exception as e:
            print(f"❌ Error creating expense: {e}")
            audit_logger.log_error("odoo_create_error", str(e), None)
            return None


def main():
    """Test Odoo client"""
    print("=" * 60)
    print("Odoo MCP Server - Test Client")
    print("=" * 60)
    print()

    # Initialize client
    client = OdooClient()

    # Authenticate
    if not client.authenticate():
        print("❌ Failed to authenticate")
        return

    # Test operations
    print("\n📋 Testing operations...")
    print()

    # Get customers
    print("👥 Fetching customers...")
    customers = client.get_customers(limit=5)
    print(f"Found {len(customers)} customers")
    for customer in customers[:3]:
        print(f"  - {customer['name']} ({customer.get('email', 'No email')})")

    # Get invoices
    print("\n💰 Fetching invoices...")
    invoices = client.get_invoices(limit=5)
    print(f"Found {len(invoices)} invoices")
    for invoice in invoices[:3]:
        print(f"  - {invoice['name']}: ${invoice['amount_total']} ({invoice['state']})")

    # Get products
    print("\n📦 Fetching products...")
    products = client.get_products(limit=5)
    print(f"Found {len(products)} products")
    for product in products[:3]:
        print(f"  - {product['name']}: ${product['list_price']}")

    print("\n✅ Test completed successfully!")


if __name__ == "__main__":
    main()
