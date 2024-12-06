from requests import PreparedRequest, Response


class SessionItem(object):
    def __init__(self):
        pass


class SessionRequestResponse(SessionItem):
    def __init__(self, request: PreparedRequest, response: Response):
        super().__init__()
        self.request = request
        self.response = response


class SessionSection(SessionItem):
    def __init__(self, title, description=None):
        super().__init__()
        self.title = title
        self.description = description


class SessionComment(SessionItem):
    def __init__(self, comment):
        super().__init__()
        self.comment = comment
