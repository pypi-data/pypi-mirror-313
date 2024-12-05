import json
from dataclasses import dataclass, field
from typing import Any

from pricecypher.encoders import PriceCypherJsonEncoder


@dataclass(frozen=True)
class Response:
    """
    Response to be (parsed and) returned after handling an event.
    NB: Although the fields are heavily inspired by HTTP, it is not necessarily limited to generate HTTP responses only.
    """
    status_code: int = 200
    body: Any = None
    headers: dict[str, str] = field(default_factory=lambda: {})
    extra: dict[str, Any] = field(default_factory=lambda: {})

    def to_dict(self, to_json=False) -> dict:
        """
        Converts the response object to a dictionary.
        :param to_json: If `True`, the returned `body` and `extra` fields are serialized into JSON strings.
        """
        headers = self.headers
        body = self.body
        extra = self.extra

        if to_json:
            headers = {'Content-Type': 'application/json', **headers}
            body = json.dumps(body, cls=PriceCypherJsonEncoder)
            extra = json.dumps(extra, cls=PriceCypherJsonEncoder)

        return {
            'statusCode': self.status_code,
            'isBase64Encoded': False,
            'headers': headers,
            'body': body,
            'extra': extra
        }
