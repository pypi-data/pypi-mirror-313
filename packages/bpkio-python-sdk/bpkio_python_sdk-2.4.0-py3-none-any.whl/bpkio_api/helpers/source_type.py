import media_muncher.handlers as handlers
from bpkio_api.exceptions import BroadpeakIoHelperError
from bpkio_api.models.Sources import SourceType


class SourceTypeDetector:
    @staticmethod
    def determine_source_type(url, headers=None) -> SourceType:
        handler = handlers.factory.create_handler(url, explicit_headers=headers)

        match handler:
            case handlers.HLSHandler() | handlers.DASHHandler():
                if handler.is_live():
                    return SourceType.LIVE
                else:
                    return SourceType.ASSET

            case handlers.JPEGHandler() | handlers.PNGHandler() | handlers.MP4Handler():
                return SourceType.SLATE

            case handlers.VASTHandler() | handlers.VMAPHandler():
                return SourceType.AD_SERVER

            case _:
                raise BroadpeakIoHelperError(
                    message=f"Unsupported document type for source at {url}",
                    original_message=None,
                )
