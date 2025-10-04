from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CaseQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50), nullable=False)
    case_number = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    court_type = db.Column(db.String(20), nullable=False)  # 'high' or 'district'
    court_name = db.Column(db.String(100), nullable=False)
    query_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'success', 'error'
    response = db.Column(db.Text)  # JSON string of the response

    def __repr__(self):
        return f'<CaseQuery {self.case_type} {self.case_number}/{self.year}>'