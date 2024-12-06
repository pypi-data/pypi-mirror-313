"""JiraPoster class for interacting with the Jira API."""

import hashlib
import json
import linecache
import os
import re
import sys
import traceback
import zlib
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from types import TracebackType
from typing import List, Optional, Union

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ChunkedEncodingError
from retry import retry

from .config import CONFIG
from .exceptions import BadRequestError
from .utils import logger
from .utils.common import Encoder, get_frames, remove_holotree_id, retrieve_build_info
from .workitems import variables


def retry_if_bad_request(func):
    """Retries a function if it raises a BadRequestError."""
    attempt = 1
    tries = 3

    @retry(exceptions=(BadRequestError, ChunkedEncodingError), tries=tries, delay=1, backoff=2)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (BadRequestError, ChunkedEncodingError) as ex:
            nonlocal attempt
            attempt = attempt + 1 if attempt < tries else 1
            raise ex

    return wrapper


class Jira:
    """Jira class for interacting with the Jira API."""

    def __init__(self):
        """Initializes the Jira class."""
        self._base_url = "https://thoughtfulautomation.atlassian.net/"
        self._assignee_cache = {}
        self._transition_types = {}
        self._issue_types = {}
        self._project_key = None
        self._webhook_url = None
        self._auth = None
        self._default_assignee = None
        self._build_info: Optional[dict] = None

    @staticmethod
    def _is_json_response(response) -> bool:
        try:
            response.json()
            return True
        except json.decoder.JSONDecodeError:
            return False

    def check_response(self, response, mandatory_json: bool = False, exc_message: str = "") -> None:
        """Check if response is not 200 or not json.

        Args:
            response (requests.Response): The response object
            mandatory_json (bool, optional): If the response is not json. Defaults to False.
            exc_message (str, optional): The exception message. Defaults to "".

        Raises:
            BadRequestError: If the response is not 200 or not json

        Returns:
            None
        """
        # Check if response is not 200 or not json
        if response.status_code not in [200, 201, 204] or (mandatory_json and not self._is_json_response(response)):
            exc_message = exc_message + "\n" if exc_message else ""
            if self._is_json_response(response):
                raise BadRequestError(
                    f"{exc_message}Status Code: {response.status_code}, "
                    f"Json content: {response.json()}, Headers: {response.headers}"
                )
            else:
                raise BadRequestError(
                    f"{exc_message}Status Code: {response.status_code}, " f"Headers: {response.headers}"
                )

    def config(
        self,
        login: str,
        api_token: str,
        project_key: str,
        webhook_url: Optional[str] = None,
        default_assignee: Optional[str] = None,
    ) -> bool:
        """Sets the webhook URL for the Jira project.

        Args:
            login (str): The username for the Jira account.
            api_token (str): The API token for the Jira account.
            project_key (str): The key of the Jira project.
            webhook_url (str): The webhook URL for the Jira project.
            default_assignee (str, optional): The default assignee for the Jira project. Defaults to None.

        Returns:
            bool: True if the configuration was successful, False otherwise.
        """
        try:
            self._project_key = project_key if CONFIG.STAGE not in ["hypercare", "support"] else CONFIG.SUPPORT_BOARD
            self._default_assignee = default_assignee
            self._build_info = retrieve_build_info()
            if not webhook_url:
                logger.warning("No JIRA webhook URL provided. All issues will be posted to backlog.")
            self._webhook_url = webhook_url
            self._auth = self._authenticate(login, api_token)
            try:
                self.get_current_user()
            except BadRequestError:
                logger.warning("Failed to authenticate to Jira or incorrect project key.")
                return False
            self._issue_types = self.__get_issue_types()
            return True
        except Exception as ex:
            logger.warning(f"Failed to configure Jira: {ex}")
            return False

    def _authenticate(self, login, api_token) -> HTTPBasicAuth:
        """Function to authenticate the user with the provided username and API token.

        Returns:
            HTTPBasicAuth: The authentication object for the Jira API.
        """
        return HTTPBasicAuth(login, api_token)

    def __get_headers(self) -> dict:
        """A function to get the headers for a Jira API request.

        Returns:
            dict: The headers for the Jira API request.
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @retry_if_bad_request
    def get_issues(self, project_key: Optional[str] = None) -> dict:
        """A function to get the issues using a Jira API.

        It updates the headers, sets up a JQL query, specifies additional query parameters,
        makes a GET request to the Jira API, and returns the JSON response.
        """
        project_key = project_key or self._project_key
        jql_query = f'project = "{project_key}"'

        # Specify additional query parameters if needed
        query_params = {"jql": jql_query, "maxResults": 100}  # Adjust as needed

        response = requests.request(
            "GET",
            self._base_url + "/rest/api/2/search",
            headers=self.__get_headers(),
            auth=self._auth,
            params=query_params,
        )
        self.check_response(response)
        return response.json()

    @retry_if_bad_request
    def get_issue(self, issue_id: str):
        """A function to get the issue using a Jira API.

        Args:
            issue_id (str): The ID of the issue.

        Returns:
            dict: The JSON response from the Jira API.
        """
        response = requests.request(
            "GET",
            url=self._base_url + f"/rest/api/3/issue/{issue_id}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()

    def get_current_user(self) -> dict:
        """Get the current user.

        Returns:
            dict: The JSON response from the Jira API.
        """
        response = requests.request(
            "GET",
            url=self._base_url + "/rest/api/3/myself",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()

    def __generate_issue_body(
        self,
        summary: str,
        description: dict,
        issue_type: str,
        project_key: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[list] = None,
        priority: Optional[str] = None,
        team: Optional[str] = None,
    ) -> str:
        """Generates the issue body payload for creating a new issue.

        Args:
            summary (str): The summary of the issue.
            description (dict): The description of the issue.
            assignee (str): The assignee of the issue.
            issue_type (str): The type of the issue.
            labels (list, optional): The labels of the issue. Defaults to None.
            priority (str, optional): The priority of the issue. Defaults to None.
            team (str, optional): The team to be assigned to the Jira issue. Defaults to None.

        Returns:
            The JSON payload for creating a new issue.
        """
        project_key = project_key or self._project_key
        fields = {
            "fields": {
                "assignee": {"id": assignee if assignee else "-1"},
                "description": description,
                "issuetype": {"id": issue_type},
                "project": {"key": project_key},
                "summary": summary,
            },
        }
        if labels:
            fields["fields"]["labels"] = labels
        if project_key == CONFIG.SUPPORT_BOARD and CONFIG.ADMIN_CODE:
            fields["fields"]["customfield_10077"] = [CONFIG.ADMIN_CODE]
        if priority:
            fields["fields"]["priority"] = {"id": priority}
        if team:
            fields["fields"]["customfield_10001"] = team
        payload = json.dumps(fields)
        return payload

    def move_ticket_to_board(self, ticket_id: str) -> None:
        """Move a ticket to a board using its ID.

        Args:
            self: The object instance
            ticket_id (str): The ID of the ticket to be moved

        Returns:
            None
        """
        payload = json.dumps({"issues": [ticket_id]})
        requests.request(
            "POST",
            url=self._webhook_url,
            headers={"Content-type": "application/json"},
            data=payload,
        )

    @retry_if_bad_request
    def __get_issue_types(self, project_key: Optional[str] = None) -> dict:
        """Get the board information.

        Args:
            self: The object instance

        Returns:
            dict: The board information
        """
        project_key = project_key or self._project_key
        response = requests.request(
            "GET",
            url=self._base_url + f"/rest/api/3/project/{project_key}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return {issue_type["name"].lower(): issue_type["id"] for issue_type in response.json()["issueTypes"]}

    @retry_if_bad_request
    def __get_transtion_types(self, issue_id: str) -> dict:
        """Get the board information.

        Args:
            self: The object instance
            issue_id (str): The ID of the issue

        Returns:
            dict: The board information
        """
        if self._transition_types.get("to do"):
            return self._transition_types

        response = requests.request(
            "GET",
            url=self._base_url + f"/rest/api/3/issue/{issue_id}/transitions",
            headers=self.__get_headers(),
            auth=self._auth,
        )

        self.check_response(response)
        return {
            transition_type["name"].lower(): transition_type["id"] for transition_type in response.json()["transitions"]
        }

    @staticmethod
    def __description_markup(additional_info: str) -> List[dict]:
        """Create the description markup.

        Args:
            additional_info (str): Additional information.

        Returns:
            dict: The description markup.
        """
        return [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Additional info: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": additional_info,
                    },
                ],
            }
        ]

    @staticmethod
    def __error_string_markup(error_string: str, exc_info: str) -> List[dict]:
        """Create the error string markup.

        Args:
            error_string (str): The error string.
            exc_info (str): The exception information.

        Returns:
            dict: The error string markup.
        """
        return [
            {
                "type": "panel",
                "attrs": {"panelType": "error"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": error_string,
                                "marks": [{"type": "code"}],
                            },
                        ],
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    exc_info
                                    if len(exc_info) < CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH
                                    else exc_info[: CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH] + "..."
                                ),
                            }
                        ],
                    },
                ],
            }
        ]

    @staticmethod
    def __warning_markup(warning_message: str, message: str) -> List[dict]:
        """Create the error string markup.

        Args:
            warning_message (str): The warning message.

        Returns:
            dict: The error string markup.
        """
        return [
            {
                "type": "panel",
                "attrs": {"panelType": "warning"},
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": warning_message,
                                "marks": [{"type": "code"}],
                            },
                        ],
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Message: ", "marks": [{"type": "strong"}]},
                            {"type": "text", "text": message},
                        ],
                    },
                ],
            }
        ]

    @staticmethod
    def __date_markup() -> List[dict]:
        """Create the date markup.

        Returns:
            dict: The date markup.
        """
        return [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Error time: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": str(datetime.now().strftime("%B %d, %Y %I:%M:%S %p")),
                    },
                ],
            }
        ]

    def __runlink_markup(self) -> List[dict]:
        """Create the runlink markup.

        Returns:
            dict: The runlink markup.
        """
        return (
            [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Run link: ",
                            "marks": [{"type": "strong"}],
                        },
                    ]
                    + self.__link_markup(),
                }
            ]
            if CONFIG.ENVIRONMENT != "local"
            else []
        )

    def __branch_info_markup(self, exc_traceback: TracebackType) -> List[dict]:
        """Create the branch info markup.

        Returns:
            dict: The branch markup.
        """
        if not self._build_info:
            return []
        frames = get_frames(exc_traceback)
        file_name, line_no, _, _ = frames[-1]
        try:
            path = Path.relative_to(Path(file_name), Path.cwd())
            code_line = (
                f"{self._build_info['repository_url']}/src/{self._build_info['last_commit']}"
                f"/{path.as_posix()}?at={self._build_info['branch']}#lines-{line_no}"
            )
            payload = [
                {
                    "type": "text",
                    "text": f"{str(path.as_posix())}:{line_no}",
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {"href": code_line},
                        }
                    ],
                },
            ]
        except ValueError:
            payload = [
                {
                    "type": "text",
                    "text": "Package error.",
                },
            ]

        input_datetime = datetime.strptime(self._build_info["commit_datetime"], "%Y-%m-%d %H:%M:%S").strftime(
            "%d %B %Y %I:%M:%S %p"
        )
        return [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Bitbucket: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": self._build_info["repository_name"],
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": self._build_info["repository_url"]},
                            }
                        ],
                    },
                    {
                        "type": "text",
                        "text": " @ ",
                    },
                    {
                        "type": "text",
                        "text": self._build_info["branch"],
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": self._build_info["branch_url"]},
                            }
                        ],
                    },
                    {
                        "type": "text",
                        "text": " > ",
                    },
                ]
                + payload,
            },
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Last commit: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": self._build_info["last_commit"][:7],
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": self._build_info["commit_url"]},
                            }
                        ],
                    },
                    {
                        "type": "text",
                        "text": " by ",
                    },
                    {
                        "type": "text",
                        "text": self._build_info["author_username"],
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": self._build_info["author_email"]},
                            }
                        ],
                    },
                    {
                        "type": "text",
                        "text": " on ",
                    },
                    {"type": "text", "text": input_datetime, "marks": [{"type": "code"}]},
                ],
            },
        ]

    @staticmethod
    def __environment_markup() -> List[dict]:
        """Create the environment markup.

        Returns:
            dict: The environment markup.
        """
        return [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Environment: ",
                        "marks": [{"type": "strong"}],
                    },
                    {
                        "type": "text",
                        "text": CONFIG.ENVIRONMENT,
                    },
                ],
            }
        ]

    @staticmethod
    def __bot_name_markup() -> List[dict]:
        """Create the ai worker markup.

        Returns:
            dict: The ai worker markup.
        """
        return (
            [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Process name: ",
                            "marks": [{"type": "strong"}],
                        },
                        {
                            "type": "text",
                            "text": f"{CONFIG.ADMIN_CODE} - {CONFIG.WORKER_NAME}",
                        },
                    ],
                }
            ]
            if CONFIG.ADMIN_CODE and CONFIG.WORKER_NAME
            else []
        )

    @staticmethod
    def __host_markup() -> List[dict]:
        """Create the host worker markup.

        Returns:
            dict: The host worker markup.
        """
        return (
            [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Host: ",
                            "marks": [{"type": "strong"}],
                        },
                        {
                            "type": "text",
                            "text": f"{CONFIG.HOST} > {CONFIG.UNAME}",
                        },
                    ],
                }
            ]
            if CONFIG.HOST and CONFIG.UNAME
            else []
        )

    @staticmethod
    def __traceback_markup(exc_traceback_info: str) -> List[dict]:
        """Create the traceback markup.

        Args:
            exc_traceback (str): The exception traceback info.

        Returns:
            dict: The traceback markup.
        """
        return [
            {
                "type": "expand",
                "attrs": {"title": "Traceback"},
                "content": [
                    {
                        "type": "codeBlock",
                        "attrs": {},
                        "content": [
                            {
                                "type": "text",
                                "text": exc_traceback_info,
                            }
                        ],
                    },
                ],
            }
        ]

    @staticmethod
    def __metadata_markup(metadata: dict) -> List[dict]:
        """Create the metadata markup.

        Args:
            metadata (dict): The metadata.

        Returns:
            dict: The metadata markup.
        """
        return [
            {
                "type": "expand",
                "attrs": {"title": "Metadata"},
                "content": [
                    {
                        "type": "codeBlock",
                        "attrs": {"language": "json"},
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(metadata, indent=4, cls=Encoder),
                            }
                        ],
                    },
                ],
            }
        ]

    @staticmethod
    def __error_markup(error_id: str) -> List[dict]:
        """Create the error markup.

        Args:
            error_id (str): The error ID.

        Returns:
            dict: The error markup.
        """
        return [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": f"Error string ID: {error_id}",
                        "marks": [
                            {"type": "em"},
                            {"type": "subsup", "attrs": {"type": "sub"}},
                        ],
                    },
                    {
                        "type": "text",
                        "text": f" (v{version('t_bug_catcher')})",
                        "marks": [
                            {"type": "em"},
                            {"type": "subsup", "attrs": {"type": "sub"}},
                        ],
                    },
                ],
            },
        ]

    @staticmethod
    def __link_markup():
        link_markup = {
            variables.get("environment"): [
                {
                    "type": "text",
                    "text": CONFIG.EMPOWER_URL,
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {"href": CONFIG.EMPOWER_URL},
                        },
                        {"type": "underline"},
                    ],
                },
                {
                    "type": "text",
                    "text": " [Robocloud ",
                },
                {
                    "type": "text",
                    "text": "link",
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {"href": CONFIG.RC_RUN_LINK},
                        },
                        {"type": "underline"},
                    ],
                },
                {
                    "type": "text",
                    "text": "]",
                },
            ],
            "robocloud": [
                {
                    "type": "text",
                    "text": "https://cloud.robocorp.com",
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {"href": CONFIG.RC_RUN_LINK},
                        },
                        {"type": "underline"},
                    ],
                }
            ],
            "local": [
                {
                    "type": "text",
                    "text": "local run",
                    "marks": [
                        {"type": "underline"},
                    ],
                }
            ],
        }
        return link_markup[CONFIG.ENVIRONMENT]

    def __create_description_markup(
        self,
        exc_type: type,
        exc_value: Union[Exception, str],
        exc_traceback: TracebackType,
        error_id: str,
        additional_info: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Create a description with the given trace_back and additional_info.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception): The exception.
            exc_traceback (TracebackType): The trace_back.
            error_id (str): The error ID.
            additional_info (str, optional): Additional information. Defaults to "".
            metadata (dict, optional): Additional metadata. Defaults to None.

        Returns:
            dict: A dictionary containing the version, type, and content.
        """
        exc_info = f"{exc_type.__name__}: {exc_value}"
        frames = get_frames(exc_traceback)
        error_string: str = frames[-1].line
        exc_traceback_info: str = (
            f"Traceback (most recent call last):\n{''.join(traceback.format_tb(exc_traceback))}{exc_info}"
        )
        if len(exc_traceback_info) > 30000:
            exc_traceback_info: str = (
                f"Traceback (most recent call last):\n{''.join(traceback.format_tb(exc_traceback)[-1])}{exc_info}"
            )

        return {
            "version": 1,
            "type": "doc",
            "content": []
            + (self.__error_string_markup(error_string, exc_info) if error_string else [])
            + self.__bot_name_markup()
            + self.__date_markup()
            + self.__runlink_markup()
            + self.__environment_markup()
            + self.__host_markup()
            + self.__branch_info_markup(exc_traceback)
            + (self.__description_markup(additional_info) if additional_info else [])
            + self.__traceback_markup(exc_traceback_info)
            + (self.__metadata_markup(metadata) if metadata else [])
            + self.__error_markup(error_id),
        }

    def __create_warning_description_markup(
        self,
        warning_message: str,
        message: str,
        warning_id: str,
    ) -> dict:
        """Create a warning description.

        Args:
            warning_message (str): The warning message.
            warning_id (str): The warning ID.

        Returns:
            dict: A dictionary containing the version, type, and content.
        """
        return {
            "version": 1,
            "type": "doc",
            "content": []
            + self.__warning_markup(warning_message, message)
            + self.__bot_name_markup()
            + self.__date_markup()
            + self.__runlink_markup()
            + self.__environment_markup()
            + self.__error_markup(warning_id),
        }

    def __create_internal_error_markup(
        self,
        exc_type: type,
        exc_value: Union[Exception, str],
        exc_traceback: TracebackType,
        error_id: str,
        additional_info: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Create a description with the given trace_back and additional_info.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception): The exception.
            exc_traceback (TracebackType): The trace_back.
            error_id (str): The error ID.
            additional_info (str, optional): Additional information. Defaults to "".
            metadata (dict, optional): Additional metadata. Defaults to None.

        Returns:
            dict: A dictionary containing the version, type, and content.
        """
        exc_info = f"{exc_type.__name__}: {exc_value}"
        frames = get_frames(exc_traceback)
        error_string: str = frames[-1].line
        exc_traceback_info: str = (
            f"Traceback (most recent call last):\n{''.join(traceback.format_tb(exc_traceback))}{exc_info}"
        )
        if len(exc_traceback_info) > 30000:
            exc_traceback_info: str = (
                f"Traceback (most recent call last):\n{''.join(traceback.format_tb(exc_traceback)[-1])}{exc_info}"
            )

        return {
            "version": 1,
            "type": "doc",
            "content": []
            + (self.__error_string_markup(error_string, exc_info) if error_string else [])
            + self.__bot_name_markup()
            + self.__date_markup()
            + self.__runlink_markup()
            + self.__environment_markup()
            + (self.__description_markup(additional_info) if additional_info else [])
            + self.__traceback_markup(exc_traceback_info)
            + (self.__metadata_markup(metadata) if metadata else [])
            + self.__error_markup(error_id),
        }

    def __create_transtion_markup(self, issue_status: str) -> dict:
        """Create a transition markup.

        Args:
            issue_status (str): The status of the Jira issue.

        Returns:
            dict: The transition markup.
        """
        return {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Status of ticket have been changed by Bot: ",
                            },
                            {
                                "type": "text",
                                "text": issue_status,
                                "marks": [{"type": "strong"}],
                            },
                            {
                                "type": "text",
                                "text": " -> ",
                            },
                            {
                                "type": "text",
                                "text": "To Do",
                                "marks": [{"type": "strong"}],
                            },
                        ],
                    },
                ],
            }
        }

    def __create_comment_markup(
        self,
        error: Optional[str] = None,
        attachments: Optional[List] = None,
        additional_info: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Create a comment with the given error and attachments.

        Args:
            error (str): The error string.
            attachments (List): The list of attachments.
            issue_status (str, optional): The issue status. Defaults to "".
            additional_info (str, optional): Additional information. Defaults to "".

        Returns:
            dict: The comment.
        """
        if error:
            error = (
                error
                if len(error) < CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH
                else error[: CONFIG.LIMITS.MAX_DESCRIPTION_LENGTH] + "..."
            )
        date_markup = [
            {
                "type": "text",
                "text": f" at {str(datetime.now().strftime('%B %d, %Y %I:%M:%S %p'))}",
            },
            {"type": "hardBreak"},
        ]

        error_markup = [
            {
                "type": "text",
                "text": error,
                "marks": [{"type": "code"}],
            },
        ]

        comment_markup = [
            {
                "type": "paragraph",
                "content": (
                    [
                        {"type": "text", "text": "Error occures again in "},
                    ]
                    + self.__link_markup()
                    + date_markup
                    + error_markup
                ),
            }
        ]

        attach_markup = [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Attachments: ",
                        "marks": [{"type": "strong"}],
                    },
                ],
            }
        ]
        if attachments:
            for attach in attachments:
                attach_markup[0]["content"].append(
                    {
                        "type": "text",
                        "text": attach[0]["filename"],
                        "marks": [
                            {
                                "type": "link",
                                "attrs": {"href": attach[0]["content"]},
                            }
                        ],
                    },
                )
                attach_markup[0]["content"].append({"type": "text", "text": "; "})

        return {
            "body": {
                "type": "doc",
                "version": 1,
                "content": []
                + (comment_markup if error else [])
                + (self.__description_markup(additional_info) if additional_info else [])
                + (attach_markup if attachments else [])
                + (self.__metadata_markup(metadata) if metadata else []),
            }
        }

    @retry_if_bad_request
    def check_issue_status(self, issue_id: str) -> str:
        """Check the status of a Jira issue.

        Args:
            issue_id (str): The ID of the Jira issue.

        Returns:
            The response from checking the status of the Jira issue.
        """
        response = requests.request(
            "GET",
            self._base_url + f"/rest/api/3/issue/{issue_id}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()["fields"]["status"]["name"]

    def __update_existing_ticket(
        self,
        existing_ticket: dict,
        summary: str,
        attachments: Optional[List] = None,
        additional_info: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """Update an existing ticket.

        Args:
            existing_ticket (dict): The existing ticket.
            attachments (List): The list of attachments.
            summary (str): The summary of the ticket.
            additional_info (str): Additional information.
            metadata (dict): Metadata.

        Returns:
            None
        """
        issue_status = self.check_issue_status(existing_ticket["id"])
        self._transition_types = self.__get_transtion_types(issue_id=existing_ticket["id"])
        if issue_status.lower() not in ["to do", "open"]:
            self.issue_transition(
                ticket_id=existing_ticket["id"],
                transition_id=self._transition_types.get("to do") or self._transition_types.get("open"),
            )
            self.update_comment(
                ticket_id=existing_ticket["id"],
                comments=self.__create_transtion_markup(
                    issue_status=issue_status,
                ),
            )
        issue = self.get_issue(existing_ticket["id"])

        if len(issue["fields"].get("attachment", [])) >= CONFIG.LIMITS.MAX_ISSUE_ATTACHMENTS:
            logger.warning(
                f"Attachments were not uploaded due to exceeding "
                f"{CONFIG.LIMITS.MAX_ISSUE_ATTACHMENTS} attachments limit."
            )
            posted_attachments = []
        else:
            posted_attachments = (
                [
                    self.add_attachment(attachment, issue["id"])
                    for attachment in attachments
                    if os.path.exists(str(attachment))
                ]
                if attachments
                else []
            )

        if len(issue.get("fields", {}).get("comment", {}).get("comments", [])) >= CONFIG.LIMITS.COMMENT_LIMIT:
            logger.warning(
                f"Comments for '{issue.get('key')}' were not posted due to exceeding JIRA comments limit "
                f"({CONFIG.LIMITS.COMMENT_LIMIT})."
            )
            return

        self.update_comment(
            ticket_id=issue["id"],
            comments=self.__create_comment_markup(
                error=summary,
                attachments=posted_attachments,
                additional_info=additional_info,
                metadata=metadata,
            ),
        )

    def __create_new_ticket(
        self,
        summary: str,
        description: dict,
        project_key: Optional[str] = None,
        assignee_id: Optional[str] = None,
        attachments: Optional[List] = None,
        labels: Optional[list] = None,
        priority: Optional[str] = None,
        team: Optional[str] = None,
    ) -> requests.Response:
        """Create a new ticket.

        Args:
            summary (str): The summary of the ticket.
            description (dict): The description of the ticket.
            assignee_id (str, optional): The assignee of the ticket. Defaults to None.
            attachments (List, optional): The list of attachments. Defaults to None.
            labels (List, optional): The list of labels. Defaults to None.
            priority (str, optional): The priority of the ticket. Defaults to None.
            team (str, optional): The team to be assigned to the Jira issue. Defaults to None.

        Returns:
            The response from creating the ticket.
        """
        project_key = project_key or self._project_key
        if project_key == CONFIG.BC_BOARD:
            issue_type = self.__get_issue_types(project_key=project_key).get("task")
        elif CONFIG.STAGE and CONFIG.STAGE.lower() == "hypercare":
            issue_type = self._issue_types.get("hypercare") or self._issue_types.get("epic")
        elif CONFIG.STAGE and CONFIG.STAGE.lower() == "support":
            issue_type = self._issue_types.get("support") or self._issue_types.get("epic")
        elif CONFIG.STAGE and CONFIG.STAGE.lower() == "delivery" and project_key == CONFIG.SUPPORT_BOARD:
            issue_type = self._issue_types.get("development") or self._issue_types.get("epic")
        else:
            issue_type = (
                self._issue_types.get("bug")
                or self._issue_types.get("task")
                or self._issue_types.get("support")
                or self._issue_types.get("epic")
            )

        issue_body = {
            "summary": summary[:255].split("\n")[0],
            "description": description,
            "assignee": assignee_id,
            "issue_type": issue_type,
            "project_key": project_key,
            "labels": labels,
            "priority": priority,
            "team": team,
        }

        issue = self.__generate_issue_body(**issue_body)

        response = self.post_ticket(issue=issue)

        errors = response.json().get("errors", {})

        if errors:
            issue_body = {key: value for key, value in issue_body.items() if key not in errors}
            issue = self.__generate_issue_body(**issue_body)
            response = self.post_ticket(issue=issue)

        if response.status_code != 201:
            logger.warning(
                f"Failed to create Jira issue. Status code: {response.status_code}"
                f" Error messages: {', '.join(response.json()['errorMessages'])}"
                f" Errors: {response.json()['errors']}"
            )

            return response

        ticket = response.json()
        ticket_id = ticket["id"]
        if attachments:
            for attachment in attachments:
                if os.path.exists(str(attachment)):
                    self.add_attachment(attachment, ticket_id)
        if self._webhook_url and project_key != CONFIG.SUPPORT_BOARD:
            self.move_ticket_to_board(ticket_id)
        return response

    def warning_message(self, summary: str, inspected_frame, message: str, assignee: Optional[str] = None) -> None:
        """Create a new ticket with warning message.

        Args:
            summary (str): The summary of the ticket.
            inspected_frame (frame): The frame of the warning.
            assignee (str, optional): The assignee of the ticket. Defaults to None.

        Returns:
            The response from creating the ticket.
        """
        if self._project_key == CONFIG.SUPPORT_BOARD and CONFIG.ADMIN_CODE:
            summary = CONFIG.ADMIN_CODE + " - " + summary

        warning_id, warning_message = self.__generate_warning_id(inspected_frame)

        existing_ticket = self.filter_tickets(
            all_tickets=self.get_issues()["issues"],
            error_id=warning_id,
        )
        if existing_ticket:
            self.__update_existing_ticket(
                existing_ticket=existing_ticket,
                summary=summary,
            )
            return existing_ticket

        assignee_id = None
        assignee = assignee if assignee else self._default_assignee
        if assignee:
            try:
                assignee_id = self.__get_assignee(assignee)
            except Exception as ex:
                logger.info(f"Failed to get assignee {assignee} due to: {ex}")

        description = self.__create_warning_description_markup(
            warning_message=warning_message,
            message=message,
            warning_id=warning_id,
        )
        response = self.__create_new_ticket(
            summary=summary,
            description=description,
            assignee_id=assignee_id,
            labels=["bug_catcher_warning"],
        )

        return response

    def report_error(
        self,
        exception: Optional[Exception] = None,
        assignee: Optional[str] = None,
        team: Optional[str] = None,
        attachments: Union[List, str, Path, None] = None,
        stack_trace: Optional[str] = None,
        metadata: Optional[dict] = None,
        additional_info: Optional[str] = None,
        group_by: Optional[str] = None,
    ) -> dict:
        """Create a Jira issue with the given attachments.

        Args:
            exception (Exception, optional): The exception to be added to the Jira issue.
            assignee (str, optional): The assignee to be added to the Jira issue.
            team (str, optional): The team to be assigned to the Jira issue. Defaults to None.
            attachments (List, optional): List of attachments to be added to the Jira issue.
            stack_trace (str, optional): Stack trace to be added to the Jira issue.
            metadata (dict, optional): Metadata to be added to the Jira issue.
            additional_info (str, optional): Additional information to be added to the Jira issue.
            group_by (str, optional): group_by flag to be added to the Jira issue.

        Returns:
            The response from creating the Jira issue.
        """
        try:
            if not exception:
                _, exception, _ = sys.exc_info()

            if attachments is None:
                attachments = []

            if isinstance(attachments, (str, Path)):
                attachments = [str(attachments)]

            if not isinstance(attachments, List):
                logger.warning(f"Incorrect type of attachments: {type(attachments)}")
                attachments = []

            if hasattr(exception, "custom_attachments"):
                attachments += exception.custom_attachments

            if len(attachments) > CONFIG.LIMITS.MAX_ATTACHMENTS:
                logger.warning(f"Only the first {CONFIG.LIMITS.MAX_ATTACHMENTS} attachments were uploaded.")
            attachments = attachments[: CONFIG.LIMITS.MAX_ATTACHMENTS]

            error_id = self.__generate_error_id(exception)
            group_id = self.generate_group_id(group_by)

            all_issues = self.get_issues()["issues"]

            if group_id:
                existing_tickets = [
                    ticket
                    for ticket in all_issues
                    if ticket["fields"]["description"] and f"{error_id}-" in ticket["fields"]["description"]
                ]
                summary = self.__create_summary(
                    type(exception),
                    exception,
                    exception.__traceback__,
                    len(existing_tickets) + 1 if existing_tickets else 1,
                )
                error_id = f"{error_id}-{group_id}"
            else:
                summary = self.__create_summary(type(exception), exception, exception.__traceback__)

            existing_ticket = self.filter_tickets(
                all_tickets=all_issues,
                error_id=error_id,
            )

            if existing_ticket:
                self.__update_existing_ticket(
                    existing_ticket=existing_ticket,
                    attachments=attachments,
                    summary=summary,
                    additional_info=additional_info,
                    metadata=metadata,
                )
                if stack_trace and os.path.exists(stack_trace):
                    os.remove(stack_trace)
                return existing_ticket

            if stack_trace:
                attachments.insert(0, stack_trace)

            assignee_id = None
            assignee = assignee if assignee else self._default_assignee
            if assignee:
                try:
                    assignee_id = self.__get_assignee(assignee)
                except Exception as ex:
                    logger.info(f"Failed to get assignee {assignee} due to: {ex}")

            description = self.__create_description_markup(
                exc_type=type(exception),
                exc_value=exception,
                exc_traceback=exception.__traceback__,
                error_id=error_id,
                additional_info=additional_info,
                metadata=metadata,
            )

            priority = CONFIG.TICKET_PRIORITIES.HIGH

            response = self.__create_new_ticket(
                summary=summary,
                description=description,
                assignee_id=assignee_id,
                attachments=attachments,
                labels=["bug_catcher"],
                priority=priority,
                team=team,
            )
            if stack_trace and os.path.exists(stack_trace):
                os.remove(stack_trace)
            return response
        except Exception as ex:
            logger.warning(f"Failed to create Jira issue due to: {type(ex)}: {ex}")
            self.report_internal_error(exception=ex, additional_info="Failed to report error.")
            return False

    def report_unhandled_error(self, exception: Exception, stack_trace: str = None):
        """Report an unhandled error to Jira.

        Args:
            exc_type (type): The type of the exception.
            exception (Exception, str): The value of the exception.
            stack_trace (str, optional): Stack trace to be added to the Jira issue.

        Returns:
            The response from creating the Jira issue.
        """
        try:
            summary = self.__create_summary(type(exception), exception, exception.__traceback__)
            error_id = self.__generate_error_id(exception)

            existing_ticket = self.filter_tickets(
                all_tickets=self.get_issues()["issues"],
                error_id=error_id,
            )
            if existing_ticket:
                self.__update_existing_ticket(
                    existing_ticket=existing_ticket,
                    summary=summary,
                )
                if stack_trace and os.path.exists(stack_trace):
                    os.remove(stack_trace)
                return existing_ticket

            assignee_id = None
            if self._default_assignee:
                try:
                    assignee_id = self.__get_assignee(self._default_assignee)
                except Exception as ex:
                    logger.info(f"Failed to get assignee {self._default_assignee} due to: {ex}")

            description = self.__create_description_markup(
                exc_type=type(exception),
                exc_value=exception,
                exc_traceback=exception.__traceback__,
                error_id=error_id,
            )

            priority = CONFIG.TICKET_PRIORITIES.HIGHEST

            response = self.__create_new_ticket(
                summary=summary,
                description=description,
                assignee_id=assignee_id,
                attachments=[stack_trace] if stack_trace else None,
                labels=["bug_catcher", "fatal_error"],
                priority=priority,
            )
            if stack_trace and os.path.exists(stack_trace):
                os.remove(stack_trace)
            return response
        except Exception as ex:
            logger.warning(f"Failed to create Jira issue due to: {type(ex)}: {ex}")
            self.report_internal_error(exception=ex, additional_info="Failed to report unhandled error.")
            return False

    def report_internal_error(self, exception: Exception, metadata: dict = None, additional_info: str = None):
        """Report an internal error to Jira.

        Args:
            exception (Exception): The exception to be added to the Jira issue.
            metadata (dict, optional): The metadata to be added to the Jira issue. Defaults to None.
            additional_info (str, optional): Additional information to be added to the Jira issue. Defaults to None.

        Returns:
            The response from creating the Jira issue.
        """
        try:
            if not exception:
                _, exception, _ = sys.exc_info()

            attachments = [str(file) for file in Path().cwd().glob("stack_details_*.json")]

            summary = self.__create_summary(type(exception), exception, exception.__traceback__)
            error_id = self.__generate_error_id(exception)

            existing_ticket = self.filter_tickets(
                all_tickets=self.get_issues(project_key=CONFIG.BC_BOARD)["issues"],
                error_id=error_id,
            )
            if existing_ticket:
                self.__update_existing_ticket(
                    existing_ticket=existing_ticket,
                    attachments=attachments,
                    summary=summary,
                    additional_info=additional_info,
                    metadata=metadata,
                )
                for file in attachments:
                    os.remove(file)
                return existing_ticket

            description = self.__create_internal_error_markup(
                exc_type=type(exception),
                exc_value=exception,
                exc_traceback=exception.__traceback__,
                error_id=error_id,
                additional_info=additional_info,
                metadata=metadata,
            )

            response = self.__create_new_ticket(
                summary=summary,
                description=description,
                project_key=CONFIG.BC_BOARD,
                attachments=attachments,
                labels=["bug_catcher"],
            )
            for file in attachments:
                os.remove(file)
            logger.info("Created Bug Catcher issue.")
            return response
        except Exception as ex:
            logger.warning(f"Failed to report Bug Catcher issue due to: {type(ex)}: {ex}")

    @retry_if_bad_request
    def add_attachment(self, attachment: str, ticket_id: str) -> Optional[dict]:
        """Uploads an attachment to a Jira ticket.

        Args:
            attachment (str): The path to the file to be attached.
            ticket_id (str): The ID of the Jira ticket.

        Returns:
            None
        """
        if not attachment:
            logger.warning(f"Attachment {attachment} does not exist.")
            return
        if not os.path.exists(attachment):
            logger.warning(f"Attachment {attachment} does not exist.")
            return
        files = {"file": (os.path.basename(attachment), open(attachment, "rb"))}
        headers = {"Accept": "application/json", "X-Atlassian-Token": "no-check"}
        response = requests.request(
            "POST",
            self._base_url + f"/rest/api/3/issue/{ticket_id}/attachments",
            headers=headers,
            auth=self._auth,
            files=files,
        )
        self.check_response(response)
        return response.json()

    @retry_if_bad_request
    def issue_transition(self, ticket_id: str, transition_id: str) -> None:
        """Perform a transition on the given ticket using the provided transition ID.

        Args:
            ticket_id (str): The ID of the ticket to transition.
            transition_id (int): The ID of the transition to be performed.

        Returns:
            None
        """
        payload = json.dumps(
            {
                "transition": {"id": transition_id},
            }
        )
        response = requests.request(
            "POST",
            self._base_url + f"/rest/api/3/issue/{ticket_id}/transitions",
            headers=self.__get_headers(),
            auth=self._auth,
            data=payload,
        )
        self.check_response(response)

    @retry_if_bad_request
    def update_comment(self, ticket_id: str, comments: dict) -> None:
        """Updates the comments for a specific ticket.

        Args:
            ticket_id (str): The ID of the ticket.
            comments (dict): The comments to be added to the ticket.

        Returns:
            None
        """
        payload = json.dumps(comments)

        response = requests.request(
            "POST",
            self._base_url + f"/rest/api/3/issue/{ticket_id}/comment",
            headers=self.__get_headers(),
            auth=self._auth,
            data=payload,
        )
        self.check_response(response)

    @retry_if_bad_request
    def get_jira_user(self, email: str) -> dict:
        """Get Jira user by email.

        Args:
            email (str): The email of the user.

        Returns:
            The Jira user object.
        """
        response = requests.request(
            "GET",
            self._base_url + f"/rest/api/3/user/search?query={email}",
            headers=self.__get_headers(),
            auth=self._auth,
        )
        self.check_response(response)
        return response.json()

    def post_ticket(self, issue: str) -> requests.Response:
        """Create a ticket using the provided issue data and return the response.

        Args:
            issue (str): The data for creating the ticket.

        Returns:
            requests.Response: The response object from the ticket creation request.
        """
        response = requests.request(
            "POST",
            self._base_url + "/rest/api/3/issue",
            data=issue,
            headers=self.__get_headers(),
            auth=self._auth,
        )

        return response

    def filter_tickets(self, all_tickets: List, error_id: str) -> Optional[dict]:
        """Filters tickets based on summary and error string ID and returns a matching ticket if found.

        Args:
            all_tickets (list): List of all tickets to filter.
            error_id (str): The error string ID to filter by.

        Returns:
            dict or None: The matching ticket if found, otherwise None.
        """
        for ticket in all_tickets:
            if not ticket["fields"]["description"]:
                continue
            if f"{error_id}_~" not in ticket["fields"]["description"]:
                continue
            return ticket

        else:
            return None

    def generate_group_id(self, group_by: Optional[str] = None) -> Optional[str]:
        """Generates a group ID based on the provided group_by string.

        Args:
            group_by (str): The string to use for generating the group ID.

        Returns:
            str or None: The generated group ID if group_by is not None, otherwise None.
        """
        if not group_by:
            return None
        crc_hash = zlib.crc32(group_by.encode())
        return format(crc_hash, "x")

    def __generate_error_id(self, exception: Exception) -> str:
        """Generates an error string ID using the exception, function name, and error string.

        Args:
            exception (Exception):

        Returns:
            str: The generated error string ID and the group ID.

        """
        frames = get_frames(exception.__traceback__)
        exception_chain = "-".join([f"{frame.name}" for frame in frames])
        rel_path = os.path.relpath(frames[-1].filename, os.getcwd())
        path = Path(os.path.splitext(rel_path)[0]).as_posix()
        path = remove_holotree_id(path)
        error_id = (
            f"{path}-{exception_chain}-{frames[-1].line}-" f"{type(exception).__module__}-{type(exception).__name__}"
        )
        hashed_id = hashlib.md5(error_id.encode()).hexdigest()
        return hashed_id

    @staticmethod
    def __generate_warning_id(inspected_frame) -> tuple:
        """Generates an error string ID using the exception, function name, and error string.

        Args:
            inspected_frame (frame): The frame of the warning.

        Returns:
            tuple: The generated error string ID and the warning message.
        """
        lineno = inspected_frame.f_lineno
        filename = inspected_frame.f_code.co_filename
        func = inspected_frame.f_code.co_name
        line = linecache.getline(filename, lineno).strip()
        rel_path = os.path.relpath(filename, os.getcwd())

        warning_message = f"{line}\n{rel_path}:{func}:{lineno}"
        warning_id = hashlib.md5(f"{filename}-{lineno}-{func}-{line}".encode()).hexdigest()
        return warning_id, warning_message

    def __get_assignee(self, assignee: str) -> str:
        """Get assignee Jira user by ID.

        Args:
            assignee (str): The ID of the assignee.

        Returns:
            str: The ID of the assignee.
        """
        if assignee in self._assignee_cache:
            return self._assignee_cache[assignee]
        response = self.get_jira_user(assignee)
        self._assignee_cache[assignee] = response[0]["accountId"]
        return response[0]["accountId"]

    @staticmethod
    def sanitize_summary(exception: Union[Exception, str]) -> str:
        """Remove locators from the exception.

        Args:
            exception (Union[Exception, str]): The exception to be cleaned.

        Returns:
            str: The cleaned exception string.
        """
        message = re.sub("<([a-z]+)(?![^>]*\/>)[^>]*>", r"<\1>", str(exception))
        message = re.sub(">([^<]+)<\/", ">...</", message)
        if "selenium" not in exception.__class__.__name__.lower() and not isinstance(exception, AssertionError):
            return str(message)
        return re.sub(r"\'(.+)\'", "'...'", message)

    def __create_summary(
        self, exc_type: type, exc_value: Union[Exception, str], exc_traceback: TracebackType, idx: Optional[int] = None
    ) -> str:
        """Create the summary of the ticket.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception, str): The value of the exception.
            exc_traceback (TracebackType): The traceback of the exception.

        Returns:
            str: The summary of the ticket.
        """
        frames = get_frames(exc_traceback)
        file_name, line_no, _, _ = frames[-1]

        if idx:
            summary = f"[{exc_type.__name__}:{os.path.basename(file_name)}:{line_no}({idx})]"
        else:
            summary = f"[{exc_type.__name__}:{os.path.basename(file_name)}:{line_no}]"
        if self._project_key == CONFIG.SUPPORT_BOARD and CONFIG.ADMIN_CODE:
            summary = CONFIG.ADMIN_CODE + " - " + summary
        if CONFIG.LIMITS.SUMMARY_LENGTH <= len(summary):
            return summary
        else:
            message = self.sanitize_summary(exc_value)
            message = (
                message
                if len(message) <= CONFIG.LIMITS.SUMMARY_LENGTH - len(summary)
                else message[: CONFIG.LIMITS.SUMMARY_LENGTH - len(summary)] + "..."
            )
            return summary + " " + message
