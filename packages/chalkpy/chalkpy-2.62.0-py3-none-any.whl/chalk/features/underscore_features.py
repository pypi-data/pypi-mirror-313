# pyright: reportPrivateUsage = false

from __future__ import annotations

import warnings
from typing import Any, Tuple, Union

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper, unwrap_feature
from chalk.features.filter import Filter
from chalk.features.underscore import (
    SUPPORTED_UNDERSCORE_OPS_BINARY,
    SUPPORTED_UNDERSCORE_OPS_UNARY,
    Underscore,
    UnderscoreAttr,
    UnderscoreCall,
    UnderscoreFunction,
    UnderscoreItem,
    UnderscoreRoot,
)
from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import polars as pl
except ModuleNotFoundError:
    pl = None


SUPPORTED_ARITHMETIC_OPS = {"+", "-", "*", "/", "//", "%", "**"}


def parse_underscore_in_context(exp: Underscore, context: Any, is_pydantic: bool = False) -> Any:
    """
    Parse a (potentially underscore) expression passed in under some "context".
    """
    parsed_exp = _parse_underscore_in_context(
        exp=exp,
        context=context,
        is_pydantic=is_pydantic,
    )
    assert not isinstance(parsed_exp, Underscore)
    return parsed_exp


def _parse_underscore_in_context(exp: Any, context: Any, is_pydantic: bool) -> Any:
    # Features of the dataframe are to be written as a dictionary of the fqn split up mapped to
    # the original features. The dictionary is represented immutably here.
    if not isinstance(exp, Underscore):
        # Recursive call hit non-underscore, deal with later
        return exp

    elif isinstance(exp, UnderscoreRoot):
        return context

    elif isinstance(exp, UnderscoreAttr):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        attr = exp._chalk__attr
        from chalk.features.dataframe import DataFrame

        if isinstance(parent_context, DataFrame) and is_pydantic:
            if attr not in parent_context._underlying.schema:
                warnings.warn(
                    f"Attribute {attr} not found in dataframe schema. Returning None. Found expression {exp}."
                )
                return None

            return attr
        else:
            return getattr(parent_context, attr)

    elif isinstance(exp, UnderscoreItem):
        parent_context = _parse_underscore_in_context(exp=exp._chalk__parent, context=context, is_pydantic=is_pydantic)
        key = exp._chalk__key
        return parent_context[key]

    elif isinstance(exp, UnderscoreCall):
        raise NotImplementedError(
            f"Calls on underscores in DataFrames is currently unsupported. Found expression {exp}"
        )

    elif isinstance(exp, UnderscoreFunction):
        if exp._chalk__function_name in SUPPORTED_UNDERSCORE_OPS_BINARY:
            if len(exp._chalk__args) != 2:
                raise ValueError(
                    f"Binary operation '{exp._chalk__function_name}' requires 2 operands; got {len(exp._chalk__args)} operands: {exp._chalk__args!r}"
                )
            left_val = exp._chalk__args[0]
            if isinstance(left_val, Underscore):
                left = _parse_underscore_in_context(exp=left_val, context=context, is_pydantic=is_pydantic)
            else:
                # The left value might be a literal, like `1` or `"::"` or `None`.
                left = left_val

            right_val = exp._chalk__args[1]
            if isinstance(right_val, Underscore):
                right = _parse_underscore_in_context(exp=right_val, context=context, is_pydantic=is_pydantic)
            else:
                # The right value might be a literal, like `1` or `"::"` or `None`.
                right = right_val

            if exp._chalk__function_name in SUPPORTED_ARITHMETIC_OPS:
                return _eval_arithmetic_expression(left, right, exp._chalk__function_name)
            else:
                return _eval_expression(left, right, exp._chalk__function_name)

        if exp._chalk__function_name in SUPPORTED_UNDERSCORE_OPS_UNARY:
            operand = _parse_underscore_in_context(exp=exp._chalk__args[0], context=context, is_pydantic=is_pydantic)
            return eval(f"{exp._chalk__function_name} operand", globals(), {"operand": operand})

    raise NotImplementedError(f"Unrecognized underscore expression {exp}")


def _unwrap_and_validate_features(left: FeatureWrapper, right: FeatureWrapper) -> Tuple[Feature, Feature]:
    f_left = unwrap_feature(left)
    f_right = unwrap_feature(right)

    if f_left.root_namespace != f_right.root_namespace:
        raise TypeError(
            f"{f_left} and {f_right} belong to different namespaces. Operations can only be performed on features of the same namespace."
        )

    return f_left, f_right


def _eval_expression(left: Union[FeatureWrapper, Filter], right: Any, op: str):
    try:
        if op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "&":
            return left & right
        elif op == "|":
            return left | right
        elif op == "__getitem__":
            assert isinstance(left, FeatureWrapper)
            return left[right]
        elif op == "__getattr__":
            return getattr(left, right)
    except:
        raise NotImplementedError(
            f"Operation {op} not implemented for {type(left).__name__} and {type(right).__name__}"
        )


def _eval_arithmetic_expression(
    left: Union[FeatureWrapper, float, int],
    right: Union[FeatureWrapper, float, int],
    op: str,
):
    if pl is None:
        raise missing_dependency_exception("chalkpy[runtime]")

    if isinstance(left, FeatureWrapper) and isinstance(right, FeatureWrapper):
        # If both are features, ensure they are in the same namespace
        _unwrap_and_validate_features(left, right)

    if isinstance(left, FeatureWrapper):
        left_col = pl.col(str(left))
    else:
        left_col = pl.lit(left)

    if isinstance(right, FeatureWrapper):
        right_col = pl.col(str(right))
    else:
        right_col = pl.lit(right)

    if op == "+":
        return left_col + right_col
    elif op == "-":
        return left_col - right_col
    elif op == "*":
        return left_col * right_col
    elif op == "/":
        return left_col / right_col
    elif op == "//":
        return left_col // right_col
    elif op == "%":
        return left_col % right_col
    elif op == "**":
        return left_col**right_col

    raise NotImplementedError(f"{op} is not implemented")
