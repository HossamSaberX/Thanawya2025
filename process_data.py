import pandas as pd
import sqlite3
from utils import normalize_arabic

# Configuration
XLSX_FILE = 'data.xlsx'
DB1_FILE = 'data1.db'
DB2_FILE = 'data2.db'
TABLE_NAME = 'students'
SEATING_NO_COL = 'seating_no'
ARABIC_NAME_COL = 'arabic_name'
TOTAL_DEGREE_COL = 'total_degree'
NORMALIZED_NAME_COL = 'normalized_name'


df = pd.read_excel(XLSX_FILE)
df.rename(columns={
    'seating_no': SEATING_NO_COL,
    'arabic_name': ARABIC_NAME_COL,
    'total_degree': TOTAL_DEGREE_COL
}, inplace=True)

df[NORMALIZED_NAME_COL] = df[ARABIC_NAME_COL].apply(normalize_arabic)

split_seating_no = 1459762

df1 = df[df[SEATING_NO_COL] < split_seating_no]
df2 = df[df[SEATING_NO_COL] >= split_seating_no]

def create_db(db_file, dataframe):
    conn = sqlite3.connect(db_file)
    db_df = dataframe[[SEATING_NO_COL, ARABIC_NAME_COL, TOTAL_DEGREE_COL, NORMALIZED_NAME_COL]].copy()
    db_df.columns = ['رقم الجلوس', 'الاسم', 'الدرجة', 'normalized_name']
    
    db_df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    
    conn.execute(f'CREATE INDEX idx_normalized_name ON {TABLE_NAME} (normalized_name);')
    conn.execute(f'CREATE INDEX idx_seating_no ON {TABLE_NAME} ("رقم الجلوس");')
    conn.close()

create_db(DB1_FILE, df1)
create_db(DB2_FILE, df2) 