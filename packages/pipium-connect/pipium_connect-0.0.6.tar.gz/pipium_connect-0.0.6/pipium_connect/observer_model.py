from typing import Callable
from pipium_connect.output_model import Output


class Observer:
    """An observer contains functions that handle the three possible outcomes of a run:
    - next: the run has produced a value
    - error: the run has produced an error and stopped
    - complete: the run has completed and will not produce any more value."""

    next: Callable[[Output], None]
    """Function that handles values."""

    error: Callable[[str], None]
    """Function that handles errors."""

    complete: Callable[[], None]
    """Function that handles completion."""

    def __init__(
        self,
        next: Callable[[Output], None],
        error: Callable[[str], None],
        complete: Callable[[], None],
    ):
        """Initialize an Observer object.

        Args:
            next: Function that handles values.
            error: Function that handles errors.
            complete: Function that handles completion."""

        self.next = next
        self.error = error
        self.complete = complete
