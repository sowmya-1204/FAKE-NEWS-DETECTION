import sqlite3

# Connect to database (creates file if not exists)
conn = sqlite3.connect("nlp.db")
cur = conn.cursor()

# Create processed_text table
cur.execute("""
CREATE TABLE IF NOT EXISTS processed_text (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ori_text TEXT NOT NULL,
    cleaned_text TEXT NOT NULL
)
""")

# Create entities table
cur.execute("""
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity TEXT NOT NULL,
    entity_type TEXT NOT NULL
)
""")

# Save changes and close connection
conn.commit()
conn.close()

print("Database created successfully!")