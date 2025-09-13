from flask_appbuilder import BaseView, expose
from flask_appbuilder.api import safe
from flask import request, jsonify

class CustomTokenLogin(BaseView):
    route_base = "/custom-auth"

    @expose("/token-login", methods=["POST"])
    @safe
    def token_login(self):
        token = request.args.get("token")
        if not token:
            return jsonify({"error": "Missing token"}), 400
        return jsonify({"message": "Token accepted", "token": token})
