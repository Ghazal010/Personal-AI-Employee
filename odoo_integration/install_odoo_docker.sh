#!/bin/bash
"""
Odoo 19 Community - Docker Installation Script
Automated setup for Odoo 19 with PostgreSQL
"""

set -e  # Exit on error

echo "=========================================="
echo "Odoo 19 Community - Docker Installation"
echo "=========================================="
echo ""

# Configuration
ODOO_VERSION="19.0"
ODOO_PORT="8069"
POSTGRES_USER="odoo"
POSTGRES_PASSWORD="odoo"
POSTGRES_DB="postgres"
ODOO_DATA_DIR="$HOME/odoo-data"
ODOO_CONFIG_DIR="$HOME/odoo-config"
ODOO_ADDONS_DIR="$HOME/odoo-addons"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker is installed"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Create directories
echo "📁 Creating directories..."
mkdir -p "$ODOO_DATA_DIR"
mkdir -p "$ODOO_CONFIG_DIR"
mkdir -p "$ODOO_ADDONS_DIR"
echo "✅ Directories created"
echo ""

# Create Odoo configuration file
echo "📝 Creating Odoo configuration..."
cat > "$ODOO_CONFIG_DIR/odoo.conf" << EOF
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = admin
db_host = db
db_port = 5432
db_user = $POSTGRES_USER
db_password = $POSTGRES_PASSWORD
EOF
echo "✅ Configuration file created"
echo ""

# Create docker-compose.yml
echo "🐳 Creating Docker Compose configuration..."
cat > "$ODOO_CONFIG_DIR/docker-compose.yml" << EOF
version: '3.1'
services:
  db:
    image: postgres:15
    container_name: odoo_db
    environment:
      - POSTGRES_DB=$POSTGRES_DB
      - POSTGRES_USER=$POSTGRES_USER
      - POSTGRES_PASSWORD=$POSTGRES_PASSWORD
    volumes:
      - odoo-db-data:/var/lib/postgresql/data
    restart: unless-stopped

  odoo:
    image: odoo:$ODOO_VERSION
    container_name: odoo_app
    depends_on:
      - db
    ports:
      - "$ODOO_PORT:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      - $ODOO_CONFIG_DIR/odoo.conf:/etc/odoo/odoo.conf
      - $ODOO_ADDONS_DIR:/mnt/extra-addons
    environment:
      - HOST=db
      - USER=$POSTGRES_USER
      - PASSWORD=$POSTGRES_PASSWORD
    restart: unless-stopped

volumes:
  odoo-web-data:
  odoo-db-data:
EOF
echo "✅ Docker Compose configuration created"
echo ""

# Start Odoo
echo "🚀 Starting Odoo 19..."
cd "$ODOO_CONFIG_DIR"
docker-compose up -d

echo ""
echo "⏳ Waiting for Odoo to start (this may take a minute)..."
sleep 30

# Check if Odoo is running
if docker ps | grep -q odoo_app; then
    echo ""
    echo "=========================================="
    echo "✅ Odoo 19 Installation Complete!"
    echo "=========================================="
    echo ""
    echo "📊 Access Odoo at: http://localhost:$ODOO_PORT"
    echo ""
    echo "🔐 Default Credentials:"
    echo "   Master Password: admin"
    echo "   (You'll create a database and user on first access)"
    echo ""
    echo "📁 Data Directories:"
    echo "   Config: $ODOO_CONFIG_DIR"
    echo "   Addons: $ODOO_ADDONS_DIR"
    echo ""
    echo "🛠️ Useful Commands:"
    echo "   View logs:    docker logs -f odoo_app"
    echo "   Stop Odoo:    cd $ODOO_CONFIG_DIR && docker-compose stop"
    echo "   Start Odoo:   cd $ODOO_CONFIG_DIR && docker-compose start"
    echo "   Restart:      cd $ODOO_CONFIG_DIR && docker-compose restart"
    echo "   Remove:       cd $ODOO_CONFIG_DIR && docker-compose down"
    echo ""
    echo "📖 Next Steps:"
    echo "   1. Open http://localhost:$ODOO_PORT in your browser"
    echo "   2. Create a new database"
    echo "   3. Install required modules (Accounting, CRM, etc.)"
    echo "   4. Configure your company settings"
    echo ""
else
    echo ""
    echo "❌ Odoo failed to start"
    echo "Check logs with: docker logs odoo_app"
    exit 1
fi
