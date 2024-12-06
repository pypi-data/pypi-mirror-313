from requests import Response


class MockResponse(Response):
    def __init__(self, status_code, data = None):
        self.status_code = status_code

        self.return_data = data

    def json(
        self,
        *,
        cls = ...,
        object_hook = ...,
        parse_float = ...,
        parse_int = ...,
        parse_constant = ...,
        object_pairs_hook = ...,
        **kwds,
    ):
        return self.return_data