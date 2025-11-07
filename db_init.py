"""
Database Initialization Script
Run this script once to create the database, tables, views, indexes, and triggers.
"""

import sqlite3
from datetime import datetime

def get_connection():
    """Create and return a database connection and cursor."""
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):
    """Create all required tables."""
    print("Creating tables...")
    
    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            location TEXT NOT NULL,
            txn_time TEXT NOT NULL,
            txn_type TEXT NOT NULL CHECK(txn_type IN ('Credit', 'Debit')),
            status TEXT DEFAULT 'OK'
        )
    """)
    
    # Create fraud_alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            reason TEXT NOT NULL,
            flagged_at TEXT DEFAULT (datetime('now'))
        )
    """)
    
    print("✓ Tables created successfully")

def create_indexes(cursor):
    """Create indexes for better query performance."""
    print("Creating indexes...")
    
    try:
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id ON transactions(user_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_txn_time ON transactions(txn_time)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_time ON transactions(user_id, txn_time)
        """)
        
        print("✓ Indexes created successfully")
    except sqlite3.Error as e:
        print(f"Index creation note: {e}")

def create_view(cursor):
    """Create view for suspicious transactions."""
    print("Creating view...")
    
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS vw_suspicious AS
        SELECT 
            fa.id,
            fa.transaction_id,
            fa.user_id,
            fa.amount,
            fa.reason,
            fa.flagged_at,
            t.location,
            t.txn_time,
            t.txn_type
        FROM fraud_alerts fa
        LEFT JOIN transactions t ON fa.transaction_id = t.transaction_id
        ORDER BY fa.flagged_at DESC
    """)
    
    print("✓ View created successfully")

def create_triggers(cursor):
    """Create triggers for automatic fraud detection."""
    print("Creating triggers...")
    
    # Trigger 1: Flag high amount transactions (> ₹10,000)
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_flag_high_amount
        AFTER INSERT ON transactions
        FOR EACH ROW
        WHEN NEW.amount > 10000
        BEGIN
            INSERT INTO fraud_alerts (transaction_id, user_id, amount, reason)
            VALUES (NEW.transaction_id, NEW.user_id, NEW.amount, 
                    'High amount transaction: ₹' || NEW.amount || ' exceeds ₹10,000 limit');
            
            UPDATE transactions 
            SET status = 'FLAGGED' 
            WHERE transaction_id = NEW.transaction_id;
        END
    """)
    
    # Trigger 2: Flag rapid transactions (more than 5 transactions within 5 minutes)
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_flag_rapid_txns
        AFTER INSERT ON transactions
        FOR EACH ROW
        BEGIN
            INSERT INTO fraud_alerts (transaction_id, user_id, amount, reason)
            SELECT 
                NEW.transaction_id,
                NEW.user_id,
                NEW.amount,
                'Rapid transactions detected: ' || COUNT(*) || ' transactions within 5 minutes'
            FROM transactions
            WHERE user_id = NEW.user_id
                AND txn_time >= datetime(NEW.txn_time, '-5 minutes')
                AND txn_time <= NEW.txn_time
            HAVING COUNT(*) > 5;
            
            UPDATE transactions 
            SET status = 'FLAGGED' 
            WHERE transaction_id = NEW.transaction_id
                AND (SELECT COUNT(*) 
                     FROM transactions 
                     WHERE user_id = NEW.user_id
                         AND txn_time >= datetime(NEW.txn_time, '-5 minutes')
                         AND txn_time <= NEW.txn_time) > 5;
        END
    """)
    
    print("✓ Triggers created successfully")

def insert_sample_data(cursor):
    """Insert sample data for testing."""
    print("Inserting sample data...")
    
    sample_transactions = [
        ('TXN001', 'USER001', 5000.00, 'Delhi', '2024-01-15 10:00:00', 'Credit', 'OK'),
        ('TXN002', 'USER001', 12000.00, 'Mumbai', '2024-01-15 10:01:00', 'Debit', 'OK'),
        ('TXN003', 'USER002', 8000.00, 'Bangalore', '2024-01-15 11:00:00', 'Credit', 'OK'),
        ('TXN004', 'USER001', 1500.00, 'Delhi', '2024-01-15 10:02:00', 'Debit', 'OK'),
        ('TXN005', 'USER001', 2000.00, 'Delhi', '2024-01-15 10:03:00', 'Credit', 'OK'),
        ('TXN006', 'USER001', 3000.00, 'Delhi', '2024-01-15 10:04:00', 'Debit', 'OK'),
        ('TXN007', 'USER001', 2500.00, 'Delhi', '2024-01-15 10:05:00', 'Credit', 'OK'),
        ('TXN008', 'USER001', 1800.00, 'Delhi', '2024-01-15 10:06:00', 'Debit', 'OK'),
    ]
    
    try:
        cursor.executemany("""
            INSERT OR IGNORE INTO transactions 
            (transaction_id, user_id, amount, location, txn_time, txn_type, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_transactions)
        print("✓ Sample data inserted successfully")
    except sqlite3.Error as e:
        print(f"Note: Some sample data may already exist: {e}")

def main():
    """Main initialization function."""
    print("=" * 50)
    print("Fraud Detection System - Database Initialization")
    print("=" * 50)
    
    conn, cursor = get_connection()
    
    try:
        create_tables(cursor)
        create_indexes(cursor)
        create_view(cursor)
        create_triggers(cursor)
        
        # Ask user if they want sample data
        response = input("\nInsert sample data for testing? (y/n): ").strip().lower()
        if response == 'y':
            insert_sample_data(cursor)
        
        conn.commit()
        print("\n" + "=" * 50)
        print("✓ Database initialization completed successfully!")
        print("=" * 50)
        
    except sqlite3.Error as e:
        print(f"\n✗ Database error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()

