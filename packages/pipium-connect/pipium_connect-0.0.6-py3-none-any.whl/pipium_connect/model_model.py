from typing import Any, Callable, Dict, List, Literal, Optional, Union
from pipium_connect.input_model import Input
from pipium_connect.observer_model import Observer
from pipium_connect.output_model import Output
from pipium_connect.rate_limit_model import RateLimit
from pipium_connect.types_model import Types
from pipium_connect.widget_config_model import WidgetConfig
from pipium_connect.widgets_model import Widgets

Access = Literal["private", "public"]


class Model:
    """A Pipium model, containing run functions and configuration."""

    name: str
    """Model name."""

    types: Types
    """Input and output MIME types."""

    invited_user_ids: Optional[List[str]]
    """Invited user IDs that are allowed to run the model."""

    access: Optional[Access]
    """Model access control.
    - Public models are accessible by anyone.
    - Private models are only accessible by the owner and invited users."""

    schema: Optional[dict]
    """JSON schema that validates config and generates a form."""

    rate_limit: Optional[RateLimit]
    """Rate limit configuration."""

    widgets: Optional[Widgets]
    """UI components for inputs and outputs. If unspecified, they are inferred the model MIME types."""

    widget_config: Optional[WidgetConfig]
    """UI component configurations."""

    run_async: Optional[Callable[[Input, Observer], None]]
    """Run function that emits values, errors and completion notifications."""

    run_sync: Optional[
        Callable[
            [Input],
            Union[Output, list[Output]],
        ]
    ]
    """Run function that returns one or more values."""

    def __init__(
        self,
        name: str,
        types: Types,
        run_sync: Optional[
            Callable[
                [Input],
                Union[Output, list[Output]],
            ]
        ] = None,
        run_async: Optional[Callable[[Input, Observer], None]] = None,
        invited_user_ids: Optional[List[str]] = None,
        access: Optional[Access] = None,
        schema: Optional[dict] = None,
        description: Optional[str] = None,
        rate_limit: Optional[RateLimit] = None,
        widgets: Optional[Widgets] = None,
        widget_config: Optional[WidgetConfig] = None,
    ):
        """Initialize a Model object.

        Args:
            name: Model name.
            types: Input and output MIME types.
            run_sync: Run function that returns one or more values.
            run_async: Run function that emits values, errors and completion notifications.
            invited_user_ids: Invited user IDs that are allowed to run the model.
            access: Model access control. Public models are accessible by anyone. Private models are only accessible by the owner and invited users.
            schema: JSON schema that validates config and generates a form.
            description: Model description.
            rate_limit: Rate limit configuration.
            widgets: UI components for inputs and outputs. If unspecified, they are inferred the model MIME types.
            widget_config: UI component configurations.
        """

        self.name = name
        self.types = types
        self.invited_user_ids = invited_user_ids
        self.access = access
        self.schema = schema
        self.description = description
        self.rate_limit = rate_limit
        self.widget_config = widget_config
        self.widgets = widgets
        self.run_sync = run_sync
        self.run_async = run_async

    def asdict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "types": self.types.asdict() if self.types else None,
            "invited_user_ids": self.invited_user_ids,
            "access": self.access,
            "schema": self.schema,
            "description": self.description,
            "rate_limit": self.rate_limit.asdict() if self.rate_limit else None,
            "widgets": self.widgets.asdict() if self.widgets else None,
            "widget_config": (
                self.widget_config.asdict() if self.widget_config else None
            ),
        }


Models = Dict[str, Model]
"""A dictionary of `Model` objects, indexed by their ID."""
