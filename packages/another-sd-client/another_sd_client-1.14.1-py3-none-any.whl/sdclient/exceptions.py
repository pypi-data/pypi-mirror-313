from sdclient.requests import SDRequest


class SDCallError(Exception):
    def __init__(self, message: str):
        super().__init__()
        self._message = message

    def __str__(self) -> str:
        return self._message

    @property
    def message(self) -> str:
        return self._message


class SDParseResponseError(SDCallError):
    pass


class SDRootElementNotFound(SDCallError):
    pass
