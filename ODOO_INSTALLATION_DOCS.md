# Odoo 19 Community - Installation & Configuration Guide

**Version:** 1.0.0
**Last Updated:** 2026-03-10
**Status:** Ready for Installation

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation Methods](#installation-methods)
4. [Docker Installation (Recommended)](#docker-installation-recommended)
5. [Manual Installation](#manual-installation)
6. [Initial Configuration](#initial-configuration)
7. [Module Installation](#module-installation)
8. [Database Management](#database-management)
9. [Backup & Restore](#backup--restore)
10. [Troubleshooting](#troubleshooting)

---

## Overview

Odoo 19 Community is an open-source ERP (Enterprise Resource Planning) system that provides business management tools including:

- **Accounting** - Invoicing, expenses, payments
- **CRM** - Customer relationship management
- **Sales** - Quotations, orders, contracts
- **Inventory** - Stock management, warehousing
- **Project Management** - Tasks, timesheets
- **HR** - Employees, attendance, payroll
- **Website** - E-commerce, blog, forms
- **Marketing** - Email campaigns, automation

### Why Odoo for Personal AI Employee?

- Centralized business data management
- API access for automation
- Comprehensive accounting features
- Invoice generation and tracking
- Expense management
- Customer/vendor management

---

## Prerequisites

### System Requirements

**Minimum:**
- 2 CPU cores
- 4 GB RAM
- 20 GB disk space
- macOS 10.15+ / Linux / Windows 10+

**Recommended:**
- 4 CPU cores
- 8 GB RAM
- 50 GB disk space
- SSD storage

### Software Requirements

**Docker Installation (Recommended):**
- Docker Desktop 4.0+
- Docker Compose 2.0+

**Manual Installation:**
- Python 3.10+
- PostgreSQL 12+
- Node.js 16+ (for website features)
- wkhtmltopdf (for PDF reports)

---

## Installation Methods

### Method 1: Docker (Recommended)

**Pros:**
- Easy installation
- Isolated environment
- Easy backup/restore
- Cross-platform

**Cons:**
- Requires Docker Desktop
- Uses more resources

### Method 2: Manual Installation

**Pros:**
- Better performance
- More control
- Lower resource usage

**Cons:**
- Complex setup
- Platform-specific
- Manual dependency management

---

## Docker Installation (Recommended)

### Step 1: Install Docker Desktop

**macOS:**
1. Download from https://www.docker.com/products/docker-desktop
2. Install Docker.dmg
3. Start Docker Desktop
4. Verify: `docker --version`

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Windows:**
1. Download from https://www.docker.com/products/docker-desktop
2. Install Docker Desktop.exe
3. Enable WSL 2 backend
4. Start Docker Desktop

### Step 2: Run Installation Script

```bash
cd odoo_integration
./install_odoo_docker.sh
```

The script will:
1. Check Docker installation
2. Create necessary directories
3. Generate configuration files
4. Start Odoo and PostgreSQL containers
5. Display access information

### Step 3: Access Odoo

1. Open browser: http://localhost:8069
2. Create a new database
3. Set master password
4. Create admin user
5. Choose language and country

### Step 4: Verify Installation

```bash
# Check containers are running
docker ps

# View Odoo logs
docker logs -f odoo_app

# View database logs
docker logs -f odoo_db
```

---

## Manual Installation

### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
createuser -s odoo
createdb odoo
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser -s odoo
sudo -u postgres createdb odoo
```

### Step 2: Install Python Dependencies

```bash
# Install system dependencies
# macOS
brew install python@3.10 node npm wkhtmltopdf

# Ubuntu/Debian
sudo apt install python3 python3-pip python3-dev \
  libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev \
  libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
  libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
  libfribidi-dev libxcb1-dev libpq-dev node-less npm wkhtmltopdf
```

### Step 3: Install Odoo

```bash
# Clone Odoo repository
git clone https://github.com/odoo/odoo.git --depth 1 --branch 19.0 odoo19
cd odoo19

# Install Python dependencies
pip3 install -r requirements.txt

# Create configuration file
./odoo-bin --save --stop-after-init
```

### Step 4: Start Odoo

```bash
./odoo-bin -c ~/.odoorc
```

Access at: http://localhost:8069

---

## Initial Configuration

### Create Database

1. **Access Odoo:** http://localhost:8069
2. **Master Password:** Set a strong master password
3. **Database Name:** Choose a name (e.g., "mycompany")
4. **Email:** Your admin email
5. **Password:** Admin password
6. **Language:** Select your language
7. **Country:** Select your country
8. **Demo Data:** Uncheck (for production)

### Configure Company

1. **Go to Settings**
2. **Companies → Update Info**
3. **Fill in:**
   - Company name
   - Address
   - Phone
   - Email
   - Website
   - Tax ID
   - Logo

### Configure Users

1. **Settings → Users & Companies → Users**
2. **Create users** for team members
3. **Assign access rights** per module
4. **Set up email** for notifications

---

## Module Installation

### Essential Modules

**Accounting:**
```
Settings → Apps → Search "Accounting"
Install: Accounting
```

**CRM:**
```
Settings → Apps → Search "CRM"
Install: CRM
```

**Sales:**
```
Settings → Apps → Search "Sales"
Install: Sales Management
```

**Invoicing:**
```
Settings → Apps → Search "Invoicing"
Install: Invoicing
```

**Expenses:**
```
Settings → Apps → Search "Expenses"
Install: Expenses
```

### Recommended Modules

- **Contacts** - Customer/vendor management
- **Calendar** - Scheduling and meetings
- **Documents** - File management
- **Project** - Task management
- **Timesheets** - Time tracking
- **Website** - Public website

### Module Configuration

After installing each module:
1. Go to module settings
2. Configure options
3. Set up chart of accounts (Accounting)
4. Configure payment methods
5. Set up taxes
6. Configure email templates

---

## Database Management

### Backup Database

**Via Web Interface:**
1. Database Manager: http://localhost:8069/web/database/manager
2. Enter master password
3. Select database
4. Click "Backup"
5. Choose format (zip recommended)
6. Download backup file

**Via Command Line (Docker):**
```bash
# Backup database
docker exec odoo_db pg_dump -U odoo -d odoo > odoo_backup_$(date +%Y%m%d).sql

# Backup filestore
docker cp odoo_app:/var/lib/odoo/filestore ./odoo_filestore_backup
```

### Restore Database

**Via Web Interface:**
1. Database Manager: http://localhost:8069/web/database/manager
2. Enter master password
3. Click "Restore"
4. Upload backup file
5. Enter new database name
6. Click "Continue"

**Via Command Line (Docker):**
```bash
# Restore database
docker exec -i odoo_db psql -U odoo -d odoo < odoo_backup.sql

# Restore filestore
docker cp ./odoo_filestore_backup odoo_app:/var/lib/odoo/filestore
```

### Duplicate Database

```bash
# Create copy for testing
docker exec odoo_db createdb -U odoo -T odoo odoo_test
```

---

## Backup & Restore

### Automated Backup Script

Create `backup_odoo.sh`:

```bash
#!/bin/bash
BACKUP_DIR="$HOME/odoo-backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup database
docker exec odoo_db pg_dump -U odoo -d odoo | gzip > "$BACKUP_DIR/odoo_db_$DATE.sql.gz"

# Backup filestore
docker cp odoo_app:/var/lib/odoo/filestore "$BACKUP_DIR/filestore_$DATE"
tar -czf "$BACKUP_DIR/filestore_$DATE.tar.gz" -C "$BACKUP_DIR" "filestore_$DATE"
rm -rf "$BACKUP_DIR/filestore_$DATE"

echo "✅ Backup completed: $BACKUP_DIR"
```

### Schedule Automated Backups

**macOS/Linux (cron):**
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup_odoo.sh
```

### Backup Retention

```bash
# Keep last 30 days of backups
find $HOME/odoo-backups -name "odoo_db_*.sql.gz" -mtime +30 -delete
find $HOME/odoo-backups -name "filestore_*.tar.gz" -mtime +30 -delete
```

---

## Troubleshooting

### Issue: Odoo won't start

**Check Docker containers:**
```bash
docker ps -a
docker logs odoo_app
docker logs odoo_db
```

**Common causes:**
- Port 8069 already in use
- PostgreSQL not running
- Insufficient memory
- Configuration errors

**Solutions:**
```bash
# Change port in docker-compose.yml
ports:
  - "8070:8069"  # Use port 8070 instead

# Restart containers
cd ~/odoo-config
docker-compose restart
```

### Issue: Database connection failed

**Check PostgreSQL:**
```bash
docker exec odoo_db psql -U odoo -d postgres -c "SELECT 1"
```

**Reset database password:**
```bash
docker exec odoo_db psql -U postgres -c "ALTER USER odoo WITH PASSWORD 'newpassword';"
```

### Issue: Can't access Odoo web interface

**Check if Odoo is listening:**
```bash
curl http://localhost:8069
```

**Check firewall:**
```bash
# macOS
sudo pfctl -d  # Disable firewall temporarily

# Linux
sudo ufw allow 8069
```

### Issue: Slow performance

**Increase resources (Docker):**
1. Docker Desktop → Preferences → Resources
2. Increase CPUs to 4
3. Increase Memory to 8 GB
4. Apply & Restart

**Optimize PostgreSQL:**
```bash
# Edit postgresql.conf
docker exec odoo_db bash -c "echo 'shared_buffers = 256MB' >> /var/lib/postgresql/data/postgresql.conf"
docker-compose restart db
```

### Issue: Module installation fails

**Clear cache:**
```bash
docker exec odoo_app rm -rf /var/lib/odoo/sessions/*
docker-compose restart odoo
```

**Update module list:**
1. Settings → Apps
2. Click "Update Apps List"
3. Try installing again

---

## Management Commands

### Start/Stop Odoo

```bash
# Start
cd ~/odoo-config
docker-compose start

# Stop
docker-compose stop

# Restart
docker-compose restart

# View status
docker-compose ps
```

### View Logs

```bash
# Real-time logs
docker logs -f odoo_app

# Last 100 lines
docker logs --tail 100 odoo_app

# Save logs to file
docker logs odoo_app > odoo.log
```

### Access Odoo Shell

```bash
# Python shell with Odoo environment
docker exec -it odoo_app odoo shell -d odoo
```

### Update Odoo

```bash
# Pull latest image
docker pull odoo:19.0

# Recreate containers
cd ~/odoo-config
docker-compose down
docker-compose up -d
```

---

## Security Best Practices

### 1. Change Master Password

1. Database Manager: http://localhost:8069/web/database/manager
2. Click "Set Master Password"
3. Use strong password (20+ characters)
4. Store securely

### 2. Use Strong Admin Password

- Minimum 12 characters
- Mix of letters, numbers, symbols
- Unique password
- Enable 2FA if available

### 3. Restrict Database Manager

Edit `odoo.conf`:
```ini
[options]
list_db = False
```

### 4. Use HTTPS

Set up reverse proxy (nginx/Apache) with SSL certificate.

### 5. Regular Backups

- Daily automated backups
- Store backups off-site
- Test restore procedure

### 6. Keep Updated

- Monitor Odoo security advisories
- Update regularly
- Test updates in staging first

---

## Next Steps

After installation:

1. ✅ **Complete Initial Configuration**
   - Set up company
   - Create users
   - Configure modules

2. ✅ **Install Required Modules**
   - Accounting
   - Invoicing
   - CRM
   - Expenses

3. ✅ **Import Data**
   - Customers
   - Vendors
   - Products
   - Chart of accounts

4. ✅ **Configure Integrations**
   - Email server
   - Payment gateways
   - Bank feeds
   - API access

5. ✅ **Set Up Automation**
   - Create MCP server (Task #2)
   - Integrate with Personal AI Employee
   - Automate invoice generation
   - Automate expense tracking

---

## Summary

Odoo 19 Community provides:

- ✅ **Complete ERP System** - All business management tools
- ✅ **Docker Installation** - Easy setup and management
- ✅ **Comprehensive Modules** - Accounting, CRM, Sales, etc.
- ✅ **API Access** - Integration with Personal AI Employee
- ✅ **Backup & Restore** - Data protection
- ✅ **Scalable** - Grows with your business

**Status:** Ready for Installation
**Version:** 1.0.0
**Last Updated:** 2026-03-10

---

## Quick Start

```bash
# Install Odoo 19 with Docker
cd odoo_integration
./install_odoo_docker.sh

# Access Odoo
open http://localhost:8069

# Create database and start using!
```

**Installation complete! 🎉**
