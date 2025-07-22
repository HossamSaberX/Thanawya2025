# Thanawya 2025 Results

A simple web application to search for student results by name or seating number.

## Setup

### 1. Install Dependencies
First, install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Prepare the Data
Before running the application, you need to process the `data.xlsx` file to generate the search databases.

Place your `data.xlsx` file in the main project directory. The Excel file should have the following columns in the first row: `seating_no`, `arabic_name`, and `total_degree`.

Then, run the processing script:
```bash
python process_data.py
```
This will create two database files: `data1.db` and `data2.db`.

### 3. Run the Application
Once the databases are created, you can start the Flask application:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.
