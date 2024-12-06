from .chat.client import AsyncChatAPI, ChatAPI
from .constants import PRODUCTION_BASE_URL
from .features.client import AsyncFeaturesAPI, FeaturesAPI
from .variants.client import AsyncVariantsAPI, VariantsAPI


class AsyncClient:
    """Asyncio compatible client for interacting with the Goodfire API.

    Attributes:
        features (FeaturesAPI): Interface for features operations
        chat (ChatAPI): Interface for chat operations
        variants (VariantsAPI): Interface for variants operations
    """

    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        """Initialize the client with an API key and base URL."""
        self.features = AsyncFeaturesAPI(api_key, base_url=base_url)
        self.chat = AsyncChatAPI(api_key, base_url=base_url)
        self.variants = AsyncVariantsAPI(api_key, base_url=base_url)


class Client:
    """Client for interacting with the Goodfire API.

    Attributes:
        features (FeaturesAPI): Interface for features operations
        chat (ChatAPI): Interface for chat operations
        variants (VariantsAPI): Interface for variants operations
    """

    def __init__(self, api_key: str, base_url: str = PRODUCTION_BASE_URL):
        """Initialize the client with an API key and base URL."""
        self.features = FeaturesAPI(api_key, base_url=base_url)
        self.chat = ChatAPI(api_key, base_url=base_url)
        self.variants = VariantsAPI(api_key, base_url=base_url)
