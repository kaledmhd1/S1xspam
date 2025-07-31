from flask import Flask, request, jsonify
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def visit_profile(jwt_token, target_uid):
    url = f"https://info-ch9ayfa.vercel.app/{target_uid}"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android 9)',
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

@app.route('/view', methods=['GET'])
def api_view():
    jwt_token = request.args.get('jwt_token')
    uid = request.args.get('uid')

    if not jwt_token or not uid:
        return jsonify({"status": "failed", "message": "Missing jwt_token or uid parameter"}), 400

    success, result = visit_profile(jwt_token, uid)
    if success:
        return jsonify({"status": "success", "data": result})
    else:
        return jsonify({"status": "failed", "message": result}), 500

@app.route('/')
def home():
    return "Profile Viewer API. Use /view?jwt_token=YOUR_JWT&uid=TARGET_UID"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
