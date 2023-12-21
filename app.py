from flask import Flask, jsonify, request
from wrappers import token_required

app = Flask(__name__)


@app.route("/")
@token_required
def index():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Success fetching the API"
        },
        "data": None,
    }), 200


if __name__ == "__main__":
    app.run()
