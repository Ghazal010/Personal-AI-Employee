#!/usr/bin/env python3
"""
Odoo Skills
Skills for Odoo ERP operations via JSON-RPC
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_skills.skill_framework import AgentSkill, SkillResult, register_skill
from audit_logger import AuditLogger, EventType


@register_skill
class GetOdooCustomersSkill(AgentSkill):
    """Get list of customers from Odoo"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("odoo_skill")

    def get_description(self) -> str:
        return "Get list of customers from Odoo ERP"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "limit": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of customers to fetch"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute customer fetching"""
        try:
            limit = kwargs.get('limit', 10)

            # Import Odoo client
            from odoo_integration.odoo_mcp_server import OdooClient

            # Initialize and authenticate
            client = OdooClient()
            if not client.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Odoo"
                )

            # Get customers
            customers = client.get_customers(limit=limit)

            # Log skill execution
            self.audit_logger.log_event(
                "odoo_customers_fetched",
                f"GetOdooCustomersSkill executed: {len(customers)} customers found",
                details={"count": len(customers)}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(customers),
                    "customers": customers
                },
                metadata={"limit": limit}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error fetching Odoo customers: {str(e)}"
            )


@register_skill
class CreateOdooCustomerSkill(AgentSkill):
    """Create a new customer in Odoo"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("odoo_skill")

    def get_description(self) -> str:
        return "Create a new customer in Odoo ERP"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "name": {
                "type": str,
                "required": True,
                "description": "Customer name"
            },
            "email": {
                "type": str,
                "required": False,
                "description": "Customer email"
            },
            "phone": {
                "type": str,
                "required": False,
                "description": "Customer phone"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute customer creation"""
        try:
            name = kwargs.get('name')
            email = kwargs.get('email')
            phone = kwargs.get('phone')

            # Import Odoo client
            from odoo_integration.odoo_mcp_server import OdooClient

            # Initialize and authenticate
            client = OdooClient()
            if not client.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Odoo"
                )

            # Create customer
            partner_id = client.create_customer(name, email, phone)

            if not partner_id:
                return SkillResult(
                    success=False,
                    error="Failed to create customer in Odoo"
                )

            # Log skill execution
            self.audit_logger.log_event(
                "odoo_customer_created",
                f"CreateOdooCustomerSkill executed: {name}",
                details={"partner_id": partner_id, "name": name}
            )

            return SkillResult(
                success=True,
                data={
                    "partner_id": partner_id,
                    "name": name,
                    "email": email,
                    "phone": phone
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error creating Odoo customer: {str(e)}"
            )


@register_skill
class GetOdooInvoicesSkill(AgentSkill):
    """Get list of invoices from Odoo"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("odoo_skill")

    def get_description(self) -> str:
        return "Get list of invoices from Odoo ERP"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "limit": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of invoices to fetch"
            },
            "state": {
                "type": str,
                "required": False,
                "description": "Filter by state: draft, posted, cancel"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute invoice fetching"""
        try:
            limit = kwargs.get('limit', 10)
            state = kwargs.get('state')

            # Import Odoo client
            from odoo_integration.odoo_mcp_server import OdooClient

            # Initialize and authenticate
            client = OdooClient()
            if not client.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Odoo"
                )

            # Get invoices
            invoices = client.get_invoices(limit=limit, state=state)

            # Log skill execution
            self.audit_logger.log_event(
                "odoo_invoices_fetched",
                f"GetOdooInvoicesSkill executed: {len(invoices)} invoices found",
                details={"count": len(invoices), "state": state}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(invoices),
                    "invoices": invoices
                },
                metadata={"limit": limit, "state": state}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error fetching Odoo invoices: {str(e)}"
            )


@register_skill
class CreateOdooInvoiceSkill(AgentSkill):
    """Create a new invoice in Odoo"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("odoo_skill")

    def get_description(self) -> str:
        return "Create a new invoice in Odoo ERP"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "partner_id": {
                "type": int,
                "required": True,
                "description": "Customer ID"
            },
            "lines": {
                "type": list,
                "required": True,
                "description": "Invoice lines (list of dicts with product_id, quantity, price_unit)"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute invoice creation"""
        try:
            partner_id = kwargs.get('partner_id')
            lines = kwargs.get('lines', [])

            # Import Odoo client
            from odoo_integration.odoo_mcp_server import OdooClient

            # Initialize and authenticate
            client = OdooClient()
            if not client.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Odoo"
                )

            # Create invoice
            invoice_id = client.create_invoice(partner_id, lines)

            if not invoice_id:
                return SkillResult(
                    success=False,
                    error="Failed to create invoice in Odoo"
                )

            # Log skill execution
            self.audit_logger.log_event(
                "odoo_invoice_created",
                f"CreateOdooInvoiceSkill executed: invoice {invoice_id}",
                details={"invoice_id": invoice_id, "partner_id": partner_id}
            )

            return SkillResult(
                success=True,
                data={
                    "invoice_id": invoice_id,
                    "partner_id": partner_id,
                    "line_count": len(lines)
                }
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error creating Odoo invoice: {str(e)}"
            )


@register_skill
class GetOdooProductsSkill(AgentSkill):
    """Get list of products from Odoo"""

    def __init__(self):
        super().__init__()
        self.audit_logger = AuditLogger("odoo_skill")

    def get_description(self) -> str:
        return "Get list of products from Odoo ERP"

    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            "limit": {
                "type": int,
                "required": False,
                "default": 10,
                "description": "Maximum number of products to fetch"
            }
        }

    def execute(self, **kwargs) -> SkillResult:
        """Execute product fetching"""
        try:
            limit = kwargs.get('limit', 10)

            # Import Odoo client
            from odoo_integration.odoo_mcp_server import OdooClient

            # Initialize and authenticate
            client = OdooClient()
            if not client.authenticate():
                return SkillResult(
                    success=False,
                    error="Failed to authenticate with Odoo"
                )

            # Get products
            products = client.get_products(limit=limit)

            # Log skill execution
            self.audit_logger.log_event(
                "odoo_products_fetched",
                f"GetOdooProductsSkill executed: {len(products)} products found",
                details={"count": len(products)}
            )

            return SkillResult(
                success=True,
                data={
                    "count": len(products),
                    "products": products
                },
                metadata={"limit": limit}
            )

        except Exception as e:
            self.audit_logger.log_error("skill_execution", str(e), None)
            return SkillResult(
                success=False,
                error=f"Error fetching Odoo products: {str(e)}"
            )
