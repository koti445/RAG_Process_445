# Northwind Corp — IT Operations Runbook (excerpt)

**Classification:** Internal — IT  
**Owner:** Platform Engineering

## Incident severity and SLA

| Severity | Description | Response SLA | Resolution target |
|----------|-------------|--------------|-------------------|
| SEV-1 | Production down | 15 minutes | 4 hours |
| SEV-2 | Major degradation | 30 minutes | 8 hours |
| SEV-3 | Minor impact | 4 hours | 3 business days |

All SEV-1 incidents require a bridge call and executive notification within 30 minutes.

## VPN access

Request VPN access via the **ServiceNow** catalog item "Remote Access — VPN". Approvals require manager + IT security. Standard provisioning time is **1 business day**.

## SSO and identity

Internal applications use **single sign-on (SSO)** through Okta. Do not create local passwords for SaaS tools that support SAML federation.

## Backup and restore

Production databases are backed up every **6 hours** with 35-day retention. Restore drills are performed quarterly; last drill ID: DR-2025-Q3.

## On-call rotation

Primary on-call carries the pager for **one week**. Escalation order: primary → secondary → engineering manager.

## Security logging

Authentication failures and admin actions are shipped to the SIEM within **5 minutes**. Retention: 400 days for compliance.
