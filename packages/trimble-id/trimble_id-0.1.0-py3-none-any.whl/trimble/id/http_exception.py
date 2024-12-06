class HttpException(Exception):
    def __init__(self, status, message):
        self.status = status
        super().__init__(message)

    def __str__(self):
        return 'Returned: ' + str(self.status) + ' ' + super().__str__()