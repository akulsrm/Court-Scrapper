from flask import Flask, render_template, request, jsonify, send_file
from models import db, CaseQuery
from scraper import fetch_case_details, download_judgment, fetch_cause_list
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///court_cases.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'downloads'

# Ensure download directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_case():
    data = request.json
    case_type = data.get('case_type')
    case_number = data.get('case_number')
    year = data.get('year')
    court_type = data.get('court_type')
    court_name = data.get('court_name')
    
    if not all([case_type, case_number, year, court_type, court_name]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Record the query in database
        query = CaseQuery(
            case_type=case_type,
            case_number=case_number,
            year=year,
            court_type=court_type,
            court_name=court_name,
            query_date=datetime.now()
        )
        
        # Fetch case details
        result = fetch_case_details(court_type, court_name, case_type, case_number, year)
        
        if 'error' in result:
            query.status = 'error'
            query.response = json.dumps({'error': result['error']})
            db.session.add(query)
            db.session.commit()
            return jsonify(result), 404
        
        # Save successful response
        query.status = 'success'
        query.response = json.dumps(result)
        db.session.add(query)
        db.session.commit()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_document():
    data = request.json
    case_id = data.get('case_id')
    document_type = data.get('document_type')
    
    if not all([case_id, document_type]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        file_path = download_judgment(case_id, document_type)
        if 'error' in file_path:
            return jsonify(file_path), 404
        
        return jsonify({'file_path': file_path})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/causelist', methods=['POST'])
def get_cause_list():
    data = request.json
    court_type = data.get('court_type')
    court_name = data.get('court_name')
    date = data.get('date')
    
    if not all([court_type, court_name, date]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        result = fetch_cause_list(court_type, court_name, date)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)