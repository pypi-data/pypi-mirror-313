import dataclasses
import functools
from typing import Any, Callable, Optional, TypedDict, Union


@dataclasses.dataclass
class CommandParameter:
    name: str
    type: str
    description: str
    required: bool

    def __str__(self):
        return f"Parameter: '{self.name} '(Required: {self.required}) - {self.description}"

    def __repr__(self):
        return f"Parameter: '{self.name}' (Required: {self.required}) - {self.description}"

    def __dict__(self):
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required,
        }


class Command:
    def __init__(
            self,
            name: str,
            description: str,
            method: Callable[..., Any],
            parameters: list[CommandParameter],
            enabled: Union[bool, Callable[..., bool]] = True,
            disabled_reason: Optional[str] = None,
    ):
        self.name = name
        self.description = description
        self.method = method
        self.parameters = parameters
        self.enabled = enabled
        self.disabled_reason = disabled_reason

    def __dict__(self) -> dict:
        """Convert Command to a JSON-serializable dictionary."""
        return {
            'name': self.name,
            'description': self.description,
            'parameters': {p.name: p.__dict__() for p in self.parameters},
            'enabled': self.enabled if not callable(self.enabled) else True,
            'disabled_reason': self.disabled_reason
        }

    def __call__(self, *args, **kwargs) -> Any:
        if hasattr(kwargs, "config") and callable(self.enabled):
            self.enabled = self.enabled(kwargs["config"])
        if not self.enabled:
            if self.disabled_reason:
                return f"Command '{self.name}' is disabled: {self.disabled_reason}"
            return f"Command '{self.name}' is disabled"
        return self.method(*args, **kwargs)

    def __str__(self) -> str:
        params = [
            f"{param.name}: {param.type if param.required else f'Optional[{param.type}]'} - {param.description}"
            for param in self.parameters
        ]
        return f"{self.name}({', '.join(params)}) -> {self.description}"


class CommandParameterSpec(TypedDict):
    type: str
    description: str
    required: bool

    def __str__(self):
        return f"Parameter: {self.type} (Required: {self.required}) - {self.description}"

    def __repr__(self):
        return f"Parameter: {self.type} (Required: {self.required}) - {self.description}"

    def __dict__(self):
        return {
            "type": self.type,
            "description": self.description,
            "required": self.required,
        }


def command(
        name: str,
        description: str,
        parameters: Optional[dict[str, CommandParameterSpec]] = None,
        enabled: Union[bool, Callable[..., bool]] = True,
        disabled_reason: Optional[str] = None,
        **kwargs
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Command:
        if parameters is not None:
            typed_parameters = [
                CommandParameter(
                    name=param_name,
                    description=parameter.get("description"),
                    type=parameter.get("type", "string"),
                    required=parameter.get("required", False),
                )
                for param_name, parameter in parameters.items()
            ]
        else:
            typed_parameters = []
        cmd = Command(
            name=name,
            description=description,
            method=func,
            parameters=typed_parameters,
            enabled=enabled,
            disabled_reason=disabled_reason,
        )

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        wrapper.command = cmd

        setattr(wrapper, "command", cmd)

        return wrapper

    return decorator
