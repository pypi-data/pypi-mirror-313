import sqlite3
from datetime import datetime
from contextlib import contextmanager
import logging

class TransactionDatabase:
    def __init__(self, db_path="transactions.db"):
        self.db_path = db_path
        self.initialize_database()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def initialize_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    amount REAL NOT NULL,
                    timestamp DATETIME NOT NULL,
                    status TEXT DEFAULT 'pending',
                    transaction_hash TEXT UNIQUE,
                    block_number INTEGER
                )
            ''')
            conn.commit()

    def record_transaction(self, transaction):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            timestamp = datetime.utcnow().isoformat()
            cursor.execute('''
                INSERT INTO transactions (sender, receiver, amount, timestamp, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction.sender, transaction.receiver, transaction.amount, 
                 timestamp, 'confirmed'))
            conn.commit()
            return cursor.lastrowid

    def get_transaction_history(self, address=None, limit=50):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if address:
                cursor.execute('''
                    SELECT * FROM transactions 
                    WHERE sender = ? OR receiver = ?
                    ORDER BY timestamp DESC LIMIT ?
                ''', (address, address, limit))
            else:
                cursor.execute('''
                    SELECT * FROM transactions 
                    ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
            return cursor.fetchall()

    def get_balance(self, address):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Outgoing transactions (negative)
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE sender = ? AND status = 'confirmed'
            ''', (address,))
            sent = cursor.fetchone()[0]
            
            # Incoming transactions (positive)
            cursor.execute('''
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE receiver = ? AND status = 'confirmed'
            ''', (address,))
            received = cursor.fetchone()[0]
            
            return received - sent
