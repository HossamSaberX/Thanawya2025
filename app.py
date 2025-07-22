from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_caching import Cache
import hashlib
from utils import normalize_arabic

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db1_path = 'data1.db'
db2_path = 'data2.db'

def query_db(db_path, query, args=(), one=False):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.OperationalError:
        return []

def make_cache_key():
    query = request.args.get('query')
    page = request.args.get('page', 1)
    key = f'{query}_{page}'
    return hashlib.md5(key.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
@cache.cached(timeout=60, key_prefix=make_cache_key)
def search():
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = 10

    if not query:
        return jsonify({"error": "No query provided"}), 400

    results1 = []
    results2 = []

    if query.isdigit():
        results1 = query_db(db1_path, "SELECT * FROM students WHERE CAST([رقم الجلوس] AS TEXT) LIKE ?", [f"%{query}%"])
        results2 = query_db(db2_path, "SELECT * FROM students WHERE CAST([رقم الجلوس] AS TEXT) LIKE ?", [f"%{query}%"])
    else:
        normalized_query = normalize_arabic(query)
        search_words = normalized_query.split()
        
        # Build the query to match all search words
        conditions = " AND ".join(["normalized_name LIKE ?" for _ in search_words])
        sql_query = f"SELECT * FROM students WHERE {conditions}"
        
        # Create the arguments list with wildcards
        args = [f"%{word}%" for word in search_words]
        
        results1 = query_db(db1_path, sql_query, args)
        results2 = query_db(db2_path, sql_query, args)

    combined_results = results1 + results2

    def to_dict(row):
        row_dict = dict(row)
        total_degree = row_dict.get('الدرجة', 0)
        
        is_pass = total_degree >= 160
        
        return {
            'رقم الجلوس': row_dict.get('رقم الجلوس', 'N/A'),
            'الاسم': row_dict.get('الاسم', 'N/A'),
            'الدرجة': total_degree,
            'student_case_desc': 'ناجح' if is_pass else 'راسب'
        }
        
    combined_results = [to_dict(row) for row in combined_results]
    
    combined_results.sort(key=lambda x: x['الدرجة'], reverse=True)

    total_results = len(combined_results)
    paginated_results = combined_results[(page - 1) * per_page : page * per_page]

    return jsonify({
        "results": paginated_results,
        "total_results": total_results
    })

if __name__ == '__main__':
    app.run(debug=False)
