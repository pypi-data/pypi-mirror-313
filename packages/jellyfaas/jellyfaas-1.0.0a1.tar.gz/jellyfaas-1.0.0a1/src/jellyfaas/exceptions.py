class JellyFaasException(Exception):
    """
    Base class for exceptions in the JellyFaas library.
    """
    pass

class AuthenticationFailedException(JellyFaasException):
    """
    Raised when authentication fails.
    """
    pass

class FunctionLookupException(JellyFaasException):
    """
    Raised when there is an issue looking up a function.
    """
    pass

class SetRequestException(JellyFaasException):
    """
    Raised when there is an issue setting request parameters for a function.
    """
    pass

class InvocationException(JellyFaasException):
    """
    Raised when there is an issue invoking the function.
    """
    pass