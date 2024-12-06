from collections.abc import Mapping
from typing import (
    Any,
)

from click import (
    Command,
    Context,
    Option,
    UsageError,
)


class RequiredAnyCommand(Command):
    def __init__(self, *args: Any, required_any: list[str], **kwargs: Any) -> None:
        self.required_any = required_any or []
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: Context) -> Any:
        if self.required_any:
            if not any(ctx.params.get(opt) for opt in self.required_any):
                required_opts = ", ".join(
                    next(
                        (p.opts[0] for p in ctx.command.params if p.name == opt),
                        opt,
                    )
                    for opt in self.required_any
                )
                raise UsageError(
                    f"You must provide at least one of the following options: {required_opts}.",
                )
        return super().invoke(ctx)


class MutuallyExclusiveOption(Option):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        help_msg = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs["help"] = help_msg + (
                f" NOTE: This argument is mutually exclusive with arguments: [{ex_str}]."
            )
        super().__init__(*args, **kwargs)

    def handle_parse_result(
        self,
        ctx: Context,
        opts: Mapping[str, Any],
        args: list[str],
    ) -> tuple[Any, list[str]]:
        command_name = self.opts[0] if self.opts else self.name
        mutually_exclusive_names = set(
            next((p.opts[0] for p in ctx.command.params if p.name == opt), opt)
            for opt in self.mutually_exclusive
        )
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                f"Illegal usage: `{command_name}` is mutually exclusive with "
                f"arguments `{', '.join(mutually_exclusive_names)}`.",
            )

        return super().handle_parse_result(ctx, opts, args)
