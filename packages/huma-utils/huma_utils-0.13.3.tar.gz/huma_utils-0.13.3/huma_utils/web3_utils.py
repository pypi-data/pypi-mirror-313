from __future__ import annotations

import web3

from huma_utils import chain_utils


async def get_w3(chain: chain_utils.Chain, web3_provider_url: str) -> web3.AsyncWeb3:
    w3 = web3.AsyncWeb3(provider=web3.AsyncHTTPProvider(web3_provider_url))
    if await w3.net.version != str(chain_utils.CHAIN_ID_BY_NAME[chain]):  # type: ignore
        raise ValueError(f"Web3 provider is not compatible with chain {chain.name}")
    return w3
