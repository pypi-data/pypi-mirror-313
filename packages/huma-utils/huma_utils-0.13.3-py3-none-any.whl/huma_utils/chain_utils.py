from __future__ import annotations

import enum


class UnsupportedChainException(Exception):
    def __init__(self, chain_id: str | int) -> None:
        super().__init__()
        self.message = f"Chain ID {chain_id} not supported"

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class Chain(enum.StrEnum):
    ETHEREUM = enum.auto()
    SEPOLIA = enum.auto()
    POLYGON = enum.auto()
    MUMBAI = enum.auto()
    CELO = enum.auto()
    ALFAJORES = enum.auto()
    SCROLL = enum.auto()
    SCROLL_SEPOLIA = enum.auto()
    BASE = enum.auto()
    BASE_SEPOLIA = enum.auto()
    SOLANA = enum.auto()
    SOLANA_DEVNET = enum.auto()
    STELLAR = enum.auto()
    STELLAR_TESTNET = enum.auto()

    def is_testnet(self) -> bool:
        return self in (  # type: ignore[comparison-overlap]
            self.SEPOLIA,
            self.MUMBAI,
            self.ALFAJORES,
            self.SCROLL_SEPOLIA,
            self.BASE_SEPOLIA,
            self.SOLANA_DEVNET,
            self.STELLAR_TESTNET,
        )


CHAIN_ID_BY_NAME = {
    Chain.ETHEREUM: 1,
    Chain.SEPOLIA: 11155111,
    Chain.POLYGON: 137,
    Chain.MUMBAI: 80001,
    Chain.CELO: 42220,
    Chain.ALFAJORES: 44787,
    Chain.SCROLL: 534352,
    Chain.SCROLL_SEPOLIA: 534351,
    Chain.BASE: 8453,
    Chain.BASE_SEPOLIA: 84532,
    Chain.SOLANA: 900,
    Chain.SOLANA_DEVNET: 901,
    Chain.STELLAR: 1500,
    Chain.STELLAR_TESTNET: 1501,
}

CHAIN_NAME_BY_ID = {v: k for k, v in CHAIN_ID_BY_NAME.items()}


def chain_from_id(chain_id: str | int) -> Chain:
    try:
        return CHAIN_NAME_BY_ID[int(chain_id)]
    except KeyError as e:
        raise UnsupportedChainException(chain_id) from e
