from typing import Optional


class ConnectOptions:
    """Options for connecting to the Pipium server."""

    server_url: Optional[str]
    """URL of the Pipium server"""

    def __init__(self, server_url: Optional[str] = None):
        """Initialize a ConnectOptions object.

        Args:
            server_url: URL of the Pipium server"""
        self.server_url = server_url
