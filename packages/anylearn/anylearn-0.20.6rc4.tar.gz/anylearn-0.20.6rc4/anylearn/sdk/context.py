from anylearn.sdk.utils import DEFAULT_ANYLEARN_HOST


class Context:
    def __init__(self, host: str = DEFAULT_ANYLEARN_HOST):
        self.host = host.rstrip("/")


__context__: Context = Context()


def get_context() -> Context:
    return __context__


def get_base_url() -> str:
    return f"{__context__.host}/api"


def init(host: str = DEFAULT_ANYLEARN_HOST) -> Context:
    global __context__
    __context__ = Context(host=host)
    return __context__
