class JiraException(Exception):
    """Base class for Jira exceptions."""

    pass


class BadRequestError(JiraException):
    """Raised when a bad request is made to the Jira API."""

    pass
