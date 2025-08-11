#!/usr/bin/env python3
"""
Database initialization script for QuickQR
This script creates the database tables and can be used for initial setup.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.core.database import create_tables, engine
from app.models.database_models import Base

def init_database():
    """Initialize the database by creating all tables"""
    print("Initializing QuickQR database...")
    
    try:
        # Create all tables
        create_tables()
        print("✅ Database tables created successfully!")
        
        # Verify tables were created
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {', '.join(tables)}")
        
        print("\n🎉 Database initialization completed successfully!")
        print("You can now start the QuickQR application.")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    print("Resetting QuickQR database...")
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("🗑️  All tables dropped.")
        
        # Create all tables
        create_tables()
        print("✅ Database tables recreated successfully!")
        
        print("\n🎉 Database reset completed successfully!")
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        reset_database()
    else:
        init_database() 