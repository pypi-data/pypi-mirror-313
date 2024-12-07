"""Registry for prompt templates."""

from __future__ import annotations

from types import UnionType
from typing import TYPE_CHECKING, Any

from llmling.completions.protocols import CompletionProvider
from llmling.core import exceptions
from llmling.core.baseregistry import BaseRegistry
from llmling.core.log import get_logger
from llmling.prompts.models import (
    BasePrompt,
    DynamicPrompt,
    ExtendedPromptArgument,
    FilePrompt,
    StaticPrompt,
)


logger = get_logger(__name__)


if TYPE_CHECKING:
    from collections.abc import Callable


class PromptRegistry(BaseRegistry[str, BasePrompt], CompletionProvider):
    """Registry for prompt templates."""

    @property
    def _error_class(self) -> type[exceptions.LLMLingError]:
        return exceptions.LLMLingError

    def register(self, key: str, item: BasePrompt, replace: bool = False) -> None:
        """Register prompt with its key as name."""
        # Create copy with name set
        item = item.model_copy(update={"name": key})
        super().register(key, item, replace)

    def _validate_item(self, item: Any) -> BasePrompt:
        """Validate and convert items to BasePrompt instances."""
        match item:
            case BasePrompt():
                return item
            case dict():
                if "type" not in item:
                    msg = "Missing prompt type in configuration"
                    raise ValueError(msg)
                match item["type"]:
                    case "text":
                        return StaticPrompt.model_validate(item)
                    case "function":
                        return DynamicPrompt.model_validate(item)
                    case "file":
                        return FilePrompt.model_validate(item)
                msg = f"Unknown prompt type: {item['type']}"
                raise ValueError(msg)
            case _:
                msg = f"Invalid prompt type: {type(item)}"
                raise exceptions.LLMLingError(msg)

    def register_function(
        self,
        fn: Callable[..., Any] | str,
        name: str | None = None,
        *,
        replace: bool = False,
    ) -> None:
        """Register a function as a prompt."""
        prompt = DynamicPrompt.from_callable(fn, name_override=name)
        assert prompt.name
        self.register(prompt.name, prompt, replace=replace)

    async def get_completions(
        self,
        current_value: str,
        argument_name: str | None = None,
        **options: Any,
    ) -> list[str]:
        """Get completions for a prompt argument."""
        try:
            prompt_name = options.get("prompt_name")
            if not prompt_name or not argument_name:
                return []

            prompt = self[prompt_name]
            arg = next(
                (a for a in prompt.arguments if a.name == argument_name),
                None,
            )
            if not arg:
                return []

            completions: list[str] = []

            # 1. Try custom completion function
            if arg.completion_function:
                try:
                    if items := arg.completion_function(current_value):
                        completions.extend(str(item) for item in items)
                except Exception:
                    logger.exception("Custom completion failed")

            # 2. Add type-based completions
            if type_completions := self._get_type_completions(arg, current_value):
                completions.extend(str(val) for val in type_completions)

            # 3. Add description-based suggestions
            if desc_completions := self._get_description_completions(arg, current_value):
                completions.extend(str(val) for val in desc_completions)

            # 4. Add default if no current value
            if not current_value and arg.default is not None:
                completions.append(str(arg.default))

            # Filter by current value if provided
            if current_value:
                current_lower = current_value.lower()
                completions = [
                    c for c in completions if str(c).lower().startswith(current_lower)
                ]

            # Deduplicate while preserving order
            seen = set()
            return [x for x in completions if not (x in seen or seen.add(x))]  # type: ignore

        except Exception:
            logger.exception("Completion failed")
            return []

    def _get_type_completions(
        self,
        arg: ExtendedPromptArgument,
        current_value: str,
    ) -> list[str]:
        """Get completions based on argument type."""
        from typing import Literal, Union, get_args, get_origin

        type_hint = arg.type_hint
        if not type_hint:
            return []

        # Handle Literal types directly
        if get_origin(type_hint) is Literal:
            return [str(val) for val in get_args(type_hint)]

        # Handle Union/Optional types
        if get_origin(type_hint) in (Union, UnionType):
            args = get_args(type_hint)
            # If one of the args is None, process the other type
            if len(args) == 2 and type(None) in args:  # noqa: PLR2004
                other_type = next(arg for arg in args if arg is not type(None))
                # Process the non-None type directly
                return self._get_type_completions(
                    ExtendedPromptArgument(
                        name=arg.name, type_hint=other_type, description=arg.description
                    ),
                    current_value,
                )

        # Handle bool
        if type_hint is bool:
            return ["true", "false"]

        return []

    def _get_description_completions(
        self,
        arg: ExtendedPromptArgument,
        current_value: str,
    ) -> list[str]:
        """Get completions from argument description."""
        if not arg.description or "one of:" not in arg.description:
            return []

        try:
            options_part = arg.description.split("one of:", 1)[1]
            # Clean up options properly
            options = [opt.strip().rstrip(")") for opt in options_part.split(",")]
            return [opt for opt in options if opt]  # Remove empty strings
        except IndexError:
            return []
