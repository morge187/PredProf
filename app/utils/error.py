class UserError(Exception):
    def __init__(self, field, cause):
        self.field = field
        self.cause = cause