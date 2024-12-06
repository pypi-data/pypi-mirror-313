from typing import Optional


class RateLimit:
    """Rate limit configuration."""

    limit: int
    """Maximum number of allowed requests."""

    ttl: Optional[int]
    """Milliseconds until a request is removed from the limit count."""

    def __init__(self, limit: int, ttl: Optional[int] = None):
        """Initialize a RateLimit object.

        Args:
            limit: Maximum number of allowed requests.
            ttl: Milliseconds until a request is removed from the limit count."""

        self.limit = limit
        self.ttl = ttl

    def asdict(self):
        return {
            "limit": self.limit,
            "ttl": self.ttl,
        }
