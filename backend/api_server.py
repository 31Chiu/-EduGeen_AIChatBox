from flask import Flask, request, jsonify
from flask_cors import CORS
from Gemini import EcoAISystem
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 解决跨域问题
ai_system = EcoAISystem()

@app.route('/api/chat', methods=['POST'])
def chat_handler():
    try:
        user_input = request.json.get('message', '')
        response = ai_system.process_query(user_input)
        
        return jsonify({
            "text": response,
            "meta": {
                # "trees": ai_system.persona.trees,
                "carbon_offset": ai_system.persona._calculate_carbon_footprint(response)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)