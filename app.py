import uuid
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- ダミーデータ ---
# OpenAPIスキーマ構造に一致する一貫したダミーデータ
DUMMY_USER = {
    "userId": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", # 簡略化のため固定UUID
    "username": "dummyuser",
    "email": "dummy@example.com",
    "createdAt": datetime.now(timezone.utc).isoformat(), # ISO形式を使用
    "lastLogin": datetime.now(timezone.utc).isoformat(),
    "isActive": True,
    "profile": {
        "fullName": "Dummy User",
        "bio": "これはダミーの自己紹介です。",
        "avatarUrl": "http://example.com/avatar.jpg"
    },
    "tags": ["dummy", "test"],
    "preferences": {
        "theme": "dark",
        "notifications": {
            "email": True,
            "sms": False
        }
    }
}

# --- APIエンドポイント ---

@app.route('/users/<uuid:userId>', methods=['GET'])
def get_user_profile(userId):
    """userIdに基づいてユーザープロファイルを取得します（ダミーデータを返します）。"""
    # 入力のuserIdは無視し、常に同じダミーユーザーを返します
    print(f"GET /users/{userId} が呼び出されました")
    # 返されるデータ構造がスキーマと一致することを確認します
    response_data = DUMMY_USER.copy()
    response_data["userId"] = str(userId) # 必要に応じて要求されたuserIdを反映するか、固定のままにします
    response_data["createdAt"] = datetime.now(timezone.utc).isoformat() # タイムスタンプを更新
    response_data["lastLogin"] = datetime.now(timezone.utc).isoformat()
    return jsonify(response_data), 200

@app.route('/users/<uuid:userId>', methods=['PATCH'])
def update_user_profile(userId):
    """userIdに基づいてユーザープロファイルを更新します（シミュレーション）。"""
    print(f"PATCH /users/{userId} が呼び出されました")
    if not request.is_json:
        return jsonify({"code": "INVALID_REQUEST", "message": "リクエストはJSONである必要があります"}), 400

    data = request.get_json()

    # 更新をシミュレート：ダミーデータの変更バージョンを返します
    # 実際には何も保存しません
    updated_data = DUMMY_USER.copy()
    updated_data["userId"] = str(userId) # 要求されたuserIdを反映

    # リクエストボディからの変更を適用する非常に基本的なシミュレーション
    if 'profile' in data and isinstance(data['profile'], dict):
        updated_data['profile'].update(data['profile'])
    if 'tags' in data and isinstance(data['tags'], list):
        updated_data['tags'] = data['tags']
    if 'isActive' in data and isinstance(data['isActive'], bool):
        updated_data['isActive'] = data['isActive']
    if 'preferences' in data and isinstance(data['preferences'], dict):
        # 単純なマージ（ディープマージではない）
        updated_data['preferences'].update(data['preferences'])

    updated_data["lastLogin"] = datetime.now(timezone.utc).isoformat() # タイムスタンプを更新

    # 注意：createdAtのような読み取り専用フィールドはリクエストからは更新されません

    return jsonify(updated_data), 200

# --- エラーハンドラ（オプションですが、良い習慣です） ---
@app.errorhandler(404)
def not_found(error):
    # ルートが一致しない場合（例：/）を処理します
    return jsonify({"code": "NOT_FOUND", "message": "リソースが見つかりません"}), 404

@app.errorhandler(400)
def bad_request(error):
    # 他の潜在的な不正リクエスト（UUIDでないuserIdなど）をキャッチします
    return jsonify({"code": "BAD_REQUEST", "message": str(error)}), 400

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"code": "METHOD_NOT_ALLOWED", "message": "このリソースではメソッドは許可されていません"}), 405


if __name__ == '__main__':
    # Pythonで直接実行し、自動リロードのためにデバッグを有効にします
    app.run(host='0.0.0.0', port=8000, debug=True)
