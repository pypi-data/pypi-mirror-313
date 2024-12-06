from datetime import datetime
from typing import Callable


class PreviousValue:
    """A previous value for the current run."""

    uri: str
    """URI of the previous value used to download it."""

    description: str
    """Description of the previous value."""

    date: datetime
    """Date the previous value was created."""

    binary: Callable[[bytes], None]
    """Gets the binary value of the previous value."""

    json: Callable[[str], None]
    """Gets the JSON value of the previous value."""

    text: Callable[[str], None]
    """Gets the text value of the previous value."""

    def __init__(
        self,
        uri: str,
        description: str,
        date: datetime,
        binary: Callable[[bytes], None],
        json: Callable[[str], None],
        text: Callable[[str], None],
    ):
        """Initialize a PreviousValue object.

        Args:
            uri: URI of the previous value.
            description: Description of the previous value.
            date: Date the previous value was created.
            binary: Gets the binary value of the previous value.
            json: Gets the JSON value of the previous value.
            text: Gets the text value of the previous value."""

        self.uri = uri
        self.description = description
        self.date = date
        self.binary = binary
        self.json = json
        self.text = text
