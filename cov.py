import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore

# Connect to SQLite database
conn = sqlite3.connect('./db.sqlite3')
cursor = conn.cursor()

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/Users/rahys/Downloads/dbmigration-1e28d-firebase-adminsdk-4xp9c-bb9d132f42.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Function to fetch table data as a list of dictionaries
def fetch_table_data(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]  # Extract column names

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Convert rows to list of dictionaries using column names
    data = [dict(zip(columns, row)) for row in rows]
    return data

# Fetch and insert books data into Firestore
books = fetch_table_data('store_book')
for book in books:
    doc_ref = db.collection('books').document(str(book['id']))  # Ensure 'id' is used as the document ID
    doc_ref.set(book)  # Firestore accepts a dictionary directly

# Fetch and insert transactions data into Firestore
transactions = fetch_table_data('store_transaction')
for transaction in transactions:
    doc_ref = db.collection('transactions').document(str(transaction['id']))  # Ensure 'id' is used as the document ID
    doc_ref.set(transaction)  # Firestore accepts a dictionary directly

# Close SQLite connection
conn.close()

# Verify data in Firestore
books_collection = db.collection('books')
transactions_collection = db.collection('transactions')

print("Books in Firestore:")
for doc in books_collection.stream():
    print(f"{doc.id}: {doc.to_dict()}")

print("\nTransactions in Firestore:")
for doc in transactions_collection.stream():
    print(f"{doc.id}: {doc.to_dict()}")
