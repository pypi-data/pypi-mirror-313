from typing import List


class Types:
    """Input and output MIME types."""

    inputs: List[str]
    """Input MIME types. These are the types this model accepts as input."""

    output: str
    """Input MIME types. This is the type this model produces as output."""

    def __init__(self, inputs: List[str], output: str):
        """Initialize a Types object.

        Args:
            inputs: Input MIME types. These are the types this model accepts as input.
            output: Input MIME types. This is the type this model produces as output."""

        self.inputs = inputs
        self.output = output

    def asdict(self):
        return {"inputs": self.inputs, "output": self.output}
