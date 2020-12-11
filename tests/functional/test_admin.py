"""
This file (test_admin.py) contains the functional tests for the `admin` blueprint.
"""


def test_cli_create_admin_user(cli_test_runner):
    """
    GIVEN a Flask CLI test runner
    WHEN the 'flask admin create_admin_user' command is processed
    THEN check that a new admin user is created
    """
    result = cli_test_runner.invoke(args=['admin', 'create_admin_user',
                                          'patrick_admin2@email.com',
                                          'FlaskIsMyFavorite567'])
    assert 'Created new admin user (patrick_admin2@email.com)!' in result.output
