from typing import Any

import httpx
import orjson


async def post_request(
    base_url: str,
    endpoint: str,
    data: dict[str, Any] | str,
    additional_headers: dict[str, str] | None = None,
    timeout: int = 5,
) -> httpx.Response:
    content: str | bytes = data if isinstance(data, str) else orjson.dumps(data)
    headers = {
        "Content-Type": "application/json",
    }
    if additional_headers is not None:
        headers = {**headers, **additional_headers}
    async with httpx.AsyncClient(base_url=base_url) as client:
        return await client.post(
            url=endpoint,
            headers=headers,
            content=content,
            timeout=timeout,
        )
