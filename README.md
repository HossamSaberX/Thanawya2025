# 2023/2024 Thanawya

This web application allows users to search for student results by name or student ID. The application is deployed on Vercel and demonstrates several key skills and technologies.

## Key Features and Skills Demonstrated

- **Data Conversion**: Convert large XLSX files to SQLite databases for efficient querying.
- **Database Optimization**: Index common columns in the SQLite database to improve search performance.
- **Web Development**: Create a dynamic and responsive web interface using HTML, CSS, and JavaScript.
- **Server-Side Development**: Develop a Flask-based backend to handle search queries and return paginated results.
- **Caching**: Implement caching with Flask-Caching to enhance performance.
- **Deployment**: Deploy the application on Vercel for easy access and demonstration.

## Live Demo

Check out the live demo: [Nateega2024](https://nateega-five.vercel.app/)

## Instructions

### 1. Setting Up the Environment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HossamSaberX/Thanawya2024
   cd Thanawya2024
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Convert the XLSX File into SQLite

If you want to convert the XLSX file to SQLite and split the database:

1. **Create the Conversion Script** (`tosqlite.py`):

   ```python
   import pandas as pd
   import sqlite3

   df = pd.read_excel('data.xlsx')
 
   split_id = 500000
   df1 = df[df['رقم الجلوس'] <= split_id]
   df2 = df[df['رقم الجلوس'] > split_id]

   def save_to_sqlite(df, db_path):
       conn = sqlite3.connect(db_path)
       df.to_sql('students', conn, if_exists='replace', index=False)
       
       # Create indexes on common columns
       cur = conn.cursor()
       cur.execute('CREATE INDEX idx_رقم_الجلوس ON students (رقم الجلوس);')
       cur.execute('CREATE INDEX idx_الاسم ON students (الاسم);')
       conn.commit()
       conn.close()


   save_to_sqlite(df1, 'data1.db')
   save_to_sqlite(df2, 'data2.db')

   print("XLSX data successfully split and converted to SQLite databases with indexes.")
   ```

2. **Run the Conversion Script**:
   ```bash
   python tosqlite.py
   ```

### 3. Running the Application

1. **Start the Flask Server**:
   ```bash
   flask run
   ```

2. **Access the Application**: Open your browser and navigate to `http://localhost:5000`.

## Additional Information

- The application uses two separate SQLite databases to handle the large volume of student data efficiently, and also cause of the limits on free hosting.
- The search functionality supports both student names and ID numbers.
- Results are paginated for better performance and user experience.
