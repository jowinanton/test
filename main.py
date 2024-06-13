from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
import mysql.connector

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# Replace with your own database configuration
db_config = {
    'user': 'root',
    'password': 'NISHAN@999@11',
    'host': 'localhost',
    'database': 'project_2'
}

# Simulated token storage
tokens = {
    "my_secure_token_123": "user1",
    "another_secure_token_456": "user2"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
    return None

@app.route('/data', methods=['GET'])
@auth.login_required
def get_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM partner")
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/secure-data', methods=['GET'])
@auth.login_required
def get_secure_data():
    partner_id = auth.current_user()
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        # Example of querying data based on the user
        cursor.execute("SELECT * FROM partner WHERE partner_id = %s", (partner_id,))
        result = cursor.fetchall()
        return jsonify(result), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
