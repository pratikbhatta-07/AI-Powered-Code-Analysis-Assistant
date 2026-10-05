from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add backend root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.orchestrator import full_review
from src.tools.explanation_tool import explain_code
from src.tools.test_tool import generate_tests
from src.tools.find_bug_tool import find_bug
from src.tools.complexity_tool import analyze_complexity
from src.utils.github_loader import get_code_from_github_file
from src.db.init_db import init_db

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize database on startup
init_db()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Backend is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    try:
        data = request.get_json()
        
        code = data.get('code', '').strip()
        language = data.get('language', 'python').strip()
        mode = data.get('mode', '2').strip()
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Mode 5 = Full Review (different structure)
        if mode == '5':
            result = full_review(code, language)
            return jsonify({
                'result': result,
                'mode': mode,
                'language': language
            })
        
        # Other modes
        if mode == '4':
            result = find_bug(code, language, mode)
        elif mode == '3':
            result = generate_tests(code, language, mode)
        else:  # modes 1, 2
            result = explain_code(code, language, mode)
        
        # Extract complexity if available
        complexity = analyze_complexity(code)
        
        return jsonify({
            'result': result,
            'complexity': {
                'time': complexity,
                'space': None  # Can be enhanced later
            },
            'mode': mode,
            'language': language
        })
        
    except Exception as e:
        print(f"Error in analyze endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/github', methods=['POST'])
def fetch_github():
    """Fetch code from GitHub URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        code = get_code_from_github_file(url)
        
        return jsonify({
            'code': code,
            'success': True
        })
        
    except Exception as e:
        print(f"Error in github endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting Code Analysis Backend...")
    print("📍 Backend running on http://localhost:5001")
    print("🔗 API available at http://localhost:5001/api")
    app.run(debug=True, host='0.0.0.0', port=5001)
