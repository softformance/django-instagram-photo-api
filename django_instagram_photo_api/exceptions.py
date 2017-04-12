class JsonException(Exception):
    def __init__(self, message=None, *args):
        self.message = message
        super(JsonException, self).__init__(message, *args)