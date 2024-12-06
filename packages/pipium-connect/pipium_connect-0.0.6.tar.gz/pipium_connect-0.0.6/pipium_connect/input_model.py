from typing import Any, List, Optional
from pipium_connect.previous_value_model import PreviousValue


class Input:
    """Input to the model."""

    id: str
    """Input ID."""

    binary: bytes
    """Input value as binary data."""

    text: str
    """Input value as text."""

    mime_type: str
    """Input MIME type."""

    user_id: str
    """User ID."""

    local_model_id: str
    """Local model ID."""

    pipe_id: str
    """Pipe ID."""

    model_id: str
    """Model ID."""

    result_id: str
    """Result ID."""

    layer_id: str
    """Layer ID."""

    config: dict
    """Input configuration from the model JSON Schema."""

    previous_values: List[PreviousValue]
    """Previous values."""

    def __init__(
        self,
        id: str,
        binary: bytes,
        mime_type: str,
        user_id: str,
        local_model_id: str,
        pipe_id: str,
        model_id: str,
        result_id: str,
        layer_id: str,
        config: Any,
        text: str,
        previous_values: Optional[List[PreviousValue]] = None,
    ):
        """Initialize an Input object.

        Args:
            id: Input ID.
            binary: Input value as binary data.
            mime_type: Input MIME type.
            user_id: User ID.
            local_model_id: Model model ID.
            pipe_id: Pipe ID.
            model_id: Model ID.
            result_id: Result ID.
            layer_id: Layer ID.
            config: Input configuration from the model JSON Schema.
            text: Input value as text.
            previous_values: Previous values for this result_id."""

        self.id = id
        self.binary = binary
        self.mime_type = mime_type
        self.user_id = user_id
        self.local_model_id = local_model_id
        self.pipe_id = pipe_id
        self.model_id = model_id
        self.result_id = result_id
        self.layer_id = layer_id
        self.config = config
        self.text = text
        self.previous_values = previous_values
