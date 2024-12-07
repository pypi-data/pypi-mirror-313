###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
__all__ = ['FileResponse', 'HTMLResponse', 'JSONResponse', 'PlainTextResponse', 'RedirectResponse', 'Response', 'StreamingResponse']
from typing import Any
from starlette.responses import Response, FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse, StreamingResponse

from everysk.core.serialize import dumps


class JSONResponse(Response):
    media_type = 'application/json; charset=UTF-8'

    def render(self, content: Any) -> bytes:
        """
        Serialize the content to JSON format using the dumps function from the core.serialize module.

        Args:
            content (Any): The content to be serialized.
        """
        # with indent=None and separators=(",", ":"), the JSON will be minified
        return dumps(content, indent=None, separators=(",", ":"), protocol='json', use_undefined=True).encode('utf-8')
