from flask import Flask, request, jsonify, render_template
from query_processor import process_query
import time
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    if request.method == "POST":
        user_input = request.form.get("question", "")
        query_id = str(uuid.uuid4())[:8]
        print(f"[{query_id}] Form Processing query at {time.strftime('%H:%M:%S')}: {user_input}")
        answer = process_query(user_input)
    return render_template("index.html", question=request.form.get("question", None), answer=answer)

@app.route("/search", methods=["GET", "POST"])
def chatbot_api():
    if request.method == "GET":
        return jsonify({
            "message": "Chatbot API is ready",
            "usage": "Send POST requests with JSON body containing 'message' field",
            "example": {"message": "How many total students?"}
        })

    user_input = ""
    if request.is_json:
        user_input = request.json.get("message", "")
    else:
        user_input = request.form.get("message", "") or request.form.get("question", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    query_id = str(uuid.uuid4())[:8]
    print(f"[{query_id}] API Processing query at {time.strftime('%H:%M:%S')}: {user_input}")
    response = process_query(user_input)
    response_with_id = f"{response} [ID: {query_id}]"

    return jsonify({
        "answer": response_with_id,
        "query_id": query_id,
        "timestamp": time.time()
    })

@app.route("/test", methods=["GET"])
def test():
    try:
        from query_processor import DBConnection
        with DBConnection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as count FROM student_data")
                result = cursor.fetchone()
                return jsonify({
                    "status": "OK",
                    "database_connected": True,
                    "student_count": result[0],
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                })
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "database_connected": False,
            "error": str(e),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
