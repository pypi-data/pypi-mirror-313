class TimeoutException(Exception):
    pass

class RetriableException(Exception):
    pass

class NotRetriableException(Exception):
    pass

class SirioBoServiceTimeoutException(TimeoutException):
    pass

class SirioBoServiceRetriableException(RetriableException):
    pass

class SirioBoServiceNotRetriableException(NotRetriableException):
    pass
