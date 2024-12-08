def get_token_from_request(request):
    token = request.headers["authorization"].removeprefix("Bearer ")
    return token