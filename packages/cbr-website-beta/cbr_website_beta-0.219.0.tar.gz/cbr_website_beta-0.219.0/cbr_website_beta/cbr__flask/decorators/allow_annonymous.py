def allow_anonymous(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    decorated_function._allow_anonymous = True
    return decorated_function

def allow_users(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    decorated_function._allow_users = True
    return decorated_function

def admin_only(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    decorated_function._admins_only = True
    return decorated_function

