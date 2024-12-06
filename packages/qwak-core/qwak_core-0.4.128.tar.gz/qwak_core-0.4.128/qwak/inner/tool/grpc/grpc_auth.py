import grpc
from qwak.inner.tool.auth import Auth0ClientBase

_SIGNATURE_HEADER_KEY = "authorization"


class Auth0Client(grpc.AuthMetadataPlugin, Auth0ClientBase):
    def __init__(self):
        Auth0ClientBase.__init__(self)

    def __call__(self, context, callback):
        callback(((_SIGNATURE_HEADER_KEY, "Bearer {}".format(self.get_token())),), None)
