from typing import TypedDict, Literal
import grpc
from grpc import AuthMetadataContext, AuthMetadataPluginCallback

class Options(TypedDict, total=False): 
    transport_type: Literal["secure", "insecure"]

class ApiKeyAuthMetadataPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(
        self, context: AuthMetadataContext, callback: AuthMetadataPluginCallback
    ):
        # Add the API key to the metadata
        callback((("x-api-key", self.api_key),), None)


class ThirdwaveClientBase:
    def __init__(self, api_key: str, options: Options):
        self.endpoint = "api.thirdwavelabs.com/grpc:443"
        self.api_key = api_key
        self.channel = None
        self.transport_type = options.get("transport_type", "secure")
        self.wallet = None  # Initialize wallet as None

    def _create_channel(self):
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

            return grpc.secure_channel(self.endpoint, composite_credentials)
        elif self.transport_type == "insecure":
            return grpc.insecure_channel(self.endpoint)
        else:
            raise ValueError("Unsupported transport type. Use 'secure' or 'insecure'.")
