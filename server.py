from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from search_engine import TriangulatorEngine
from groq import Groq
import os
from dotenv import load_dotenv

# Initialize Flask with static folder
app = Flask(__name__, static_folder='frontend/dist', static_url_path='/')
CORS(app)

# Load environment
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Lazy load the engine to ensure port opens quickly
engine = None

def get_engine():
    global engine
    if engine is None:
        print("🚀 Initializing AI Synthesis Engine...")
        engine = TriangulatorEngine(index_path='indexes/rag_index.faiss')
    return engine

# --- API ENDPOINT ---
@app.route('/api/query', methods=['POST'])
def query_rag():
    data = request.json
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
        
    try:
        report = get_engine().triangulate(client, user_query)
        return jsonify({
            "answer": report["final_answer"],
            "confidence": report["confidence"],
            "domain": report["detected_domain"],
            "sources": [
                {"source": r["chunk"]["source"], "text": r["chunk"]["text"], "score": round(r["score"], 4)}
                for r in report["sources"]
            ]
        })
    except Exception as e:
        print(f"Query Error: {e}")
        return jsonify({"error": str(e)}), 500

# --- SERVE REACT FRONTEND ---
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Force host to 0.0.0.0 and get port from environment
    port = int(os.environ.get("PORT", 5000))
    print(f"🌍 Server starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
