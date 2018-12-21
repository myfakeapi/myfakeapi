import uuid

from django.db import models
from django.contrib.auth import get_user_model

# Taken from https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"
HEAD = "HEAD"
CONNECT = "CONNECT"
OPTIONS = "OPTIONS"
TRACE = "TRACE"
PATCH = "PATCH"

DEFAULT_HTTP_METHOD = GET
HTTP_METHODS = (
    (DEFAULT_HTTP_METHOD, DEFAULT_HTTP_METHOD),
    (POST, POST),
    (PUT, PUT),
    (DELETE, DELETE),
    (HEAD, HEAD),
    (CONNECT, CONNECT),
    (OPTIONS, OPTIONS),
    (TRACE, TRACE),
    (PATCH, PATCH),
)

HTTP = "http"  # rest or soap api
WEBSOCKETS = "ws"

DEFAULT_MOCK_TYPE = HTTP
MOCK_TYPES = (
    (HTTP, HTTP),
    (WEBSOCKETS, WEBSOCKETS)
)

# Compiled from https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# and https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

DEFAULT_HTTP_CODE = 200
HTTP_CODES = (
    (None, "-- Information responses --"),
    (100, "100 - Continue"),
    (101, "101 - Switching Protocol"),
    (102, "102 - Processing (WebDAV)"),
    (103, "103 - Early Hints"),
    (None, "-- Successful responses --"),
    (DEFAULT_HTTP_CODE, "200 - OK"),
    (201, "201 - Created"),
    (202, "202 - Accepted"),
    (203, "203 - Non-Authoritative Information"),
    (204, "204 - No Content"),
    (205, "205 - Reset Content"),
    (206, "206 - Partial Content"),
    (207, "207 - Multi-Status (WebDAV)"),
    (208, "208 - Multi-Status (WebDAV)"),
    (226, "226 - IM Used"),
    (None, "-- Redirection messages --"),
    (300, "300 - Multiple Choice"),
    (301, "301 - Moved Permanently"),
    (302, "302 - Found"),
    (303, "303 - See Other"),
    (304, "304 - Not Modified"),
    (305, "305 - Use Proxy"),
    (306, "306 - Unused"),
    (307, "307 - Temporary Redirect"),
    (308, "308 - Permanent Redirect"),
    (None, "-- Client error responses --"),
    (400, "400 - Bad Request"),
    (401, "401 - Unauthorized"),
    (402, "402 - Payment Required"),
    (403, "403 - Forbidden"),
    (404, "404 - Not Found"),
    (405, "405 - Method Not Allowed"),
    (406, "406 - Not Acceptable"),
    (407, "407 - Proxy Authentication Required"),
    (408, "408 - Request Timeout"),
    (409, "409 - Conflict"),
    (410, "410 - Gone"),
    (411, "411 - Length Required"),
    (412, "412 - Precondition Failed"),
    (413, "413 - Payload Too Large"),
    (414, "414 - URI Too Long"),
    (415, "415 - Unsupported Media Type"),
    (416, "416 - Requested Range Not Satisfiable"),
    (417, "417 - Expectation Failed"),
    (418, "418 - I'm a teapot"),
    (421, "421 - Misdirected Request"),
    (422, "422 - Unprocessable Entity (WebDAV)"),
    (423, "423 - Locked (WebDAV)"),
    (424, "424 - Failed Dependency (WebDAV)"),
    (425, "425 - Too Early"),
    (426, "426 - Upgrade Required"),
    (428, "428 - Precondition Required"),
    (429, "429 - Too Many Requests"),
    (431, "431 - Request Header Fields Too Large"),
    (451, "451 - Unavailable For Legal Reasons"),
    (None, "-- Server error responses --"),
    (500, "500 - Internal Server Error"),
    (501, "501 - Not Implemented"),
    (502, "502 - Bad Gateway"),
    (503, "503 - Service Unavailable"),
    (504, "504 - Gateway Timeout"),
    (505, "505 - HTTP Version Not Supported"),
    (506, "506 - Variant Also Negotiates"),
    (507, "507 - Insufficient Storage"),
    (508, "508 - Loop Detected (WebDAV)"),
    (510, "510 - Not Extended"),
    (511, "511 - Network Authentication Required"),
)

