from flask import Flask, request, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def visit_profile(jwt_token, target_uid):
    url = "https://clientbp.common.ggbluefox.com/GetUserInfoData"

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android 9)',
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB50',
    }

    data = {
        "target_uid": target_uid
    }

    try:
        response = requests.post(url, headers=headers, data=data, verify=False)
        print("Response code:", response.status_code)
        print("Response body:", response.text)
        return response.status_code == 200
    except Exception as e:
        print("Error:", str(e))
        return False

@app.route('/view', methods=['GET'])
def view():
    jwt_token = request.args.get("jwt_token")
    target_uid = request.args.get("target_uid")

    if not jwt_token or not target_uid:
        return jsonify({"error": "Missing jwt_token or target_uid"}), 400

    success = visit_profile(jwt_token, target_uid)

    if success:
        return jsonify({"status": "success", "message": "Profile viewed."})
    else:
        return jsonify({"status": "failed", "message": "Failed to view profile."}), 500

@app.route('/')
def home():
    return "✅ FF View API is running. Use /view?jwt_token=...&target_uid=..."

if __nam
