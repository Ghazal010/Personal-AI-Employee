# Plan: Process Client Invoice Requests

**Created:** 2026-02-25
**Status:** Template
**Type:** Workflow Plan

## Objective

Create a standardized workflow for processing client invoice requests from initial request to payment received.

## Steps

### 1. Request Analysis ✓
- [x] Read incoming request from Inbox
- [x] Extract client details (name, email, project)
- [x] Extract financial details (amount, hours, rate)
- [x] Identify deadline
- [x] Determine priority level

### 2. Validation
- [ ] Verify project completion status
- [ ] Confirm hours worked match records
- [ ] Check rate against contract
- [ ] Validate client contact information
- [ ] Review for any outstanding issues

### 3. Invoice Generation
- [ ] Create invoice document with:
  - Invoice number (format: INV-YYYY-MM-###)
  - Client details
  - Project description
  - Itemized breakdown
  - Payment terms (Net 30)
  - Payment methods
- [ ] Save to /Pending_Approval/

### 4. Human Approval
- [ ] Present invoice for review
- [ ] Wait for approval/modifications
- [ ] If rejected: revise and resubmit
- [ ] If approved: proceed to sending

### 5. Delivery
- [ ] Send invoice via email
- [ ] CC accounting system
- [ ] Log in CRM
- [ ] Set payment reminder (Net 30)

### 6. Follow-up
- [ ] Track payment status
- [ ] Send reminder at Day 20 if unpaid
- [ ] Send final notice at Day 28 if unpaid
- [ ] Escalate if overdue

### 7. Completion
- [ ] Confirm payment received
- [ ] Update accounting records
- [ ] Move to /Done/
- [ ] Log in Business_Goals.md revenue

## Decision Points

**Requires Human Approval:**
- Any invoice > $100 (per Company Handbook)
- New clients (first invoice)
- Disputed amounts
- Payment plan requests

**Can Auto-Execute:**
- Recurring invoices < $100
- Pre-approved clients
- Standard payment terms

## Error Handling

**If client email bounces:**
- Try alternate contact method
- Check CRM for updated info
- Flag for manual follow-up

**If payment delayed:**
- Send polite reminder
- Offer payment plan if needed
- Don't auto-escalate before Day 30

**If dispute raised:**
- Pause collection
- Document issue
- Schedule resolution call
- Update invoice if needed

## Success Metrics

- Invoice sent within 24 hours of request
- Payment received within 30 days
- Zero billing disputes
- 100% accuracy on amounts

## Notes

This plan serves as a template. Each execution should:
1. Create a copy in /In_Progress/
2. Check off steps as completed
3. Log any deviations
4. Move to /Done/ when complete

---

**Template Version:** 1.0
**Last Updated:** 2026-02-25
