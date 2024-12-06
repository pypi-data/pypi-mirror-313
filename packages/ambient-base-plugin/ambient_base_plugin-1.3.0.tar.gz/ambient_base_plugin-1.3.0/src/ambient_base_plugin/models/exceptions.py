class UnauthorizedError(BaseException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message)
