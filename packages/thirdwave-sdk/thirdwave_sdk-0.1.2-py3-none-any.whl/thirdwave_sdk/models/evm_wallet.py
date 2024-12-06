from datetime import datetime
from typing import List, Optional
from thirdwave_sdk.utils.eth_utils import evm_from_bytes
from enum import Enum
from dataclasses import dataclass


class Currency(Enum):
    CURRENCY_UNSPECIFIED = 0
    CURRENCY_USD = 1

    def __str__(self):
        return self.name


class BlockchainName(Enum):
    UNSPECIFIED = 0
    ETHEREUM = 1
    BINANCE = 2
    POLYGON = 3
    ARBITRUM = 4
    BASE = 5

    def __str__(self):
        return self.name
    
class TransactionPatternName(Enum):
    UNSPECIFIED = 0
    CONTINUOUS = 1
    HIGH_VELOCITY = 2
    SUSPICIOUS_WALLET_NETWORK = 3
    TIMED = 4
    
    def __str__(self):
        return self.name


@dataclass
class EvmTransaction:
    _hash: bytes
    _blockchain: BlockchainName
    timestamp: datetime

    @property
    def hash(self) -> str:
        return str(self._hash.hex())

    @property
    def blockchain(self) -> str:
        return self._blockchain.name

    def __repr__(self):
        return f"EvmTransaction(hash={self.hash}, blockchain={self.blockchain}, timestamp={self.timestamp})"

    def __str__(self):
        return self.__repr__()


@dataclass
class BotBehaviors:
    continuous_engagement: bool
    funding_network: bool
    temporal_activity: bool
    transaction_velocity: bool

    def __repr__(self):
        return (
            f"BotBehaviors(continuous_engagement={self.continuous_engagement}, "
            f"funding_network={self.funding_network}, temporal_activity={self.temporal_activity}, "
            f"transaction_velocity={self.transaction_velocity})"
        )

    def __str__(self):
        return self.__repr__()


@dataclass
class Erc20TokenHolding:
    _blockchain: BlockchainName
    balance: float
    _address: bytes

    @property
    def address(self):
        return evm_from_bytes(self._address)

    @property
    def blockchain(self) -> str:
        return self._blockchain.name

    def __repr__(self):
        return (
            f"Erc20TokenHolding(blockchain={self.blockchain}, balance={self.balance}, "
            f"address={self.address})"
        )

    def __str__(self):
        return self.__repr__()


@dataclass
class NativeTokenHolding:
    blockchain: BlockchainName
    balance: float

    def __repr__(self):
        return (
            f"NativeTokenHolding(blockchain={self.blockchain}, balance={self.balance})"
        )

    def __str__(self):
        return self.__repr__()


@dataclass
class Spend:
    total: float
    games: float

    def __repr__(self):
        return f"Spend(total={self.total}, games={self.games})"

    def __str__(self):
        return self.__repr__()

@dataclass
class TransactionPattern:
    key: TransactionPatternName
    value: bool
    
    def __str__(self):
        return self.__repr__()
    
