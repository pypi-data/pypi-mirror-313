import pickle

from requests import Response

from .curl import CurlExporter
from .markdown import MarkdownExporter
from .postman import PostmanExporter
from .session_items import (SessionComment, SessionItem,
                            SessionRequestResponse, SessionSection)
from .text import TextExporter


class SessionRecorder(object):
    _instance = None

    # singleton pattern
    def __new__(cls, session_file=None):
        if cls._instance is None:
            # print("Creating the session recorder")
            cls._instance = super(SessionRecorder, cls).__new__(cls)
            cls._instance.session_file = session_file
            cls._instance.enabled = True
        return cls._instance

    @staticmethod
    def is_active() -> bool:
        recorder = SessionRecorder()
        return recorder.enabled and recorder.session_file is not None

    def _load_from_pickle(self):
        items = []
        if self.session_file:
            with open(self.session_file, "rb") as f:
                while True:
                    try:
                        items.append(pickle.load(f))
                    except EOFError:
                        break
        return items

    def size(self) -> int:
        return self._count_pickled_objects()

    # @staticmethod
    # def _get_session_file():
    #     session_file = None
    #     session_sentinel = os.path.expanduser("~/.bpkio/session")

    #     # Check if the sentinel file exists.
    #     if os.path.exists(session_sentinel):
    #         # If it does, open it and read the URL to the session file.
    #         with open(session_sentinel, "r") as f:
    #             session_file = f.read()
    #     return session_file

    def _append_to_session(self, item):
        if self.session_file:
            with open(self.session_file, "ab") as f:
                pickle.dump(item, f)

    def _count_pickled_objects(self):
        """Counts the number of picked objects without loading them to memory"""
        count = 0
        if self.session_file:
            try:
                with open(self.session_file, "rb") as f:
                    while True:
                        try:
                            pickle.load(f)
                            count += 1
                        except EOFError:
                            break
            except FileNotFoundError:
                pass
        return count

    @staticmethod
    def record(item):
        recorder = SessionRecorder()
        recorder.add(item)

    def add(self, item):
        if self.is_active():
            if isinstance(item, Response):
                item = SessionRequestResponse(request=item.request, response=item)

            if not isinstance(item, SessionItem):
                raise Exception(f"Invalid item type: {type(item)}")

            self._append_to_session(item)

    def add_section(self, title, description=None):
        self.add(SessionSection(title, description))

    def add_comment(self, comment):
        self.add(SessionComment(comment))

    def export(self, options: dict = dict()):
        if not self.session_file:
            return

        session_id = self.session_file.split("/")[-1]
        session = self._load_from_pickle()

        options["session_id"] = session_id

        format = options.get("format", "text")

        exporter = None
        match format:
            case "text":
                exporter = TextExporter(**options)
            case "markdown":
                exporter = MarkdownExporter(**options)
            case "curl":
                exporter = CurlExporter(**options)
            case "postman":
                exporter = PostmanExporter(**options)
            case _:
                print("Invalid format.")

        if exporter:
            print(exporter.export(session))

    @staticmethod
    def do_not_record(func):
        """Decorator preventing recording of operations in the function"""

        def wrapper(*args, **kwargs):
            session = SessionRecorder()
            session.enabled = False
            result = func(*args, **kwargs)
            session.enabled = True
            return result

        return wrapper
