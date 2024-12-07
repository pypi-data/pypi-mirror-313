from typing import Optional, Dict

import aiohttp
from aiohttp import FormData

from .model import Response


async def get_json(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as response:
            response_json = await response.json()
            if response.ok:
                return Response(result_data=response_json)
            return Response(error=response_json, success=False)


async def post_json(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, params=params) as response:
            response_json = await response.json()
            if response.ok:
                return Response(result_data=response_json)
            return Response(error=response_json, success=False)


async def get_bytes(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None,
                    post_data: FormData = None) -> Response:
    async with aiohttp.ClientSession(headers=headers) as session:

        if not post_data:
            async with session.get(url, params=params) as response:
                response_data = await response.read()
                if response.status == 200:
                    return Response(result_data=response_data)
                return Response(error=(await response.json()), success=False)

        async with session.post(url, params=params, data=post_data) as response:
            response_data = await response.read()
            if response.status == 200:
                return Response(result_data=response_data)
            return Response(error=(await response.json()), success=False)
