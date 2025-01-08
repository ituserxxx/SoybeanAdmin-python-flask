from flask import  request, jsonify

# 自定义校验 Authorization 头的函数
from main import app

def check_authorization():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        # 如果没有 Authorization 头，返回 401 未授权错误
        return jsonify({"message": "Authorization header is missing"}), 401

    # 检查 Authorization 头的格式是否为 "Bearer <token>"
    if not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization format is invalid"}), 401

    # 获取 token
    token = auth_header[len('Bearer '):]

    # 这里可以进一步检查 token 是否有效，比如解码 JWT 或其他操作
    if token != 'valid_token':  # 假设 'valid_token' 是有效的 token
        return jsonify({"message": "Invalid token"}), 401
    # 如果验证通过，返回 None，表示不需要额外处理
    return None


# 在每个请求之前校验 Authorization 参数
@app.before_request
def before_request():
    # 排除 /login 和 /public 路由的请求，不进行校验
    if request.endpoint in ['login', 'public']:
        return None  # 不进行校验，继续处理请求
    # 否则进行 Authorization 校验
    response = check_authorization()
    if response:
        return response  # 如果验证失败，直接返回错误响应