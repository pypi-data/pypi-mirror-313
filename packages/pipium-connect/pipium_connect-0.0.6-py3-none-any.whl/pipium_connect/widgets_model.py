from typing import List, Literal, Optional


InputWidgetId = Literal[
    "camera",
    "code",
    "css",
    "csv",
    "file",
    "form",
    "html",
    "java",
    "javascript",
    "json",
    "markdown",
    "microphone",
    "python",
    "textarea",
    "typescript",
    "xml",
    "yaml",
]

OutputWidgetId = Literal["audio", "chat", "file", "image", "svg", "video"]


class Widgets:
    """UI components for inputs and outputs."""

    inputs: Optional[List[InputWidgetId]]
    """Input UI components."""

    outputs: Optional[List[OutputWidgetId]]
    """Output UI components."""

    def __init__(
        self,
        inputs: Optional[List[InputWidgetId]] = None,
        outputs: Optional[List[OutputWidgetId]] = None,
    ):
        """Initialize a Widgets object.

        Args:
            inputs: Input UI components.
            outputs: Output UI components."""

        self.inputs = inputs
        self.outputs = outputs

    def asdict(self):
        return {
            "inputs": self.inputs,
            "outputs": self.outputs,
        }
