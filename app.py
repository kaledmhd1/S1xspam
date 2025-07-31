from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

def encrypt_api(PAYLOAD):
    def xor_encrypt_decrypt(data, key=0x55):
        return bytes([b ^ key for b in data])

    data_bytes = bytes.fromhex(PAYLOAD)
    encrypted_bytes = xor_encrypt_decrypt(data_bytes)
    return encrypted_bytes.hex()

def decrypt_api(hex_string):
    # فك التشفير هو نفس التشفير (XOR)
    return encrypt_api(hex_string)

def guest_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    data = {
        "uid": str(uid),
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    resp = requests.post(url, headers=headers, data=data)
    resp_json = resp.json()
    encrypted_token = resp_json.get("access_token")
    return encrypted_token

@app.route("/get_jwt", methods=["POST"])
def get_jwt():
    data = request.get_json()
    if not data or "uid" not in data or "password" not in data:
        return jsonify({"error": "Missing uid or password"}), 400
    
    uid = data["uid"]
    password = data["password"]
    
    encrypted_token = guest_token(uid, password)
    if not encrypted_token:
        return jsonify({"error": "Failed to get encrypted token"}), 500

    jwt_token = decrypt_api(encrypted_token)

    return jsonify({"BearerAuth": jwt_token, "success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
