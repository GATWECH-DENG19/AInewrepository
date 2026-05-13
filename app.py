from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog
import os

app = Flask(__name__)
CORS(app)
prolog = Prolog()

# ==========================================================
# MULTI-FOLDER PATH LOGIC
# ==========================================================
# 1. Get the absolute path of the folder where app.py is (e.g., .../backend/)
base_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go UP one level, then DOWN into the 'prolog' folder to find 'prolog.pl'
# The ".." means "go up one folder"
prolog_path = os.path.abspath(os.path.join(base_dir, "..", "prolog", "prolog.pl"))

# 3. IMPORTANT: Fix Windows backslashes for SWI-Prolog
prolog_path = prolog_path.replace("\\", "/")

if not os.path.exists(prolog_path):
    print(f"❌ ERROR: Could not find prolog.pl at: {prolog_path}")
    print("Ensure your folder structure is: Project/prolog/prolog.pl and Project/backend/app.py")
else:
    try:
        prolog.consult(prolog_path)
        print(f"✅ Prolog successfully loaded from separate folder: {prolog_path}")
    except Exception as e:
        print(f"❌ Prolog Consult Error: {e}")

# ==========================================================
# API ROUTES
# ==========================================================

@app.route('/route', methods=['POST'])
def get_route():
    data = request.get_json()
    start = str(data.get("start", "")).lower().strip().replace(" ", "_")
    goal = str(data.get("goal", "")).lower().strip().replace(" ", "_")

    if not start or not goal:
        return jsonify({"error": "Missing start or goal location"}), 400

    try:
        query = f"astar('{start}', '{goal}', Path, Cost)"
        result = list(prolog.query(query))

        if result:
            return jsonify({
                "path": [str(node) for node in result[0]["Path"]],
                "cost": round(float(result[0]["Cost"]), 5),
                "status": "success"
            })
        return jsonify({"error": f"No path found between {start} and {goal}."}), 404

    except Exception as e:
        print(f"❌ Backend Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