CONTENT_TYPE_TEXT_PLAIN = "text/plain"
CONTENT_TYPE_TEXT_HTML = "text/html"
CONTENT_TYPE_APPLICATION_JSON = "application/json"
CONTENT_TYPE_APPLICATION_JAVASCRIPT = "application/javascript"

DEFAULT_CONTENT_TYPE = CONTENT_TYPE_TEXT_PLAIN
CONTENT_TYPE_LIST = (
    (CONTENT_TYPE_TEXT_PLAIN, "Plain ({})".format(CONTENT_TYPE_TEXT_PLAIN)),
    (CONTENT_TYPE_TEXT_HTML, "HTML ({})".format(CONTENT_TYPE_TEXT_HTML)),
    (CONTENT_TYPE_APPLICATION_JSON, "JSON ({})".format(CONTENT_TYPE_APPLICATION_JSON)),
    (CONTENT_TYPE_APPLICATION_JAVASCRIPT, "JSONP ({})".format(CONTENT_TYPE_APPLICATION_JAVASCRIPT)),
)


class API(models.Model):
    """
    API handler set
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(blank=True, null=True, max_length=100)
    public = models.BooleanField(default=False)
    users = models.ManyToManyField(get_user_model())

    def __str__(self):
        """
        Object representation as string
        :return:
        """
        return self.title


class APIHandler(models.Model):
    """
    Fake API handler
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api = models.ForeignKey("my_fake_api.API", on_delete=models.CASCADE)
    mock_type = models.CharField(choices=MOCK_TYPES, max_length=10, default=DEFAULT_MOCK_TYPE)

    request_path = models.CharField(max_length=3000)
    request_method = models.CharField(choices=HTTP_METHODS, max_length=10, default=DEFAULT_HTTP_METHOD)
    request_body = models.TextField(blank=True, null=True)

    response_body = models.TextField(blank=True, null=True)
    response_content_type = models.CharField(choices=CONTENT_TYPE_LIST, max_length=30, default=DEFAULT_CONTENT_TYPE)
    response_status_code = models.PositiveSmallIntegerField(choices=HTTP_CODES, default=DEFAULT_HTTP_CODE)

    def __str__(self):
        """
        Object representation as string
        """
        return self.request_path

    class Meta(object):
        """
        Model meta settings
        """
        unique_together = ("request_path", "api")

    def log(self):
        """
        Create log entry
        """
        obj = APIRequest(
            api_handler=self,

            request_path=self.request_path,
            request_method=self.request_method,
            request_body=self.request_body,

            response_body=self.response_body,
            response_content_type=self.response_content_type,
            response_status_code=self.response_status_code,
        )
        obj.save()


class APIRequest(models.Model):
    """
    Logged request details
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_handler = models.ForeignKey("my_fake_api.APIHandler", on_delete=models.CASCADE)

    request_path = models.CharField(max_length=3000)
    request_method = models.CharField(choices=HTTP_METHODS, max_length=10, default=DEFAULT_HTTP_METHOD)
    request_body = models.TextField(blank=True, null=True)
    request_headers = models.TextField(blank=True, null=True)

    response_body = models.TextField(blank=True, null=True)
    response_content_type = models.CharField(choices=CONTENT_TYPE_LIST, max_length=30, default=DEFAULT_CONTENT_TYPE)
    response_status_code = models.PositiveSmallIntegerField(choices=HTTP_CODES, default=DEFAULT_HTTP_CODE)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Object representation as string
        """
        return "{} @ {}".format(self.request_path, self.created)

    class Meta(object):
        ordering = ('-pk', )
