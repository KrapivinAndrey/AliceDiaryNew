class Error(Exception):
    pass


class NotFoundError(Error):
    pass


class NeedAuth(Error):
    pass
