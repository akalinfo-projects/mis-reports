from flask import Blueprint, request, jsonify, redirect
import os
import requests

custom_auth_bp = Blueprint("custom_auth", __name__, url_prefix="/custom-auth")
print("✅ CUSTOM-AUTH: custom_token_auth.py loaded and blueprint created")

@custom_auth_bp.route("/token-login", methods=["GET"])
def token_login():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    introspect_url = os.getenv("https://key.enam20.com/realms/iamservice/protocol/openid-connect/token/introspect")
    client_auth = os.getenv("Basic XXXXXX=")

    try:
        response = requests.post(
            introspect_url,
            data={"token": token},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {client_auth}",
            },
            timeout=5
        )
        data = response.json()
        if not data.get("active"):
            return jsonify({"error": "Token inactive"}), 401

        from flask_login import login_user
        from superset.security import SupersetSecurityManager

        
        username = data["preferred_username"]
        email =  data["email"] 
        user = SupersetSecurityManager().get_user_by_username(data["username"])
        print(username )
        print("username")
        if not user:
            user = security_manager.add_user(
                username=username,
                first_name=data.get("given_name", "Keycloak"),
                last_name=data.get("family_name", "User"),
                email=email,
                role=security_manager.find_role("Gamma")  # Or a custom role
            )
        
        if user:
            #login_user(user)
            login_user(user, remember=False)
            return redirect("/superset/welcome")
        return jsonify({"error": "User not found"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500