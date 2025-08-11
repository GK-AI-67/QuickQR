# QuickQR Database Setup

This document explains the database setup for the QuickQR application.

## Database Overview

QuickQR uses **SQLite** as its database, which is:
- ✅ **Free** - No licensing costs
- ✅ **Lightweight** - Single file database
- ✅ **Reliable** - ACID compliant
- ✅ **Portable** - Easy to backup and migrate
- ✅ **Perfect for small to medium applications**

## Database Schema

The application uses the following tables:

### 1. `qr_designs` - Main QR Code Designs
- Stores all QR code design information
- Includes styling parameters (colors, size, etc.)
- Tracks creation and update timestamps

### 2. `content_data` - Content Associated with QR Codes
- Stores text content and metadata
- Links to QR designs via foreign key
- Supports different content types (text, image, text+image)

### 3. `design_images` - Images for QR Designs
- Stores image files and metadata
- Links to QR designs via foreign key
- Includes file size, MIME type, and storage path

### 4. `qr_code_usage` - Analytics and Usage Tracking
- Tracks QR code scans and usage
- Stores IP addresses, user agents, and timestamps
- Enables analytics and insights

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

Run the database initialization script:

```bash
# Initialize database (creates tables)
python init_db.py

# Or reset database (drops and recreates tables)
python init_db.py reset
```

### 3. Start the Application

```bash
python main.py
```

The database will be automatically created as `quickqr.db` in the backend directory.

## Database Features

### ✅ User Design Storage
- All QR code designs are stored in the database
- Includes text content, images, and styling parameters
- Supports multiple content types

### ✅ Image Storage
- Images are stored in the `uploads/` directory
- Database tracks image metadata and file paths
- Automatic cleanup when designs are deleted

### ✅ Analytics
- Tracks QR code usage and scans
- Stores visitor information (IP, user agent, etc.)
- Provides usage statistics and insights

### ✅ Search and Management
- Search designs by title, description, or content
- CRUD operations for managing designs
- Pagination support for large datasets

## API Endpoints

### QR Design Management
- `GET /api/v1/qr/designs` - List all designs
- `GET /api/v1/qr/designs/{id}` - Get specific design
- `PUT /api/v1/qr/designs/{id}` - Update design
- `DELETE /api/v1/qr/designs/{id}` - Delete design
- `GET /api/v1/qr/designs/search/{query}` - Search designs
- `GET /api/v1/qr/designs/{id}/usage` - Get usage statistics

### Content Management
- `GET /api/v1/content/{qr_id}` - Get content data
- `DELETE /api/v1/content/{qr_id}` - Delete content
- `GET /api/v1/view/{qr_id}` - View content (HTML)

## Database Backup

### Manual Backup
```bash
# Copy the database file
cp quickqr.db quickqr_backup_$(date +%Y%m%d_%H%M%S).db
```

### Automated Backup (Optional)
You can set up automated backups using cron jobs or similar tools.

## Migration

If you need to migrate to a different database (PostgreSQL, MySQL, etc.):

1. Update the database URL in `app/core/database.py`
2. Install the appropriate database driver
3. Run migrations using Alembic (if configured)
4. Test thoroughly before deploying

## Troubleshooting

### Database Locked
If you get a "database is locked" error:
- Ensure no other processes are using the database
- Check if the application is running multiple instances
- Restart the application

### Permission Issues
- Ensure the application has write permissions to the backend directory
- Check file permissions on `quickqr.db` and `uploads/` directory

### Corrupted Database
If the database becomes corrupted:
```bash
# Reset the database
python init_db.py reset
```

## Performance Considerations

- SQLite is suitable for applications with moderate concurrent users
- For high-traffic applications, consider migrating to PostgreSQL or MySQL
- Regular database maintenance (VACUUM) can improve performance
- Monitor database size and implement cleanup strategies if needed 