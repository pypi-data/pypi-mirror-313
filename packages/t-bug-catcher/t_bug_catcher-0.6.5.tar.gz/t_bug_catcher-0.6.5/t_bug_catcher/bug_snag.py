import sys
from typing import Optional

import bugsnag
import requests

from .config import CONFIG
from .utils import logger
from .workitems import variables

bugsnag.configuration.auto_notify = False


class BugSnag:
    """BugSnag class for interacting with the BugSnag API."""

    def __init__(self):
        """Initializes the BugSnag class."""
        pass

    def config(self, api_key: str) -> bool:
        """Configures the BugSnag class.

        Args:
            api_key (str): The API key for the BugSnag account.

        Returns:
            bool: True if the configuration was successful, False otherwise.
        """
        try:
            bugsnag.configure(api_key=api_key, release_stage=CONFIG.ENVIRONMENT, auto_notify=False)
            bugsnag.add_metadata_tab(
                "Metadata",
                {
                    "run_url": variables.get("processRunUrl", ""),
                    "run_by": variables.get("userEmail", ""),
                },
            )
            response = requests.request(
                "POST",
                "https://otlp.bugsnag.com/v1/traces",
                headers={
                    "Content-Type": "application/json",
                    "Bugsnag-Api-Key": api_key,
                    "Bugsnag-Payload-Version": "4",
                    "Bugsnag-Span-Sampling": "True",
                },
                data='{"message": "test"}',
            )
            if response.status_code not in [200, 201, 202, 204]:
                logger.warning(f"Error connecting to Bugsnag: {response.text}")
                return False
            return True
        except Exception as ex:
            logger.warning(f"Failed to configure Bugsnag: {ex}")
            return False

    def report_error(self, exception: Optional[Exception] = None, metadata: Optional[dict] = None):
        """Sends an error to BugSnag.

        Args:
            exception (Exception, optional): The exception to report.
            metadata (dict, optional): The metadata to be added to the Bugsnag issue. Defaults to None.

        Returns:
            None
        """
        if not exception:
            _, exception, _ = sys.exc_info()
        if isinstance(metadata, dict):
            bugsnag.notify(exception=exception, metadata={"special_info": metadata})
            return
        if metadata is None:
            bugsnag.notify(exception=exception)
            return
        logger.warning(f"Incorrect type of metadata: {type(metadata)}")
        bugsnag.notify(exception=exception)

    def report_unhandled_error(self, exc_type, exc_value, traceback):
        """Sends an unhandled exception to BugSnag.

        Args:
            exc_type (type): The type of the exception.
            exc_value (Exception): The value of the exception.
            traceback (traceback): The traceback of the exception.

        Returns:
            None
        """
        bugsnag.notify((exc_type, exc_value, traceback), severity="error")
