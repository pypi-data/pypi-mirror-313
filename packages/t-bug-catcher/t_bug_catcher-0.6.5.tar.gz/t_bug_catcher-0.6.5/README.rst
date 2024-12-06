t-bug-catcher
==============

Description
-----------
The `t-bug-catcher` package is a bug reporting tool that allows users to easily submit bug reports for the application.

Installation
------------
You can install the `t-bug-catcher` package using pip:

.. code-block:: bash

    pip install t-bug-catcher

Usage
-----
To use the bug catcher in your application, import the package and initialize it:

.. code-block:: python

    from t_bug_catcher import report_error
    ...
    try:
        ...
    except Exception:
        report_error()

Configuration
-------------
You can configure the bug catcher by passing options during initialization:

.. code-block:: python
    
    from t_bug_catcher import configure
    ...
    configure.jira(
        login="JIRA_LOGIN",
        api_token="JIRA_API_TOKEN",
        project_key="PROJECT_NAME",
    )
    configure.bugsnag(
        api_token="BUGSNAG_API_TOKEN",
    )
