"""JiraPoster class for interacting with the Jira API."""

import inspect
import os
import sys
from types import TracebackType
from typing import List, Optional

from .bug_snag import BugSnag
from .config import CONFIG
from .jira import Jira
from .stack_saver import StackSaver
from .utils import logger
from .utils.common import get_frames


class Configurator:
    """Configurer class for configuring the JiraPoster and BugSnag."""

    def __init__(self, jira: Jira, bugsnag: BugSnag):
        """Initializes the Configurer class."""
        self.__jira: Jira = jira
        self.__bug_snag: BugSnag = bugsnag
        self.__jira_configured = False
        self.__bug_snag_configured = False

    def jira(
        self,
        login: str,
        api_token: str,
        project_key: str,
        webhook_url: Optional[str] = None,
        default_assignee: Optional[str] = None,
    ):
        """Configures the JiraPoster and BugSnag classes.

        Args:
            login (str): The username for the Jira account.
            api_token (str): The API token for the Jira account.
            project_key (str): The key of the Jira project.
            webhook_url (str, optional): The webhook URL for the Jira project. Defaults to None.
            default_assignee (str, optional): The default assignee for the Jira project. Defaults to None.

        Returns:
            None
        """
        self.__jira_configured = self.__jira.config(
            login=login,
            api_token=api_token,
            project_key=project_key,
            webhook_url=webhook_url,
            default_assignee=default_assignee,
        )

    def bugsnag(self, api_key: str):
        """Configures the BugSnag class.

        Args:
            api_key (str): The API token for the BugSnag account.

        Returns:
            None
        """
        self.__bug_snag_configured = self.__bug_snag.config(api_key=api_key)

    @property
    def is_jira_configured(self):
        """Checks if the JiraPoster class has been configured."""
        return self.__jira_configured

    @property
    def is_bugsnag_configured(self):
        """Checks if the BugSnag class has been configured."""
        return self.__bug_snag_configured


