from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_caching import Cache
import hashlib

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
## 
db1_path = 'data1.db'
db2_path = 'data2.db'
 ### These two lines are sequential steps after you divide the xlsx into two dbs (For hosting wise) ###
##
split_id = 500000

def query_db(db_path, query, args=(), one=False):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def make_cache_key(*args, **kwargs):
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
        id = int(query)
        results1 = query_db(db1_path, "SELECT * FROM students WHERE CAST([رقم الجلوس] AS TEXT) LIKE ?", [f"%{query}%"])
        results2 = query_db(db2_path, "SELECT * FROM students WHERE CAST([رقم الجلوس] AS TEXT) LIKE ?", [f"%{query}%"])
    else: 
        results1 = query_db(db1_path, "SELECT * FROM students WHERE [الاسم] LIKE ?", [f"%{query}%"])
        results2 = query_db(db2_path, "SELECT * FROM students WHERE [الاسم] LIKE ?", [f"%{query}%"])

    combined_results = results1 + results2

    combined_results = [dict(row) for row in combined_results]

    combined_results.sort(key=lambda x: x['الدرجة'], reverse=True)

    total_results = len(combined_results)
    paginated_results = combined_results[(page - 1) * per_page : page * per_page]

    return jsonify({
        "results": paginated_results,
        "total_results": total_results
    })

if __name__ == '__main__':
    app.run(debug=False)