from __future__ import annotations

from abc import abstractmethod


class ClientApiBuilder:
    """
    This class is used to build the API for the client.
    Depending on the client, the API is built differently.
    """

    @abstractmethod
    def build_api(self) -> str:
        """
        Build the API for the client.
        """
