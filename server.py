from flask import Flask, request, jsonify
from flask_cors import CORS
from search_engine import TriangulatorEngine
from groq import Groq
import os
from dotenv import load_dotenv

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load environment and RAG engine
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
engine = TriangulatorEngine(index_path='indexes/rag_index.faiss')

@app.route('/api/query', methods=['POST'])
def query_rag():
    data = request.json
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
        
    try:
        # Run the Synthesis Engine (Innovation Component)
        report = engine.triangulate(client, user_query)
        
        # Format response for the frontend
        return jsonify({
            "answer": report["final_answer"],
            "confidence": {
                "level": report["confidence"]["level"],
                "reason": report["confidence"]["reason"]
            },
            "domain": report["detected_domain"],
            "sources": [
                {
                    "source": r["chunk"]["source"],
                    "text": r["chunk"]["text"],
                    "score": round(r["score"], 4)
                }
                for r in report["sources"]
            ]
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
