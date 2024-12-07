class GPTRouterBadRequestError(Exception):
    """Exception raised for HTTP status code 400: Bad Request within the GPTRouter.

    This status code indicates that the GPTRouter could not understand the request due to invalid syntax."""

    pass


class GPTRouterNotAvailableError(Exception):
    """Exception raised when GPTRouter is unavailable"""

    pass


class GPTRouterUnauthorizedError(Exception):
    """Exception raised for HTTP status code 401: Unauthorized.

    This status code indicates that the client must authenticate itself with the correct GPTRouter API Token."""

    pass


class GPTRouterForbiddenError(Exception):
    """Exception raised for HTTP status code 403: Forbidden.

    This status code indicates that the client does not have privileges to perform an action on GPTRouter."""

    pass


class GPTRouterInternalServerError(Exception):
    """Exception raised for HTTP status code 500: Internal Server Error within the GPTRouter.

    This status code indicates a server error at GPTRouter end, as the name suggests."""

    pass


class GPTRouterTooManyRequestsError(Exception):
    """Exception raised for status code 429: Too Many Requests.

    This status code indicates that the user has sent too many requests in a given amount of time."""

    def __init__(self, message="You are being rate limited"):
        self.message = message
        super().__init__(self.message)


class GPTRouterApiTimeoutError(Exception):
    """Exception raised for API request timeout within the GPTRouter.
    Indicates that the request took too long to complete."""

    pass


class GPTRouterStreamingError(Exception):
    """Exception raised for Errors received during streaming a generation response"""

    pass
