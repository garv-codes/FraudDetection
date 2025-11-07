"""
Fraud Detection System for Banking Transactions
Flask Backend Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'fraud_detection_secret_key_2024'  # Required for flash messages

def get_connection():
    """Create and return a database connection and cursor."""
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

# ============ ROUTES ============

@app.route('/')
def home():
    """Home page route."""
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    """Add transaction route - GET shows form, POST processes it."""
    if request.method == 'POST':
        transaction_id = request.form.get('transaction_id', '').strip()
        user_id = request.form.get('user_id', '').strip()
        amount = request.form.get('amount', '').strip()
        location = request.form.get('location', '').strip()
        txn_time = request.form.get('txn_time', '').strip()
        txn_type = request.form.get('txn_type', '').strip()
        
        # Validation
        if not all([transaction_id, user_id, amount, location, txn_type]):
            flash('Please fill all required fields!', 'error')
            return render_template('add_transaction.html')
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Amount must be greater than 0!', 'error')
                return render_template('add_transaction.html')
        except ValueError:
            flash('Invalid amount format!', 'error')
            return render_template('add_transaction.html')
        
        # Convert datetime-local format to SQLite format
        if not txn_time:
            txn_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            # Convert from datetime-local format (YYYY-MM-DDTHH:MM) to SQLite format (YYYY-MM-DD HH:MM:SS)
            txn_time = txn_time.replace('T', ' ') + ':00'
        
        conn, cursor = get_connection()
        try:
            # Check if transaction_id already exists
            cursor.execute("SELECT transaction_id FROM transactions WHERE transaction_id = ?", (transaction_id,))
            if cursor.fetchone():
                flash('Transaction ID already exists!', 'error')
                return render_template('add_transaction.html')
            
            # Insert transaction
            cursor.execute("""
                INSERT INTO transactions 
                (transaction_id, user_id, amount, location, txn_time, txn_type, status)
                VALUES (?, ?, ?, ?, ?, ?, 'OK')
            """, (transaction_id, user_id, amount, location, txn_time, txn_type))
            
            conn.commit()
            flash('Transaction added successfully! Fraud detection triggered automatically.', 'success')
            return redirect(url_for('view_transactions'))
            
        except sqlite3.IntegrityError:
            flash('Transaction ID already exists!', 'error')
            conn.rollback()
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
            conn.rollback()
        finally:
            conn.close()
    
    # GET request - show form
    return render_template('add_transaction.html')

@app.route('/transactions')
def view_transactions():
    """View all transactions route."""
    conn, cursor = get_connection()
    try:
        cursor.execute("""
            SELECT * FROM transactions 
            ORDER BY txn_time DESC
        """)
        transactions = cursor.fetchall()
        return render_template('view_transactions.html', transactions=transactions)
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('view_transactions.html', transactions=[])
    finally:
        conn.close()

@app.route('/update/<transaction_id>', methods=['GET', 'POST'])
def update_transaction(transaction_id):
    """Update transaction route."""
    conn, cursor = get_connection()
    
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        amount = request.form.get('amount', '').strip()
        location = request.form.get('location', '').strip()
        txn_time = request.form.get('txn_time', '').strip()
        txn_type = request.form.get('txn_type', '').strip()
        
        # Validation
        if not all([user_id, amount, location, txn_time, txn_type]):
            flash('Please fill all required fields!', 'error')
            return redirect(url_for('update_transaction', transaction_id=transaction_id))
        
        try:
            amount = float(amount)
            if amount <= 0:
                flash('Amount must be greater than 0!', 'error')
                return redirect(url_for('update_transaction', transaction_id=transaction_id))
        except ValueError:
            flash('Invalid amount format!', 'error')
            return redirect(url_for('update_transaction', transaction_id=transaction_id))
        
        # Convert datetime-local format to SQLite format
        if txn_time:
            txn_time = txn_time.replace('T', ' ') + ':00'
        
        try:
            cursor.execute("""
                UPDATE transactions 
                SET user_id = ?, amount = ?, location = ?, txn_time = ?, txn_type = ?, status = 'OK'
                WHERE transaction_id = ?
            """, (user_id, amount, location, txn_time, txn_type, transaction_id))
            
            conn.commit()
            
            # Re-trigger fraud detection by deleting and re-inserting fraud alerts
            # (This is a simplified approach - in production, you'd have a stored procedure)
            cursor.execute("DELETE FROM fraud_alerts WHERE transaction_id = ?", (transaction_id,))
            
            # Check high amount
            if amount > 10000:
                cursor.execute("""
                    INSERT INTO fraud_alerts (transaction_id, user_id, amount, reason)
                    VALUES (?, ?, ?, ?)
                """, (transaction_id, user_id, amount, 
                      f'High amount transaction: ₹{amount} exceeds ₹10,000 limit'))
                cursor.execute("UPDATE transactions SET status = 'FLAGGED' WHERE transaction_id = ?", 
                             (transaction_id,))
            
            # Check rapid transactions
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM transactions
                WHERE user_id = ? 
                    AND txn_time >= datetime(?, '-5 minutes')
                    AND txn_time <= ?
            """, (user_id, txn_time, txn_time))
            result = cursor.fetchone()
            if result and result['count'] > 5:
                cursor.execute("""
                    INSERT INTO fraud_alerts (transaction_id, user_id, amount, reason)
                    VALUES (?, ?, ?, ?)
                """, (transaction_id, user_id, amount, 
                      f'Rapid transactions detected: {result["count"]} transactions within 5 minutes'))
                cursor.execute("UPDATE transactions SET status = 'FLAGGED' WHERE transaction_id = ?", 
                             (transaction_id,))
            
            conn.commit()
            flash('Transaction updated successfully!', 'success')
            return redirect(url_for('view_transactions'))
            
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
            conn.rollback()
        finally:
            conn.close()
    
    # GET request - show edit form
    try:
        cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            flash('Transaction not found!', 'error')
            return redirect(url_for('view_transactions'))
        return render_template('update_transaction.html', transaction=transaction)
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return redirect(url_for('view_transactions'))
    finally:
        conn.close()

@app.route('/delete/<transaction_id>')
def delete_transaction(transaction_id):
    """Delete transaction route."""
    conn, cursor = get_connection()
    try:
        # Also delete associated fraud alerts
        cursor.execute("DELETE FROM fraud_alerts WHERE transaction_id = ?", (transaction_id,))
        cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
        conn.commit()
        flash('Transaction deleted successfully!', 'success')
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        conn.rollback()
    finally:
        conn.close()
    return redirect(url_for('view_transactions'))

@app.route('/fraud')
def fraud_alerts():
    """View fraud alerts route."""
    conn, cursor = get_connection()
    try:
        # Using the view for better data
        cursor.execute("SELECT * FROM vw_suspicious ORDER BY flagged_at DESC")
        alerts = cursor.fetchall()
        return render_template('fraud_alerts.html', alerts=alerts)
    except sqlite3.Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('fraud_alerts.html', alerts=[])
    finally:
        conn.close()

@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

if __name__ == '__main__':
    print("=" * 50)
    print("Fraud Detection System - Flask Application")
    print("=" * 50)
    print("Server starting on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    app.run(debug=True, port=5000)

