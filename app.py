from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_caching import Cache
import hashlib
from utils import normalize_arabic
import os

app = Flask(__name__)

# Configure Redis caching
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': redis_url
})

DB_PATH = 'data.db'

def query_db(query, args=(), one=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.OperationalError:
        return None if one else []

def make_cache_key():
    query = request.args.get('query')
    page = request.args.get('page', 1)
    key_str = f"query={query}&page={page}"
    return hashlib.md5(key_str.encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def search():
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = 10

    if not query:
        return jsonify({"error": "No query provided"}), 400

    offset = (page - 1) * per_page
    
    base_select = "SELECT * FROM students"
    count_select = "SELECT COUNT(*) FROM students"
    conditions = []
    args = []

    if query.isdigit():
        conditions.append("CAST([رقم الجلوس] AS TEXT) LIKE ?")
        args.append(f"%{query}%")
    else:
        normalized_query = normalize_arabic(query)
        search_words = normalized_query.split()
        conditions.extend(["normalized_name LIKE ?" for _ in search_words])
        args.extend([f"%{word}%" for word in search_words])
    
    where_clause = " WHERE " + " AND ".join(conditions)
    
    count_query = count_select + where_clause
    total_results_row = query_db(count_query, args, one=True)
    total_results = total_results_row[0] if total_results_row else 0

    results_query = f"{base_select}{where_clause} ORDER BY الدرجة DESC LIMIT ? OFFSET ?"
    paginated_results = query_db(results_query, args + [per_page, offset])

    # Format results
    results_list = []
    for row in paginated_results:
        row_dict = dict(row)
        total_degree = row_dict.get('الدرجة', 0)
        is_pass = total_degree >= 160
        results_list.append({
            'رقم الجلوس': row_dict.get('رقم الجلوس', 'N/A'),
            'الاسم': row_dict.get('الاسم', 'N/A'),
            'الدرجة': total_degree,
            'student_case_desc': 'ناجح' if is_pass else 'راسب'
        })
        
    return jsonify({
        "results": results_list,
        "total_results": total_results
    })

if __name__ == '__main__':
    app.run(debug=False)
