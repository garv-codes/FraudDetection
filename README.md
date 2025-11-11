
Fraud Detection System Overview

This project is a comprehensive full-stack Database Management System (DBMS) solution designed for real-time monitoring and detection of suspicious banking transactions.
It automatically flags fraudulent activity using intelligent database triggers tied directly to transaction insertions.


Detection Criteria: The system actively monitors for two specific fraud types:
    High Amount: Any transaction exceeding ₹10,000.
    Rapid Activity: More than 5 transactions by the same user within 5 minutes.


Technical Stack:
    Frontend: HTML,CSS
    Backend: Flask (Python)
    Database: SQLite3 

Key Database Features: The application relies on advanced DBMS concepts for reliability:
    Triggers: Ensure instant fraud checks upon data entry.
    Indexes: Optimize query performance on user and time columns.
    Views: Simplify reporting on suspicious transactions.


Setup in Three Steps:
    1.  Install dependencies: pip install -r requirements.txt
    2.  Initialize the database: python db_init.py
    3.  Run the application: python app.py


