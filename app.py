import secrets
from flask import Flask, render_template, redirect, session, request, jsonify
import google.generativeai as genai
from db import mongo
from health_report import analyze_health_report
from med import get_medicine_info
import google.generativeai as genai
from aisuggestion import get_ai_health_suggestion, ai_suggestion_bp



from PIL import Image
import PIL
import io

from med import medicine_bp

from login import handle_login
from signup import handle_signup
from contact import send_message

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.register_blueprint(medicine_bp)
app.register_blueprint(ai_suggestion_bp)


import secrets
app.secret_key = secrets.token_hex(16)
# Routes


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')


@app.route('/health-report') 
def health_report():
    return render_template('health_report.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    return analyze_health_report()


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return send_message()
    return render_template('contact.html')


@app.route('/medicine-info', methods=['GET', 'POST'])
def medicine_info():
    return get_medicine_info()


@app.route('/ai-suggestion', methods=['GET', 'POST'])
def ai_suggestion():
    return get_ai_health_suggestion()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return handle_signup()

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = mongo.db.users.find_one({'username': session['username']})
        reports_count = mongo.db.reports.count_documents({'user_id': user['_id']})
        medicines_searched = mongo.db.search_history.count_documents({'user_id': user['_id']})

        return render_template('dashboard_structure.html', reports_count=reports_count, medicines_searched=medicines_searched)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)

if __name__ == '__main__':
    app.run(debug=True)
