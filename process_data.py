import pandas as pd
import sqlite3
from utils import normalize_arabic

# Configuration
XLSX_FILE = 'data.xlsx'
DB_FILE = 'data.db'
TABLE_NAME = 'students'
SEATING_NO_COL = 'seating_no'
NAME_COL = 'name'
DEGREE_COL = 'degree'
NORMALIZED_NAME_COL = 'normalized_name'

df = pd.read_excel(XLSX_FILE)
df.rename(columns={
    'seating_no': SEATING_NO_COL,
    'arabic_name': NAME_COL,
    'total_degree': DEGREE_COL
}, inplace=True)

df[NORMALIZED_NAME_COL] = df[NAME_COL].apply(normalize_arabic)

conn = sqlite3.connect(DB_FILE)

db_df = df[[SEATING_NO_COL, NAME_COL, DEGREE_COL, NORMALIZED_NAME_COL]].copy()
db_df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

conn.execute(f'CREATE INDEX idx_normalized_name ON {TABLE_NAME} ({NORMALIZED_NAME_COL});')
conn.execute(f'CREATE INDEX idx_seating_no ON {TABLE_NAME} ({SEATING_NO_COL});')
conn.close()

print("Database created successfully as data.db") 