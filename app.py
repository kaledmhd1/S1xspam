from flask import Flask, request, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# دالة ترسل طلب فتح بروفايل اللاعب
def visit_profile(jwt_token, target_uid):
    url = "https://clientbp.common.ggbluefox.com/GetUserInfoData"

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android 9)',
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': 'OB50',
    }

    # إرسال uid الهدف في الحقل المطلوب
    data = {
        "target_uid": target_uid
    }

    try:
        response = requests.post(url, headers=headers, data=data, verify=False)
        return response.status_code == 200
    except:
        return False

@app.route('/view', methods=['POST'])
def view():
    try:
        data = request.get_json()
        jwt_token = data.get("jwt_token")
        target_uid = data.get("target_uid")

        if not jwt_token or not target_uid:
            return jsonify({"error": "Missing jwt_token or target_uid"}), 400

        success = visit_profile(jwt_token, target_uid)

        if success:
            return jsonify({"status": "success", "message": "Profile viewed."})
        else:
            return jsonify({"status": "failed", "message": "Failed to view profile."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "FF View API running. Use POST /view"

if __name__ == '__main__':
    app.run()
