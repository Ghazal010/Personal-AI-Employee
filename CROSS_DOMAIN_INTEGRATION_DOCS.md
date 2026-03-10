# Cross-Domain Integration - Documentation

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Workflows](#workflows)
4. [Usage](#usage)
5. [Integration Examples](#integration-examples)
6. [Configuration](#configuration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The Cross-Domain Integration Framework bridges the Personal and Business domains of the Personal AI Employee system, enabling seamless data flow and automation between:

**Personal Domain:**
- Email (Gmail)
- WhatsApp
- Twitter/X
- Facebook & Instagram
- Task Management

**Business Domain:**
- Odoo ERP
- Accounting
- Invoicing
- CRM
- Expense Management

### Key Benefits

- **Automated Workflows** - Connect personal communications to business operations
- **Data Synchronization** - Keep customer data consistent across systems
- **Time Savings** - Eliminate manual data entry
- **Error Reduction** - Automated data extraction and validation
- **Audit Trail** - All cross-domain operations logged

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  PERSONAL DOMAIN                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Email   │  │ WhatsApp │  │ Twitter  │  │ Facebook │   │
│  │  (Gmail) │  │          │  │    /X    │  │Instagram │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
└───────┼─────────────┼──────────────┼─────────────┼──────────┘
        │             │              │             │
        ▼             ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│           CROSS-DOMAIN INTEGRATION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Workflow Engine                             │    │
│  ├────────────────────────────────────────────────────┤    │
│  │  • email_to_customer                               │    │
│  │  • email_to_invoice                                │    │
│  │  • email_to_expense                                │    │
│  │  • whatsapp_to_customer                            │    │
│  │  • social_to_customer                              │    │
│  │  • task_to_invoice                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Agent Skills Framework                      │    │
│  ├────────────────────────────────────────────────────┤    │
│  │  • Email Skills                                     │    │
│  │  • WhatsApp Skills                                  │    │
│  │  • Social Media Skills                              │    │
│  │  • Odoo Skills                                      │    │
│  │  • Task Skills                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└───────┬─────────────┬──────────────┬─────────────┬──────────┘
        │             │              │             │
        ▼             ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                  BUSINESS DOMAIN                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   CRM    │  │Invoicing │  │Accounting│  │ Expenses │   │
│  │(Customers)│  │          │  │          │  │          │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │              │             │          │
│       └─────────────┴──────────────┴─────────────┘          │
│                          │                                   │
│                    ┌─────▼─────┐                            │
│                    │ Odoo ERP  │                            │
│                    └───────────┘                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Personal Event (Email, WhatsApp, Social Media)
   ↓
2. Event Detection (Watchers/Monitors)
   ↓
3. Action File Creation (Obsidian Vault)
   ↓
4. Cross-Domain Workflow Trigger
   ↓
5. Data Extraction & Transformation
   ↓
6. Agent Skills Execution
   ↓
7. Business System Update (Odoo)
   ↓
8. Audit Logging
   ↓
9. Confirmation & Notification
```

---

## Workflows

### 1. Email → Customer

**Purpose:** Automatically create Odoo customers from email senders

**Trigger:** New email received

**Process:**
1. Extract sender name and email
2. Check if customer exists in Odoo
3. If not exists, create new customer
4. Return customer ID

**Input:**
```python
{
    'email_from': 'John Doe <john@example.com>',
    'email_subject': 'Inquiry about services',
    'email_body': 'Email content...'
}
```

**Output:**
```python
{
    'success': True,
    'customer_id': 15,
    'customer_name': 'John Doe',
    'action': 'created_new'  # or 'found_existing'
}
```

---

### 2. Email → Invoice

**Purpose:** Generate invoices from email requests

**Trigger:** Email with invoice request

**Process:**
1. Create/find customer (via email_to_customer)
2. Extract amount from email (regex: $XXX or XXX USD)
3. Extract description from subject
4. Get product from Odoo
5. Create draft invoice
6. Return invoice ID

**Input:**
```python
{
    'email_from': 'Jane Smith <jane@example.com>',
    'email_subject': 'Invoice for consulting - $500',
    'email_body': 'Please send invoice...'
}
```

**Output:**
```python
{
    'success': True,
    'invoice_id': 10,
    'customer_id': 15,
    'amount': 500.0,
    'description': 'Invoice for consulting'
}
```

---

### 3. Email → Expense

**Purpose:** Create expenses from receipt emails

**Trigger:** Email with receipt/expense

**Process:**
1. Extract amount from email
2. Extract description
3. Create expense in Odoo (requires HR module)

**Input:**
```python
{
    'email_subject': 'Receipt - Office Supplies',
    'email_body': 'Total: $45.99'
}
```

**Output:**
```python
{
    'success': True,
    'amount': 45.99,
    'description': 'Receipt - Office Supplies',
    'action_required': 'Install HR Expenses module'
}
```

---

### 4. WhatsApp → Customer

**Purpose:** Create customers from WhatsApp contacts

**Trigger:** New WhatsApp chat

**Process:**
1. Extract contact name and phone
2. Create customer in Odoo
3. Return customer ID

**Input:**
```python
{
    'contact_name': 'John Smith',
    'phone_number': '+1234567890'
}
```

**Output:**
```python
{
    'success': True,
    'customer_id': 16,
    'customer_name': 'John Smith'
}
```

---

### 5. Social Media → Customer

**Purpose:** Create customers from social media interactions

**Trigger:** Social media mention/message

**Process:**
1. Extract username and display name
2. Create customer with social media info
3. Return customer ID

**Input:**
```python
{
    'platform': 'twitter',
    'username': 'johndoe',
    'name': 'John Doe'
}
```

**Output:**
```python
{
    'success': True,
    'customer_id': 17,
    'customer_name': 'John Doe',
    'platform': 'twitter'
}
```

---

### 6. Task → Invoice

**Purpose:** Generate invoices from completed tasks

**Trigger:** Task marked as done

**Process:**
1. Get/create customer
2. Extract amount and description
3. Create invoice
4. Return invoice ID

**Input:**
```python
{
    'task_name': 'Website Development',
    'customer_email': 'client@example.com',
    'amount': 2500.0
}
```

**Output:**
```python
{
    'success': True,
    'invoice_id': 11,
    'customer_id': 15,
    'amount': 2500.0
}
```

---

## Usage

### Python API

```python
from cross_domain_integration import CrossDomainIntegration

# Initialize
integration = CrossDomainIntegration()

# Execute workflow
result = integration.execute_workflow('email_to_customer', {
    'email_from': 'John Doe <john@example.com>',
    'email_subject': 'Inquiry',
    'email_body': 'I need information...'
})

if result['success']:
    print(f"Customer created: {result['customer_id']}")
else:
    print(f"Error: {result['error']}")
```

### Command Line

```bash
# Test cross-domain integration
python3 cross_domain_integration.py
```

### Integration with Ralph Wiggum Loop

Add to Ralph Wiggum Loop for automated execution:

```python
# In ralph_wiggum_loop.py
from cross_domain_integration import CrossDomainIntegration

integration = CrossDomainIntegration()

# In monitoring cycle
for email in new_emails:
    # Auto-create customer
    result = integration.execute_workflow('email_to_customer', {
        'email_from': email['from'],
        'email_subject': email['subject'],
        'email_body': email['body']
    })

    # If invoice request detected
    if 'invoice' in email['subject'].lower():
        invoice_result = integration.execute_workflow('email_to_invoice', {
            'email_from': email['from'],
            'email_subject': email['subject'],
            'email_body': email['body']
        })
```

---

## Integration Examples

### Example 1: Automated Customer Creation

**Scenario:** New email arrives from potential customer

**Flow:**
1. Gmail Watcher detects new email
2. Creates action file in Obsidian
3. Cross-domain workflow triggered
4. Customer created in Odoo
5. Confirmation logged

**Code:**
```python
# Automatic trigger in gmail_watcher_enhanced.py
from cross_domain_integration import CrossDomainIntegration

integration = CrossDomainIntegration()

for email in new_emails:
    result = integration.execute_workflow('email_to_customer', {
        'email_from': email['from'],
        'email_subject': email['subject'],
        'email_body': email['body']
    })

    if result['success']:
        print(f"✅ Customer {result['customer_name']} created/found")
```

---

### Example 2: Invoice Generation from Email

**Scenario:** Client emails requesting invoice

**Email Subject:** "Invoice for March consulting - $2,500"

**Flow:**
1. Email detected
2. Amount extracted: $2,500
3. Customer created/found
4. Invoice created in Odoo
5. Invoice ID returned

**Code:**
```python
result = integration.execute_workflow('email_to_invoice', {
    'email_from': 'client@company.com',
    'email_subject': 'Invoice for March consulting - $2,500',
    'email_body': 'Please send invoice for services rendered.'
})

# Result:
# {
#   'success': True,
#   'invoice_id': 42,
#   'customer_id': 15,
#   'amount': 2500.0,
#   'description': 'Invoice for March consulting'
# }
```

---

### Example 3: WhatsApp to CRM

**Scenario:** New WhatsApp conversation with potential client

**Flow:**
1. WhatsApp Monitor detects new chat
2. Contact info extracted
3. Customer created in Odoo CRM
4. Sales opportunity created

**Code:**
```python
result = integration.execute_workflow('whatsapp_to_customer', {
    'contact_name': 'Maria Garcia',
    'phone_number': '+34612345678'
})

# Customer now in Odoo CRM for follow-up
```

---

### Example 4: Social Media Lead Capture

**Scenario:** Twitter mention from interested party

**Flow:**
1. Twitter Monitor detects mention
2. User info extracted
3. Lead created in Odoo CRM
4. Follow-up task created

**Code:**
```python
result = integration.execute_workflow('social_to_customer', {
    'platform': 'twitter',
    'username': 'potential_client',
    'name': 'Potential Client'
})

# Lead captured for sales team
```

---

## Configuration

### Enable Workflows

Edit `cross_domain_integration.py` to enable/disable workflows:

```python
# Enable/disable specific workflows
ENABLED_WORKFLOWS = {
    'email_to_customer': True,
    'email_to_invoice': True,
    'email_to_expense': False,  # Requires HR module
    'whatsapp_to_customer': True,
    'social_to_customer': True,
    'task_to_invoice': True,
}
```

### Workflow Triggers

Configure automatic triggers in respective monitors:

**Gmail Watcher:**
```python
# In gmail_watcher_enhanced.py
if AUTO_CREATE_CUSTOMERS:
    integration.execute_workflow('email_to_customer', email_data)
```

**WhatsApp Monitor:**
```python
# In whatsapp_monitor_enhanced.py
if AUTO_CREATE_CUSTOMERS:
    integration.execute_workflow('whatsapp_to_customer', chat_data)
```

---

## Best Practices

### 1. Test Workflows Individually

```python
# Test each workflow before enabling automation
integration = CrossDomainIntegration()

# Test with sample data
test_data = {
    'email_from': 'test@example.com',
    'email_subject': 'Test',
    'email_body': 'Test body'
}

result = integration.execute_workflow('email_to_customer', test_data)
print(result)
```

### 2. Monitor Audit Logs

```bash
# Check cross-domain operations
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{
  "component": "cross_domain_integration",
  "limit": 20
}'
```

### 3. Handle Errors Gracefully

```python
result = integration.execute_workflow('email_to_invoice', data)

if not result['success']:
    # Log error
    print(f"Workflow failed: {result['error']}")

    # Create manual task for review
    execute_skill('CreateTaskSkill',
        title="Review failed invoice creation",
        description=f"Error: {result['error']}"
    )
```

### 4. Validate Data Before Processing

```python
# Validate email format
if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
    print("Invalid email format")
    return

# Validate amount
if amount <= 0:
    print("Invalid amount")
    return
```

### 5. Use Staging Environment

- Test workflows in Odoo test database first
- Verify data extraction accuracy
- Check for edge cases
- Monitor performance

---

## Troubleshooting

### Issue: Customer Creation Fails

**Error:** `Failed to create customer in Odoo`

**Solutions:**
1. Verify Odoo is running
2. Check Odoo credentials
3. Ensure user has customer creation rights
4. Check audit logs for details

### Issue: Amount Extraction Fails

**Error:** `Could not extract amount from email`

**Solutions:**
1. Check email format (should contain $XXX or XXX USD)
2. Update regex pattern in workflow
3. Add manual amount parameter
4. Review email content

### Issue: Workflow Not Executing

**Symptoms:** No cross-domain operations happening

**Solutions:**
1. Check if workflow is enabled
2. Verify triggers are configured
3. Check audit logs for errors
4. Test workflow manually

### Issue: Duplicate Customers

**Symptoms:** Same customer created multiple times

**Solutions:**
1. Improve duplicate detection logic
2. Search by email before creating
3. Use Odoo's duplicate detection
4. Merge duplicates in Odoo

---

## Summary

The Cross-Domain Integration Framework provides:

- ✅ **6 Automated Workflows** - Connect personal and business systems
- ✅ **Seamless Data Flow** - Automatic synchronization
- ✅ **Error Handling** - Graceful failure management
- ✅ **Audit Logging** - Complete operation tracking
- ✅ **Extensible Architecture** - Easy to add new workflows
- ✅ **Production Ready** - Tested and documented

**Status:** Production Ready
**Version:** 1.0.0
**Last Updated:** 2026-03-10

---

## Quick Start

```bash
# Test cross-domain integration
python3 cross_domain_integration.py

# Enable in Ralph Wiggum Loop
# Edit ralph_wiggum_loop.py to add workflow calls

# Monitor operations
python3 skills_cli.py --skill QueryAuditLogsSkill --params '{
  "component": "cross_domain_integration"
}'
```

**Integration complete! 🎉**