class EvmWallet:
    def __init__(
        self,
        address: bytes,
        bot_behaviors: BotBehaviors,
        erc20_token_holdings: List[Erc20TokenHolding],
        first_expense_transaction: Optional[EvmTransaction],
        first_funding_transaction: Optional[EvmTransaction],
        hodler_score: int,
        engagement_score: int,
        outbound_transaction_value: float,
        outbound_transaction_count: float,
        transaction_patterns: List[TransactionPattern],
        is_bot: bool,
        native_token_holdings: List[NativeTokenHolding],
        spend: Spend,
        current_balance: float,
        transaction_count: int,
        updated_at: datetime,
        discovered_at: datetime,
        waverank: int,
    ):
        self._address = address
        self._bot_behaviors = bot_behaviors
        self._erc20_token_holdings = erc20_token_holdings
        self._first_expense_transaction = first_expense_transaction
        self._first_funding_transaction = first_funding_transaction
        self._hodler_score = hodler_score
        self._engagement_score = engagement_score
        self._outbound_transaction_value = outbound_transaction_value
        self._outbound_transaction_count = outbound_transaction_count
        self._transaction_patterns = transaction_patterns
        self._is_bot = is_bot
        self._native_token_holdings = native_token_holdings
        self._spend = spend
        self._current_balance = current_balance
        self._transaction_count = transaction_count
        self._updated_at = updated_at
        self._discovered_at = discovered_at
        self._waverank = waverank
    @property
    def address(self):
        return evm_from_bytes(self._address)

    @property
    def active_chains(self):
        return sorted(list(set([
            holding.blockchain for holding in self._erc20_token_holdings if holding.blockchain != BlockchainName.UNSPECIFIED
        ] + [
                holding.blockchain for holding in self._native_token_holdings if holding.blockchain != BlockchainName.UNSPECIFIED
            ])))

    @property
    def bot_behaviors(self):
        return self._bot_behaviors

    @property
    def erc20_token_holdings(self):
        return self._erc20_token_holdings

    @erc20_token_holdings.setter
    def erc20_token_holdings(self, erc20_token_holdings: List[Erc20TokenHolding]):
        self._erc20_token_holdings = erc20_token_holdings

    @property
    def first_expense_transaction(self):
        return self._first_expense_transaction

    @property
    def first_funding_transaction(self):
        return self._first_funding_transaction

    @property
    def hodler_score(self):
        return self._hodler_score
    
    @property
    def engagement_score(self):
        return self._engagement_score
    
    @property
    def outbound_transaction_value(self):
        return self._outbound_transaction_value
    
    @property
    def outbound_transaction_count(self):
        return self._outbound_transaction_count
    
    @property
    def transaction_patterns(self):
        return self._transaction_patterns

    @property
    def is_bot(self):
        return self._is_bot

    @property
    def native_token_holdings(self):
        return self._native_token_holdings

    @property
    def spend(self):
        return self._spend

    @property
    def current_balance(self):
        return self._current_balance

    @property
    def transaction_count(self):
        return self._transaction_count

    @property
    def updated_at(self):
        return self._updated_at

    @property
    def discovered_at(self):
        return self._discovered_at
    
    @property
    def waverank(self):
        return self._waverank

    def __repr__(self):
        return (
            f"EvmWallet(address={self.address}, bot_behaviors={self.bot_behaviors}, "
            f"erc20_token_holdings={self.erc20_token_holdings}, first_expense_transaction={self.first_expense_transaction}, "
            f"first_funding_transaction={self.first_funding_transaction}, hodler_score={self.hodler_score}, is_bot={self.is_bot}, "
            f"native_token_holdings={self.native_token_holdings}, spend={self.spend}, current_balance={self.current_balance}, "
            f"transaction_count={self.transaction_count}, updated_at={self.updated_at}, discovered_at={self.discovered_at},"
            f"waverank={self.waverank})")

    def __str__(self):
        return self.__repr__()


class EvmWalletResponse:
    def __init__(self, wallet: EvmWallet):
        self.wallet = wallet

    @staticmethod
    def from_grpc(response) -> "EvmWalletResponse":
        wallet = EvmWallet(
            address=response.wallet.address,
            bot_behaviors=BotBehaviors(
                response.wallet.bot_behaviors.continuous_engagement,
                response.wallet.bot_behaviors.funding_network,
                response.wallet.bot_behaviors.temporal_activity,
                response.wallet.bot_behaviors.transaction_velocity,
            ),
            erc20_token_holdings=[
                Erc20TokenHolding(
                    holding.blockchain,
                    holding.balance,
                    holding.address,
                )
                for holding in response.wallet.erc20_token_holdings
            ],
            first_expense_transaction=(
                EvmTransaction(
                    response.wallet.first_expense_transaction.hash,
                    response.wallet.first_expense_transaction.blockchain,
                    response.wallet.first_expense_transaction.timestamp.ToDatetime(),
                )
                if response.wallet.HasField("first_expense_transaction")
                else None
            ),
            first_funding_transaction=(
                EvmTransaction(
                    response.wallet.first_funding_transaction.hash,
                    response.wallet.first_funding_transaction.blockchain,
                    response.wallet.first_funding_transaction.timestamp.ToDatetime(),
                )
                if response.wallet.HasField("first_funding_transaction")
                else None
            ),
            hodler_score=response.wallet.hodler_score,
            engagement_score=response.wallet.engagement_score,
            outbound_transaction_value=response.wallet.outbound_transaction_value,
            outbound_transaction_count=response.wallet.outbound_transaction_count,
            transaction_patterns=[
                TransactionPattern(pattern.key, pattern.value)
                for pattern in response.wallet.transaction_patterns
                if pattern.key != TransactionPatternName.UNSPECIFIED
            ],
            is_bot=response.wallet.is_bot,
            native_token_holdings=[
                NativeTokenHolding(
                    holding.blockchain,
                    holding.balance,
                )
                for holding in response.wallet.native_token_holdings
            ],
            spend=Spend(
                response.wallet.spend.total,
                response.wallet.spend.games,
            ),
            current_balance=response.wallet.current_balance,
            transaction_count=response.wallet.transaction_count,
            updated_at=response.wallet.updated_at.ToDatetime(),
            discovered_at=response.wallet.discovered_at.ToDatetime(),
            waverank=response.wallet.waverank,
        )
        return EvmWalletResponse(wallet)

    def __repr__(self):
        return f"EvmWalletResponse(wallet={self.wallet})"

    def __str__(self):
        return self.__repr__()
