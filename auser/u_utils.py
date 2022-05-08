# check token for register view
def check_token(user, token):
    if (user.token is None) or (token is None):
        return False
    if user.token == token:
        return True
    return False
