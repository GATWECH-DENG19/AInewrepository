from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pyswip import Prolog
import os

# Initialize Flask with folder paths for Render/Docker
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app) # This allows your Netlify frontend to talk to this backend
prolog = Prolog()

# ==========================================================
# FILE PATH LOGIC (Docker Friendly)
# ==========================================================
base_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Name of your prolog file - CHANGE THIS if your file is named differently!
prolog_filename = "prolog.pl" 

# 2. Look for the file in the main folder or a subfolder named 'prolog'
prolog_path = os.path.join(base_dir, prolog_filename)
if not os.path.exists(prolog_path):
    prolog_path = os.path.join(base_dir, "prolog", prolog_filename)

# 3. Format path for SWI-Prolog
prolog_path = prolog_path.replace("\\", "/")

# 4. Load Prolog
if not os.path.exists(prolog_path):
    print(f"❌ ERROR: Could not find {prolog_filename} at {prolog_path}")
else:
    try:
        prolog.consult(prolog_path)
        print(f"✅ Prolog successfully loaded: {prolog_path}")
    except Exception as e:
        print(f"❌ Prolog Consult Error: {e}")

# ==========================================================
# ROUTES
# ==========================================================

# Home route to prevent "Not Found" error
@app.route('/')
def home():
    return jsonify({
        "message": "AI Map Finder Backend is Online",
        "prolog_file_found": os.path.exists(prolog_path),
        "path_searched": prolog_path
    })

# The actual pathfinding route
@app.route('/route', methods=['POST'])
def get_route():
    data = request.get_json()
    
    # Safely get start and goal from the request
    start = str(data.get("start", "")).lower().strip().replace(" ", "_")
    goal = str(data.get("goal", "")).lower().strip().replace(" ", "_")

    if not start or not goal:
        return jsonify({"error": "Missing start or goal location"}), 400

    try:
        # This matches your Prolog predicate: astar(start, goal, Path, Cost)
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

# ==========================================================
# START THE SERVER
# ==========================================================
if __name__ == "__main__":
    # Use the port Render assigns, default to 10000 for Docker
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
