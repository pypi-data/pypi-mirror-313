import functools

# todo: move to AuthService!


def common_auth(func):
    """
    Декоратор используется в классах IssueService для проверки общих прав доступа
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        user_info = self.auth_service.verify_access_token(self.token, self.required_scopes)
        self.auth_user_info = user_info
        return func(self, *args, **kwargs)
    return wrapper