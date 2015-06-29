from tintin.api.wubook import WuBookApi, WuBookApiError


class WuBookClient(WuBookApi):
    def __init__(self, username, password, lcode):
        super(WuBookClient, self).__init__()
        self.username = username
        self.password = password
        self.lcode = lcode

        self.token = self.get_token(username, password)

        self._handle_auth(self)

    def _handle_auth(self, cls):
        for attr, val in cls.__dict__.iteritems():
            if callable(val) and not (attr.startswith("_") or attr.endswith("_token")):
                setattr(cls, attr, self._keep_token(val))

    def _keep_token(self, method):
        def _wrapped(*args, **kwargs):
            try:
                # Commented, because it's hard to parse now
                # return BaseCollection(*[BaseDTO(ob) for ob in method(self.token, self.lcode, *args, **kwargs)])
                return method(self.token, self.lcode, *args, **kwargs)
            except WuBookApiError as e:
                if e.code == -1:
                    self.token = self.get_token(self.username, self.password)
                    return method(self.token, self.lcode, *args, **kwargs)
                raise
        return _wrapped