class BugCatcher:
    """BugCatcher class for interacting with the Jira API."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one BugCatcher instance is created."""
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initializes the BugCatcher class."""
        self.__jira: Jira = Jira()
        self.__bug_snag: BugSnag = BugSnag()
        self.__configurator: Configurator = Configurator(self.__jira, self.__bug_snag)
        self.__sys_excepthook = None
        self.__stack_saver = StackSaver()
        self.__errors_count = 0

    @property
    def configure(self):
        """Configures the JiraPoster and BugSnag classes."""
        return self.__configurator

    def get_errors_count(self):
        """Returns the number of exceptions reported."""
        return self.__errors_count

    def report_error(
        self,
        exception: Optional[Exception] = None,
        description: Optional[str] = None,
        metadata: Optional[dict] = None,
        attachments: Optional[List] = None,
        assignee: Optional[str] = None,
        team: Optional[str] = None,
        group_by: Optional[str] = None,
    ):
        """Reports an error to the Jira project.

        Args:
            exception (Exception, optional): The exception to report. Defaults to None.
            description (str, optional): The description of the error. Defaults to "".
            metadata (dict, optional): The metadata to be added to the Jira issue. Defaults to None.
            attachments (List, optional): The attachments to be added to the Jira issue. Defaults to None.
            assignee (str, optional): The assignee to be added to the Jira issue. Defaults to None.
            team (str, optional): The team to be assigned to the Jira issue. Defaults to None.
            group_by (str, optional): The group to be assigned to the Jira issue. Defaults to None.

        Returns:
            None
        """
        if CONFIG.ENVIRONMENT.lower() == "local":
            logger.warning("Reporting an error is not supported in local environment.")
            return

        if not self.__configurator.is_jira_configured and not self.__configurator.is_bugsnag_configured:
            logger.warning("Jira and BugSnag are not configured. Please configure them before reporting an error.")
            return

        if not exception:
            _, exception, _ = sys.exc_info()

        if not isinstance(exception, Exception):
            logger.warning("Implementation error. Incorrect exception type.")
            inspected_frame = inspect.currentframe().f_back
            if self.__configurator.is_jira_configured:
                self.__jira.warning_message(
                    summary="bug_catcher implementation warning ⚠️",
                    inspected_frame=inspected_frame,
                    message=(
                        "Incorrect exception type. Check the variable that holds the exception "
                        "and make sure that report_error() in the try/except block is called."
                    ),
                    assignee=assignee,
                )
            return

        if not getattr(exception, "__traceback__", None):
            logger.warning("Implementation error. No traceback available.")
            inspected_frame = inspect.currentframe().f_back
            if self.__configurator.is_jira_configured:
                self.__jira.warning_message(
                    summary="bug_catcher implementation warning ⚠️",
                    inspected_frame=inspected_frame,
                    message=(
                        "No traceback is available. Please, use an exception with a traceback in the try/except block. "
                        "Not just called exceptions."
                    ),
                    assignee=assignee,
                )
            return

        handled_error = getattr(exception, "handled_error", None)
        if handled_error:
            logger.warning(f"Exception {handled_error} already reported.")
            return

        stack_trace = self.__stack_saver.save_stack_trace(exception)

        if self.__configurator.is_jira_configured:
            self.__jira.report_error(
                exception=exception,
                assignee=assignee,
                team=team,
                attachments=attachments,
                stack_trace=stack_trace,
                additional_info=description,
                metadata=metadata,
                group_by=group_by,
            )

        if self.__configurator.is_bugsnag_configured:
            self.__bug_snag.report_error(
                exception=exception,
                metadata=metadata,
            )

        frames = get_frames(exception.__traceback__)
        exc_info = f"{os.path.basename(frames[-1].filename)}:{frames[-1].name}:{frames[-1].lineno}"
        exception.handled_error = exc_info
        logger.info(f"Exception {exc_info} reported.")
        self.__errors_count += 1

    def report_error_to_jira(
        self,
        exception: Optional[Exception] = None,
        assignee: Optional[str] = None,
        attachments: Optional[List] = None,
        metadata: Optional[dict] = None,
        additional_info: Optional[str] = None,
    ):
        """Creates a Jira issue with the given attachments.

        Args:
            exception (Exception, optional): The exception to report. Defaults to None.
            assignee (str, optional): The assignee to be added to the Jira issue. Defaults to None.
            attachments (List, optional): The attachments to be added to the Jira issue. Defaults to None.
            additional_info (str, optional): The additional information to be added to the Jira issue. Defaults to "".
            metadata (dict, optional): The metadata to be added to the Jira issue. Defaults to None.

        Returns:
            None

        """
        if CONFIG.ENVIRONMENT.lower() == "local":
            logger.warning("Reporting an error is not supported in local environment.")
            return

        self.__jira.report_error(
            exception=exception,
            assignee=assignee,
            attachments=attachments,
            additional_info=additional_info,
            metadata=metadata,
        )

    def report_error_to_bugsnag(self, exception: Optional[Exception] = None, metadata: Optional[dict] = None):
        """Sends an error to BugSnag.

        Args:
            exception (Exception): The exception to report.
            metadata (dict, optional): The metadata to be added to the Bugsnag issue. Defaults to None.

        Returns:
            None

        """
        if CONFIG.ENVIRONMENT.lower() == "local":
            logger.warning("Reporting an error is not supported in local environment.")
            return

        self.__bug_snag.report_error(
            exception=exception,
            metadata=metadata,
        )

    @staticmethod
    def attach_file_to_exception(exception: Exception, attachment: str) -> None:
        """Update the exception with the given attachment.

        Args:
            exception (Exception): The exception to update.
            attachment (str): The attachment to add to the exception.

        Returns:
            None
        """
        if hasattr(exception, "custom_attachments"):
            exception.custom_attachments.append(attachment)
        else:
            exception.custom_attachments = [attachment]

    def __excepthook(self, exc_type: type, exc_value: Exception, exc_traceback: TracebackType) -> None:
        """Handles unhandled exceptions.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception): The value of the exception.
            exc_traceback (traceback): The traceback of the exception.

        Returns:
            None
        """
        if CONFIG.ENVIRONMENT.lower() == "local":
            logger.warning("Reporting an error is not supported in local environment.")
            return

        if not self.__configurator.is_jira_configured and not self.__configurator.is_bugsnag_configured:
            logger.warning("Jira and BugSnag are not configured. Please configure them before reporting an error.")
            return

        handled_error = getattr(exc_value, "handled_error", None)
        if handled_error:
            logger.warning(f"Exception {handled_error} already reported.")
            return

        stack_trace = self.__stack_saver.save_stack_trace(exc_value)

        if self.__configurator.is_jira_configured:
            self.__jira.report_unhandled_error(exc_value, stack_trace)
        if self.__configurator.is_bugsnag_configured:
            self.__bug_snag.report_unhandled_error(exc_type, exc_value, exc_traceback)
        frames = get_frames(exc_value.__traceback__)
        exc_info = f"{os.path.basename(frames[-1].filename)}:{frames[-1].name}:{frames[-1].lineno}"
        logger.info(f"Exception {exc_info} reported.")
        self.__errors_count += 1

    def __get_sys_hook_attribute(self, attribute: str = "bug_catcher_client"):
        """Checks if the system hook is installed.

        Args:
            attribute (str, optional): The attribute to check. Defaults to "bug_catcher_client".

        Returns:
            The attribute of the system hook if it is installed, otherwise None.
        """
        return getattr(sys.excepthook, attribute, None)

    def install_sys_hook(self):
        """Installs a system hook to handle unhandled exceptions."""
        if self.__get_sys_hook_attribute():
            return

        self.__sys_excepthook = sys.excepthook

        def excepthook(*exc_info):
            self.__excepthook(*exc_info)

            if self.__sys_excepthook:
                self.__sys_excepthook(*exc_info)

        sys.excepthook = excepthook
        sys.excepthook.bug_catcher_client = self

    def uninstall_sys_hook(self):
        """Uninstalls the system hook to handle unhandled exceptions."""
        client = self.__get_sys_hook_attribute()

        if client is self and self.__sys_excepthook:
            sys.excepthook = self.__sys_excepthook
            self.__sys_excepthook = None


__bug_catcher = BugCatcher()
__bug_catcher.install_sys_hook()

configure = __bug_catcher.configure
report_error = __bug_catcher.report_error
attach_file_to_exception = __bug_catcher.attach_file_to_exception
report_error_to_jira = __bug_catcher.report_error_to_jira
report_error_to_bugsnag = __bug_catcher.report_error_to_bugsnag
install_sys_hook = __bug_catcher.install_sys_hook
uninstall_sys_hook = __bug_catcher.uninstall_sys_hook
get_errors_count = __bug_catcher.get_errors_count
