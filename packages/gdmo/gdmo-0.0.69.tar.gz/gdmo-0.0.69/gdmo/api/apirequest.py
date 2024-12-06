import requests
import json

class APIRequest: 
    def __init__(self, url):
        """
        Initializes a RestAPI object with the specified url.

        Args:
        - url (str): Required. URL to send the request to.
        """
        if not url.startswith('http'):
            raise ValueError('Invalid URL. Must start with http:// or https://')
        self._url       = url # Required. URL to send the request to.
        self._method    = 'POST' # Required. Identifies the method used in the call
        self._headers   = {'Content-Type':'application/json'} # Optional. A dictionary of HTTP headers to send to the specified url.
        self._json      = None
        self._data      = None
        self._params    = {} # Optional. A dictionary of query parameters to send with the request.
        self._response  = ''

    def set_header(self, key, value):
        """
        Sets the specified key-value pair in the HTTP headers dictionary.
   
        Args:
        - key (str): Required. The key to set in the headers dictionary.
        - value (str): Required. The value to set for the specified key.

        Returns:
        - bool: True if the key-value pair was successfully set in the headers dictionary.
        """
        if not isinstance(key, str):
            raise TypeError('Header key must be a string')
        if not isinstance(value, str):
            raise TypeError('Header value must be a string')
        self._headers[key] = value
        return self

    def set_auth(self, value):
        """
        Sets the specified HTTP authentication tuple.

        Args:
        - value (tuple): Required. A tuple to enable a certain HTTP authentication.

        Returns:
        - bool: True if the authentication tuple was successfully set.
        """
        self._auth = value
        return self

    def set_param(self, key, value):
        """
        Sets the specified key-value pair in the parameters dictionary.

        Args:
        - key (str): Required. The key to set in the parameters dictionary.
        - value (str): Required. The value to set for the specified key.

        Returns:
        - bool: True if the key-value pair was successfully set in the parameters dictionary.
        """
        self._params[key] = value
        return self

    def set_parameters(self, parameters):

        for key in parameters:
            self.set_param(key, parameters[key])

        return self

    def set_content_type(self, value):
        """
        Sets the specified content type in the HTTP headers dictionary.

        Args:
        - value (str): Required. The content type to set in the headers dictionary.

        Returns:
        - bool: True if the content type was successfully set in the headers dictionary.

        Raises:
        - ValueError: If the specified content type is invalid.
        """
        content_types = [
            'application/vnd.android.package-archive',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'application/vnd.oasis.opendocument.graphics',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.mozilla.xul+xml',
            'video/mpeg',
            'video/mp4',
            'video/quicktime',
            'video/x-ms-wmv',
            'video/x-msvideo',
            'video/x-flv',
            'video/webm',
            'text/css',
            'text/csv',
            'text/html',
            'text/javascript',
            'text/plain',
            'text/xml',
            'multipart/mixed',
            'multipart/alternative',
            'multipart/related',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/tiff',
            'image/vnd.microsoft.icon',
            'image/x-icon',
            'image/vnd.djvu',
            'image/svg+xml',
            'audio/mpeg',
            'audio/x-ms-wma',
            'audio/vnd.rn-realaudio',
            'audio/x-wav',
            'application/java-archive',
            'application/EDI-X12',
            'application/EDIFACT',
            'application/javascript',
            'application/octet-stream',
            'application/ogg',
            'application/pdf',
            'application/xhtml+xml',
            'application/x-shockwave-flash',
            'application/json',
            'application/ld+json',
            'application/xml',
            'application/zip',
            'application/x-www-form-urlencoded'
        ]
        
        if value not in content_types:
            raise ValueError(f"Invalid content type: {value}")
        
        self._headers['Content-Type'] = value
        return self

    def set_method(self, method):
        """
        Sets the specified HTTP method.

        Args:
        - method (str): Required. The HTTP method to set.

        Returns:
        - bool: True if the HTTP method was successfully set.
        """
        if method not in ["POST", "GET", "PATCH", "PUT"]:
            raise ValueError("Invalid HTTP method. Only POST, GET, PATCH, and PUT methods are allowed.")
        self._method = method        
        return self

    def set_data(self, data):
        """
        Sets the specified data to be sent in the HTTP request.

        Args:
        - data (dict, list of tuples, bytes, or file object): Required. The data to send in the HTTP request.

        Returns:
        - bool: True if the data was successfully set.
        """
        self._data = data
        return self

    def set_json(self, json_data):
        """
        Sets the specified JSON data to be sent in the HTTP request.

        Args:
        - json_data (str): Required. The JSON data to send in the HTTP request.

        Returns:
        - bool: True if the JSON data was successfully set.

        Raises:
        - ValueError: If the specified JSON data is invalid.
        """
        try:
            json.loads(json_data)
        except ValueError:
            raise ValueError("Invalid JSON data")

        self._json = json_data
        return self

    def make_request(self):
        """
        Sends the HTTP request using the specified parameters.

        Returns:
        - APIRequest: The APIRequest object.
        """
        data = self._data if self._data else None
        json_data = self._json if self._json else None
        params = self._params if self._params else None
        headers = self._headers if self._headers else None

        # Check if params is a dictionary
        if params is not None and not isinstance(params, dict):
            raise ValueError("Params must be a dictionary")
        # Check if headers is a dictionary
        if headers is not None and not isinstance(headers, dict):
            raise ValueError("Headers must be a dictionary")

        try:
            if self._method == "POST":
                self._response = requests.post(
                    self._url,
                    headers=headers,
                    json=json_data,
                    data=data,
                    timeout=7200
                )
            elif self._method == "GET":
                self._response = requests.get(
                    self._url,
                    headers=headers,
                    params=params
                )
            else:
                raise ValueError(f"Method {self._method} not supported")

            self._response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else self._response.status_code
            reason = e.response.reason if e.response else self._response.reason
            message = f"HTTP error: {e}\n"
            message += f"Status Code: {status_code}\n"
            message += f"Reason: {reason}\n"
            message += f"Headers: {self._headers}\n"
            message += f"Method: {self._method}\n"
            message += f"Data: {data}\n"
            message += f"Params: {params}\n"
            message += f"URL: {self._url}\n"
            return requests.exceptions.HTTPError(message)
        except requests.exceptions.RequestException as e:
            message  = f"HTTP error: {e}\n"
            message += f"Headers: {self._headers}\n"
            message += f"Method: {self._method}\n"
            message += f"Data: {data}\n"
            message += f"Params: {params}\n"
            message += f"URL: {self._url}\n"
            return requests.exceptions.HTTPError(message)

        return self

    def get_json_response(self):
        """
        Returns the JSON response from the HTTP request.

        Returns:
        - dict: The JSON response from the HTTP request.
        """
        response = self._response
        try:
            json_response = response.json()
        except ValueError:
            raise ValueError('Response is not valid JSON')
        return json_response
    
    def get_raw_response(self):
        return self._response
