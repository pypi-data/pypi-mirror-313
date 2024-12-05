import requests
from ffquant.utils.Logger import stdout_log

__ALL__ = ['add_marker']

def add_marker(id:str = None, datetime:str = None, type:str = "LOG_INFO", title:str = None, message:str = None, debug=False):
    """
    Sends a GET request to add a marker to a logging service.

    Parameters:
    id (str, optional): Identifier for the marker. Defaults to None.
    datetime (str, optional): Date and time for the marker. Defaults to None.
    type (str, optional): Type of log. Possible values are "LOG_ERROR", "LOG_INFO". Defaults to "LOG_INFO".
    title (str, optional): Title of the log. Defaults to None.
    message (str, optional): Message content of the log. Defaults to None.
    debug (bool, optional): If True, enables logging of the request process. Defaults to False.

    Returns:
    bool: True if the marker was added successfully, False otherwise.
    """
    url = f"http://192.168.25.247:8220/log/tv/{id}"
    params = {
        "time": datetime,
        "type": type,
        "title": title,
        "message": message
    }
    response = requests.get(url, params=params).json()
    if response.get('code') == "200":
        if debug:
            stdout_log(f"add_marker success, response: {response}")
        return True
    else:
        if debug:
            stdout_log(f"add_marker fail, response: {response}")
        return False

if __name__ == "__main__":
    add_marker(id="14282760", datetime="2024-11-05 12:00:00", type="LOG_INFO", title="准盈", message="hello world & hello again %!@#$%^&*()<>,.", debug=True)