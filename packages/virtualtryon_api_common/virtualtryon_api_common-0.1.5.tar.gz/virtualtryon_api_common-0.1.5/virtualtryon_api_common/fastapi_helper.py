def get_auth_header(request):
    token = request.headers["authorization"].removeprefix("Bearer ")
    return token