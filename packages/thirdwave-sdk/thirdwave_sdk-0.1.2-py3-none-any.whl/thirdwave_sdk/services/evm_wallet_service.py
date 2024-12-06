from thirdwave_sdk.proto.thirdwave.v1 import evm_wallet_pb2, evm_wallet_pb2_grpc
from thirdwave_sdk.models.evm_wallet import EvmWalletResponse, EvmWallet
from thirdwave_sdk.utils.eth_utils import evm_address_to_bytes
from typing import AsyncGenerator, List, Tuple

Metadata = Tuple[Tuple[str, str], ...]


class WalletService:
    def __init__(self, channel, api_key: str, http_user_agent: str):
        self.channel = channel
        self.api_key = api_key
        self.http_user_agent = http_user_agent
        self.stub = evm_wallet_pb2_grpc.EvmWalletServiceStub(channel)

    async def get_one(self, address: str | bytes) -> EvmWallet:
        request = evm_wallet_pb2.EvmWalletRequest(address=evm_address_to_bytes(address))
        metadata: Metadata = (
            ("x-api-key", self.api_key),
            ("user-agent", self.http_user_agent),)
        response = await self.stub.GetOne(request, metadata=metadata)
        return EvmWalletResponse.from_grpc(response).wallet

    async def get_many(self, addresses: List[str] | List[bytes]) -> AsyncGenerator[EvmWallet, None]:
        metadata: Metadata = (
            ("x-api-key", self.api_key),
            ("user-agent", self.http_user_agent),)

        async def request_generator():
            for address in addresses:
                yield evm_wallet_pb2.EvmWalletRequest(
                    address=evm_address_to_bytes(address)
                )

        async for response in self.stub.GetMany(request_generator(), metadata=metadata):
            yield EvmWalletResponse.from_grpc(response).wallet

    async def add_wallet(self, address: str | bytes, stream):
        request = evm_wallet_pb2.EvmWalletRequest(address=evm_address_to_bytes(address))
        await stream.send_message(request)
