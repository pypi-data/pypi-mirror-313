from ML_management import variables


def set_server_url(url: str) -> None:
    """
    Set server URL.

    If you set the URL using this function,
    it takes precedence over the URL from the environment variable 'server_url'.

    Parameters
    ==========
    url: str
        Server url.
    Returns
    =======
    None
    """
    variables.server_url = url


def set_mlm_credentials(login: str, password: str) -> None:
    """
    Set login and password for mlmanagement.

    If you set the credentials using this function,
    it takes precedence over the credentials from the environment variables.

    Parameters
    ==========
    login: str
        Your mlm login.
    passwrod: str
        Yor mlm password.
    Returns
    =======
    None
    """
    variables.mlm_login = login
    variables.mlm_password = password


def get_server_url() -> str:
    """Get the current server URL."""
    return variables.get_server_url()
