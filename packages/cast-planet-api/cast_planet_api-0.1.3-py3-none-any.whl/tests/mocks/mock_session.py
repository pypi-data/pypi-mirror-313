from requests import Session


class MockSession(Session):
    get_called = False
    post_called = False
    delete_called = False
    put_called = False

    def get(self, url, **kwargs):
        self.get_called = True

    def post(self, url, **kwargs):
        self.post_called = True

    def put(self, url, **kwargs):
        self.put_called = True

    def delete(self, url, **kwargs):
        self.deleted_called = True
