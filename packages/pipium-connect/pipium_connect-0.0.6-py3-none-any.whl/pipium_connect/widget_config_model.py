from typing import Any, Optional


class AudioWidgetConfig:
    """Audio widget configuration."""

    autoplay: Optional[bool]
    """Whether audio should autoplay."""

    def __init__(self, autoplay: Optional[bool] = None):
        """Initialize an AudioWidgetConfig object.

        Args:
            autoplay: Whether audio should autoplay."""

        self.autoplay = autoplay

    def asdict(self):
        return {"autoplay": self.autoplay}


class FormWidgetConfig:
    """Form widget configuration."""

    schema: dict
    """JSON schema that generates a form."""

    def __init__(self, schema: dict):
        """Initialize a FormWidgetConfig object.

        Args:
            schema: JSON schema that generates a form."""

        self.schema = schema

    def asdict(self):
        return {"schema": self.schema}


class WidgetConfig:
    """UI component configurations."""

    audio: Optional[AudioWidgetConfig]
    """Audio widget configuration."""

    form: Optional[FormWidgetConfig]
    """Form widget configuration."""

    def __init__(
        self,
        audio: Optional[AudioWidgetConfig] = None,
        form: Optional[FormWidgetConfig] = None,
    ):
        """Initialize a WidgetConfig object.

        Args:
            audio: Audio widget configuration.
            form: Form widget configuration."""

        self.audio = audio
        self.form = form

    def asdict(self):
        return {
            "audio": self.audio.asdict() if self.audio else None,
            "form": self.form.asdict() if self.form else None,
        }
