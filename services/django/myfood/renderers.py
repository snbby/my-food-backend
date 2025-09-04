import msgspec
from rest_framework.renderers import BaseRenderer

# Stable key ordering helps apples-to-apples benchmarking diffs
_ENCODER = msgspec.json.Encoder(order="deterministic")  # returns bytes

class MsgspecJSONRenderer(BaseRenderer):
    media_type = "application/json"
    format = "json"
    charset = None  # we return bytes already

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b""
        return _ENCODER.encode(data)