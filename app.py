from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_jwt', methods=['GET'])
def get_jwt():
    uid = request.args.get('uid')
    password = request.args.get('password')
    if not uid or not password:
        return jsonify({"error": "Missing uid or password"}), 400

    try:
        guest_url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "uid": uid, "password": password,
            "response_type": "token", "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067"
        }
        resp = requests.post(guest_url, headers=headers, data=data)
        resp.raise_for_status()
        td = resp.json()
        jwt_token = td.get("token")
        if not jwt_token:
            return jsonify({"error": "JWT not found in response"}), 500

        return jsonify({"jwt_token": jwt_token})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
