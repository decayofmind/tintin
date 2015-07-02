class GenericError(Exception):
    def __init__(self, internal_message):
        super(GenericError, self).__init__(internal_message)
        self.internal_message = internal_message

    def __str__(self):
        return self.internal_message

    __unicode__ = __str__


class ApiError(GenericError):
    def __init__(self, message, code):
        super(ApiError, self).__init__(message)
        self.code = code

    def __str__(self):
        return '{0} ({1})'.format(self.message, self.code)

    __unicode__ = __str__
