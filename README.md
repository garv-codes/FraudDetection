# 🏦 Fraud Detection System for Banking Transactions

A comprehensive full-stack Database Management System (DBMS) project that automatically detects suspicious banking transactions using intelligent database triggers and real-time monitoring.

## 📋 Project Overview

This system helps financial institutions protect their customers and prevent fraudulent activities through:

- **High Amount Detection**: Automatically flags transactions exceeding ₹10,000
- **Rapid Transaction Detection**: Detects more than 5 transactions within 5 minutes for the same user
- **Real-time Monitoring**: Instant fraud alerts using database triggers
- **Full CRUD Operations**: Create, Read, Update, and Delete transactions seamlessly

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Architecture**: MVC Pattern with Database Triggers

## 📁 Project Structure

```
fraud_project/
│
├── app.py                 # Main Flask application
├── db_init.py            # Database initialization script
├── db.sqlite             # SQLite database file (created after initialization)
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
│
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── home.html
│   ├── add_transaction.html
│   ├── view_transactions.html
│   ├── update_transaction.html
│   ├── fraud_alerts.html
│   └── about.html
│
└── static/              # Static files
    └── css/
        └── style.css
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd fraud_project
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Initialize the Database

Run the database initialization script to create tables, views, indexes, and triggers:

```bash
python db_init.py
```

When prompted, enter `y` to insert sample data for testing, or `n` to start with an empty database.

### Step 4: Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

## 📚 Database Schema

### Tables

#### `transactions`

- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `transaction_id` (TEXT UNIQUE)
- `user_id` (TEXT)
- `amount` (REAL)
- `location` (TEXT)
- `txn_time` (TEXT)
- `txn_type` (TEXT - 'Credit' or 'Debit')
- `status` (TEXT DEFAULT 'OK')

#### `fraud_alerts`

- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `transaction_id` (TEXT)
- `user_id` (TEXT)
- `amount` (REAL)
- `reason` (TEXT)
- `flagged_at` (TEXT DEFAULT CURRENT_TIMESTAMP)

### Database Features

- **Indexes**: Created on `user_id`, `txn_time`, and composite index on `(user_id, txn_time)` for optimized queries
- **Views**: `vw_suspicious` - Joins fraud_alerts with transactions for comprehensive reporting
- **Triggers**:
  - `trg_flag_high_amount`: Flags transactions > ₹10,000
  - `trg_flag_rapid_txns`: Flags when same user has >5 transactions within 5 minutes

## 🎯 Features

### 1. Home Page

- Project overview and description
- Team member information
- Key features showcase
- Quick action buttons

### 2. Add Transaction

- Form to add new banking transactions
- Automatic fraud detection on insert
- Auto-filled current timestamp option

### 3. View Transactions

- Display all transactions in a clean table
- Edit and Delete functionality
- Status indicators (OK/FLAGGED)
- Transaction type badges

### 4. Fraud Alerts

- View all suspicious transactions
- Detailed fraud detection reasons
- Summary statistics
- Real-time updates

### 5. About Page

- Project purpose and real-world use cases
- DBMS concepts implemented
- Technical stack information

## 💻 DBMS Concepts Implemented

1. **CRUD Operations**: Complete Create, Read, Update, Delete functionality
2. **Joins**: LEFT JOIN in views to combine related tables
3. **Aggregate Functions**: COUNT(\*) for fraud detection logic
4. **Subqueries**: Nested SELECT queries in triggers
5. **Views**: `vw_suspicious` for simplified querying
6. **Indexes**: Performance optimization on frequently queried columns
7. **Triggers**: Automatic fraud detection on transaction insert
8. **Stored Procedures**: Conceptual implementation through trigger logic

## 🎨 Design Features

- Clean, minimal light theme
- Responsive design (mobile-friendly)
- Card-based layout with hover effects
- Custom CSS (no Bootstrap)
- Modern gradient navigation bar
- Interactive tables with alternate row colors
- Flash message notifications
- Professional footer with dynamic year

## 📝 Usage Instructions

1. **Add a Transaction**:

   - Navigate to "Add Transaction"
   - Fill in transaction details
   - Submit the form
   - Fraud detection runs automatically

2. **View All Transactions**:

   - Go to "View Transactions"
   - See all recorded transactions
   - Use Edit/Delete buttons to manage records

3. **Check Fraud Alerts**:

   - Visit "Fraud Alerts" page
   - View all flagged suspicious transactions
   - See detailed reasons for flagging

4. **Update Transactions**:
   - Click "Edit" on any transaction
   - Modify the details
   - Fraud detection re-runs on update

## 🧪 Testing Fraud Detection

### Test High Amount Detection:

1. Add a transaction with amount > ₹10,000
2. Check the "Fraud Alerts" page
3. Transaction should be flagged

### Test Rapid Transaction Detection:

1. Add 6+ transactions for the same user within 5 minutes
2. Check the "Fraud Alerts" page
3. Transactions should be flagged for rapid activity

## 👨‍💻 Developer Information

**Developer**: Rishabh Jain  
**Institution**: NSUT (Netaji Subhas University of Technology)  
**Course**: B.Tech Information Technology - 2nd Year  
**Subject**: Database Management System (DBMS) Project

## 📄 License

This project is created for educational purposes as part of a DBMS course project.

## 🤝 Contributing

This is an academic project. However, suggestions and improvements are welcome!

## ⚠️ Notes

- The database file `db.sqlite` will be created automatically on first run
- All database operations use parameterized queries to prevent SQL injection
- Timestamps are stored as TEXT in SQLite format
- Flash messages appear at the top of pages for user feedback

## 🐛 Troubleshooting

**Issue**: Database not found

- **Solution**: Run `python db_init.py` first to create the database

**Issue**: Module not found errors

- **Solution**: Install dependencies with `pip install -r requirements.txt`

**Issue**: Port already in use

- **Solution**: Change the port in `app.py` (last line) or close the application using port 5000

---

**Made with ❤️ by Rishabh Jain | NSUT | DBMS Project © 2024**
