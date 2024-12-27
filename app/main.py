# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# Run in Terminal
# rm -rf venv
# python3 -m venv venv
# source venv/bin/activate
# pip install requests
# pip install --upgrade pip

from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример токена для авторизации (в реальном проекте он должен быть безопасно сгенерирован)
VALID_TOKEN = "your_secure_token_123"

@app.route('/secure-data', methods=['GET'])
def secure_data():
    # Извлекаем токен из заголовка Authorization
    auth_header = request.headers.get('Authorization')
    # Проверяем
    result =check_header(auth_header)
    # Если токен не валиден, вернем ошибку
    if result[1]!=200:
        return result

    return jsonify({"message": "Access granted", "data": "Here is your secure data"})


@app.route('/post-data', methods=['POST'])
def post_data():
    # Извлекаем токен из заголовка Authorization
    auth_header = request.headers.get('Authorization')
    # Проверяем
    result =check_header(auth_header)
    # Если токен не валиден, вернем ошибку
    if result[1]!=200:
        return result

    data = request.get_json(silent=True)  # Возвращает None, если JSON некорректен
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    PayoutId = data.get("PayoutId", "unknown")
    MerchantReference = data.get("MerchantReference", "unknown")
    IsVerified = True
    Reason=""
    if (PayoutId=="unknown" or MerchantReference=="unknown"):
        IsVerified=False
        Reason ="PayoutId or MerchantReference is unknown "

    return_data = {
          "PayoutId": PayoutId,
          "IsVerified": IsVerified,
          "AccountNumberDecryptionKey": MerchantReference,
          "Reason": Reason
        }

    return jsonify(return_data)



def check_header(auth_header):
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401

        # Проверяем, что токен передан в формате Bearer
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Invalid authorization format"}), 401

        # Извлекаем сам токен
    token = auth_header.split(" ")[1]

    # Проверяем валидность токена
    if token != VALID_TOKEN:
        return jsonify({"error": "Invalid or expired token"}), 403

    return jsonify({"ok": ""}), 200

if __name__ == '__main__':
    app.run(debug=True)