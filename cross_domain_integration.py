#!/usr/bin/env python3
"""
Cross-Domain Integration Framework
Connects Personal (Email, WhatsApp, Social Media) with Business (Odoo ERP)
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agent_skills import execute_skill
from audit_logger import AuditLogger, EventType

# Setup audit logger
audit_logger = AuditLogger("cross_domain_integration")


class CrossDomainIntegration:
    """
    Cross-Domain Integration Framework

    Bridges Personal and Business domains:
    - Personal: Email, WhatsApp, Social Media, Tasks
    - Business: Odoo ERP, Accounting, Invoicing, CRM
    """

    def __init__(self):
        self.workflows = {}
        self.register_workflows()

    def register_workflows(self):
        """Register all cross-domain workflows"""
        self.workflows = {
            'email_to_customer': self.email_to_customer_workflow,
            'email_to_invoice': self.email_to_invoice_workflow,
            'email_to_expense': self.email_to_expense_workflow,
            'whatsapp_to_customer': self.whatsapp_to_customer_workflow,
            'social_to_customer': self.social_media_to_customer_workflow,
            'task_to_invoice': self.task_to_invoice_workflow,
        }

    def execute_workflow(self, workflow_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a cross-domain workflow

        Args:
            workflow_name: Name of the workflow to execute
            data: Input data for the workflow

        Returns:
            Workflow execution result
        """
        if workflow_name not in self.workflows:
            return {
                'success': False,
                'error': f'Workflow not found: {workflow_name}'
            }

        try:
            result = self.workflows[workflow_name](data)

            audit_logger.log_event(
                "cross_domain_workflow_executed",
                f"Executed workflow: {workflow_name}",
                details={'workflow': workflow_name, 'result': result}
            )

            return result

        except Exception as e:
            audit_logger.log_error("workflow_execution_error", str(e), None)
            return {
                'success': False,
                'error': str(e)
            }

    # Workflow Implementations

    def email_to_customer_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Email → Odoo Customer

        Extracts customer information from email and creates in Odoo

        Input:
            - email_from: Sender email address
            - email_subject: Email subject
            - email_body: Email body

        Output:
            - customer_id: Odoo partner ID
            - customer_name: Customer name
        """
        try:
            # Extract customer info from email
            email_from = data.get('email_from', '')

            # Parse name and email
            if '<' in email_from:
                name = email_from.split('<')[0].strip()
                email = email_from.split('<')[1].strip('>')
            else:
                name = email_from
                email = email_from

            # Check if customer already exists
            customers_result = execute_skill('GetOdooCustomersSkill', limit=100)

            if customers_result.success:
                existing = next(
                    (c for c in customers_result.data['customers'] if c.get('email') == email),
                    None
                )

                if existing:
                    return {
                        'success': True,
                        'customer_id': existing['id'],
                        'customer_name': existing['name'],
                        'action': 'found_existing'
                    }

            # Create new customer
            create_result = execute_skill(
                'CreateOdooCustomerSkill',
                name=name,
                email=email
            )

            if create_result.success:
                return {
                    'success': True,
                    'customer_id': create_result.data['partner_id'],
                    'customer_name': name,
                    'action': 'created_new'
                }
            else:
                return {
                    'success': False,
                    'error': create_result.error
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def email_to_invoice_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Email → Odoo Invoice

        Parses invoice request from email and creates invoice in Odoo

        Input:
            - email_from: Sender email
            - email_subject: Subject (should contain amount/description)
            - email_body: Body text

        Output:
            - invoice_id: Odoo invoice ID
            - customer_id: Customer ID
            - amount: Invoice amount
        """
        try:
            # First, ensure customer exists
            customer_result = self.email_to_customer_workflow(data)

            if not customer_result['success']:
                return customer_result

            customer_id = customer_result['customer_id']

            # Parse invoice details from email
            subject = data.get('email_subject', '')
            body = data.get('email_body', '')

            # Extract amount (look for $XXX or XXX USD patterns)
            amount_match = re.search(r'\$(\d+(?:\.\d{2})?)', subject + ' ' + body)
            if not amount_match:
                amount_match = re.search(r'(\d+(?:\.\d{2})?)\s*(?:USD|dollars?)', subject + ' ' + body, re.IGNORECASE)

            amount = float(amount_match.group(1)) if amount_match else 100.0

            # Extract description
            description = subject if subject else "Service"

            # Get first product (or create a generic service product)
            products_result = execute_skill('GetOdooProductsSkill', limit=1)

            if not products_result.success or not products_result.data['products']:
                return {
                    'success': False,
                    'error': 'No products found in Odoo. Please create at least one product.'
                }

            product_id = products_result.data['products'][0]['id']

            # Create invoice
            invoice_result = execute_skill(
                'CreateOdooInvoiceSkill',
                partner_id=customer_id,
                lines=[{
                    'product_id': product_id,
                    'quantity': 1,
                    'price_unit': amount,
                    'name': description
                }]
            )

            if invoice_result.success:
                return {
                    'success': True,
                    'invoice_id': invoice_result.data['invoice_id'],
                    'customer_id': customer_id,
                    'amount': amount,
                    'description': description
                }
            else:
                return {
                    'success': False,
                    'error': invoice_result.error
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def email_to_expense_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Email → Odoo Expense

        Creates expense from receipt email

        Input:
            - email_subject: Subject (should contain expense description)
            - email_body: Body (should contain amount)

        Output:
            - expense_id: Odoo expense ID
            - amount: Expense amount
        """
        try:
            subject = data.get('email_subject', '')
            body = data.get('email_body', '')

            # Extract amount
            amount_match = re.search(r'\$(\d+(?:\.\d{2})?)', subject + ' ' + body)
            if not amount_match:
                amount_match = re.search(r'(\d+(?:\.\d{2})?)\s*(?:USD|dollars?)', subject + ' ' + body, re.IGNORECASE)

            if not amount_match:
                return {
                    'success': False,
                    'error': 'Could not extract amount from email'
                }

            amount = float(amount_match.group(1))

            # Extract description
            description = subject if subject else "Expense"

            # Note: This requires hr.expense module and employee setup
            # For now, return a placeholder
            return {
                'success': True,
                'message': 'Expense workflow requires HR module setup',
                'amount': amount,
                'description': description,
                'action_required': 'Install HR Expenses module in Odoo'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def whatsapp_to_customer_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: WhatsApp → Odoo Customer

        Creates customer from WhatsApp contact

        Input:
            - contact_name: WhatsApp contact name
            - phone_number: Phone number

        Output:
            - customer_id: Odoo partner ID
        """
        try:
            name = data.get('contact_name', 'Unknown')
            phone = data.get('phone_number')

            # Create customer
            create_result = execute_skill(
                'CreateOdooCustomerSkill',
                name=name,
                phone=phone
            )

            if create_result.success:
                return {
                    'success': True,
                    'customer_id': create_result.data['partner_id'],
                    'customer_name': name
                }
            else:
                return {
                    'success': False,
                    'error': create_result.error
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def social_media_to_customer_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Social Media → Odoo Customer

        Creates customer from social media interaction

        Input:
            - platform: Platform name (twitter, facebook, instagram)
            - username: Social media username
            - name: Display name

        Output:
            - customer_id: Odoo partner ID
        """
        try:
            platform = data.get('platform', 'social')
            username = data.get('username', '')
            name = data.get('name', username)

            # Create customer with social media info in notes
            create_result = execute_skill(
                'CreateOdooCustomerSkill',
                name=name,
                email=f"{username}@{platform}.social"  # Placeholder email
            )

            if create_result.success:
                return {
                    'success': True,
                    'customer_id': create_result.data['partner_id'],
                    'customer_name': name,
                    'platform': platform
                }
            else:
                return {
                    'success': False,
                    'error': create_result.error
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def task_to_invoice_workflow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Workflow: Task → Odoo Invoice

        Creates invoice from completed task

        Input:
            - task_name: Task name
            - customer_email: Customer email
            - amount: Invoice amount

        Output:
            - invoice_id: Odoo invoice ID
        """
        try:
            # Get or create customer
            customer_result = self.email_to_customer_workflow({
                'email_from': data.get('customer_email', '')
            })

            if not customer_result['success']:
                return customer_result

            customer_id = customer_result['customer_id']
            amount = data.get('amount', 0)
            description = data.get('task_name', 'Service')

            # Get product
            products_result = execute_skill('GetOdooProductsSkill', limit=1)

            if not products_result.success or not products_result.data['products']:
                return {
                    'success': False,
                    'error': 'No products found in Odoo'
                }

            product_id = products_result.data['products'][0]['id']

            # Create invoice
            invoice_result = execute_skill(
                'CreateOdooInvoiceSkill',
                partner_id=customer_id,
                lines=[{
                    'product_id': product_id,
                    'quantity': 1,
                    'price_unit': amount,
                    'name': description
                }]
            )

            if invoice_result.success:
                return {
                    'success': True,
                    'invoice_id': invoice_result.data['invoice_id'],
                    'customer_id': customer_id,
                    'amount': amount
                }
            else:
                return {
                    'success': False,
                    'error': invoice_result.error
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Test cross-domain integration"""
    print("=" * 60)
    print("Cross-Domain Integration - Test")
    print("=" * 60)
    print()

    integration = CrossDomainIntegration()

    # Test: Email to Customer
    print("📧 Testing: Email → Customer")
    result = integration.execute_workflow('email_to_customer', {
        'email_from': 'John Doe <john@example.com>',
        'email_subject': 'Inquiry about services',
        'email_body': 'I would like to know more about your services.'
    })
    print(f"Result: {json.dumps(result, indent=2)}")
    print()

    # Test: Email to Invoice
    print("💰 Testing: Email → Invoice")
    result = integration.execute_workflow('email_to_invoice', {
        'email_from': 'Jane Smith <jane@example.com>',
        'email_subject': 'Invoice for consulting - $500',
        'email_body': 'Please send invoice for consulting services rendered.'
    })
    print(f"Result: {json.dumps(result, indent=2)}")
    print()

    print("✅ Cross-domain integration test completed!")


if __name__ == "__main__":
    main()
