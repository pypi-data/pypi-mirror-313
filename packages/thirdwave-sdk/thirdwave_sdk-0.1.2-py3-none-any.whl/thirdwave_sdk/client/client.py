import grpc
from thirdwave_sdk.client.base import ThirdwaveClientBase, ApiKeyAuthMetadataPlugin
from thirdwave_sdk.services.evm_wallet_service import WalletService
from thirdwave_sdk.utils.get_http_user_agent import get_http_user_agent


class ThirdwaveClient(ThirdwaveClientBase):
    def initialize(self):
        self.channel = self._create_channel()
        self.http_user_agent = get_http_user_agent()
        
        # Initialize services after the channel is set up
        self.wallet = WalletService(self.channel, self.api_key, self.http_user_agent)

    def close(self):
        if self.channel:
            self.channel.close()


class ThirdwaveAsyncClient(ThirdwaveClientBase):
    async def initialize(self):
        if self.transport_type == "secure":
            # Create SSL credentials
            ssl_credentials = grpc.ssl_channel_credentials()

            # Create call credentials using the API key
            auth_plugin = ApiKeyAuthMetadataPlugin(self.api_key)
            call_credentials = grpc.metadata_call_credentials(auth_plugin)

            # Combine SSL and call credentials
            composite_credentials = grpc.composite_channel_credentials(
                ssl_credentials, call_credentials
            )

            self.channel = grpc.aio.secure_channel(self.endpoint, composite_credentials)
        elif self.transport_type == "insecure":
            self.channel = grpc.aio.insecure_channel(self.endpoint)
        else:
            raise ValueError("Unsupported transport type. Use 'secure' or 'insecure'.")

        self.http_user_agent = get_http_user_agent()
        # Initialize services after the channel is set up
        self.wallet = WalletService(self.channel, self.api_key, self.http_user_agent)

    async def close(self):
        if self.channel:
            await self.channel.close()
