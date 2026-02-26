from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add current directory to path to find other modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_pipeline import ingest_url, answer_query

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/ingest', methods=['POST'])
def ingest():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400
        
    try:
        num_chunks = ingest_url(url)
        return jsonify({"message": f"Successfully ingested {num_chunks} chunks."})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Check for exit command
    if query.strip().lower() in ["exit", "quit", "bye", "stop"]:
        return jsonify({
            "answer": "Chatbot session ended. You can refresh the page to start a new session.",
            "exit": True
        })
        
    try:
        answer = answer_query(query)
        return jsonify({"answer": answer, "exit": False})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting backend server at http://localhost:5000")
    print("Ensure Ollama is running with your selected model.")
    app.run(host='0.0.0.0', port=5000, debug=True)
