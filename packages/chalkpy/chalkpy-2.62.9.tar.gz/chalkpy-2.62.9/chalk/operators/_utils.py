import traceback
from typing import Callable, Optional, Sequence, Union

from chalk import DataFrame, Features, StaticOperator
from chalk.client import ChalkError, ChalkException, ErrorCode, ErrorCodeCategory
from chalk.features.feature_field import Feature


class _GetStaticOperatorError(Exception):
    underlying_error: ChalkError

    def __init__(self, resolver_fqn: str, message: str, underlying_exception: Optional[Exception]):
        super().__init__(f"Failed to get a static operator from the resolver '{resolver_fqn}': {message}")

        def get_stacktrace(exc: Exception):
            try:
                return "".join(traceback.format_exception(exc))
            except TypeError:
                return "".join(traceback.format_exception(type(exc), exc, None))

        self.underlying_error = ChalkError(
            code=ErrorCode.RESOLVER_FAILED if underlying_exception else ErrorCode.VALIDATION_FAILED,
            category=ErrorCodeCategory.REQUEST,
            message=message,
            resolver=resolver_fqn,
            exception=ChalkException(
                kind=type(underlying_exception).__name__,
                message=str(underlying_exception),
                stacktrace=get_stacktrace(underlying_exception),
            )
            if underlying_exception
            else None,
        )


def static_resolver_to_operator(
    fqn: str,
    fn: Callable,
    inputs: Sequence[Union[Feature, type[DataFrame]]],
    output: Optional[type[Features]],
) -> StaticOperator:
    if output is None:
        raise _GetStaticOperatorError(
            resolver_fqn=fqn,
            message="Static resolver must specify a return type",
            underlying_exception=None,
        )

    if len(inputs) > 0 or not (
        len(output.features) == 1 and isinstance(output.features[0], type) and issubclass(output.features[0], DataFrame)
    ):
        raise _GetStaticOperatorError(
            resolver_fqn=fqn,
            message="Static resolver must take no arguments and have exactly one DataFrame output",
            underlying_exception=None,
        )
    try:
        static_operator = fn()
    except Exception as e:
        raise _GetStaticOperatorError(
            resolver_fqn=fqn, message="Resolver failed with an exception", underlying_exception=e
        )
    else:
        if not isinstance(static_operator, StaticOperator):
            raise _GetStaticOperatorError(
                resolver_fqn=fqn,
                message=f"Static resolver must return a StaticOperator, found {type(static_operator).__name__}",
                underlying_exception=None,
            )
        return static_operator
