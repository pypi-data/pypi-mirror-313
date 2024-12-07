from __future__ import annotations

from enum import Enum
from typing import Any, Literal, Mapping, TypeVar, Union

import pyarrow as pa

from chalk.features._encoding.pyarrow import rich_to_pyarrow
from chalk.features.underscore import Underscore, UnderscoreCast, UnderscoreFunction
from chalk.functions.holidays import DayOfWeek

########################################################################################################################
# String Functions                                                                                                     #
########################################################################################################################


_SUPPORTED_UNDERSCORE_STRING_TO_BYTES = {
    "base64": "string_to_bytes_base64",
    "hex": "string_to_bytes_hex",
    "utf-8": "string_to_bytes_utf8",
}

_SUPPORTED_UNDERSCORE_BYTES_TO_STRING = {
    "base64": "bytes_to_string_base64",
    "hex": "bytes_to_string_hex",
    "utf-8": "bytes_to_string_utf8",
}


def replace(expr: Underscore | Any, old: str, new: str):
    """Replace all occurrences of a substring in a string with another substring.

    Parameters
    ----------
    expr
        The string to replace the substring in.
    old
        The substring to replace.
    new
        The substring to replace the old substring with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalized_name: str = F.replace(_.name, " ", "_")
    """
    return UnderscoreFunction("replace", expr, old, new)


def like(expr: Underscore | Any, pattern: str):
    """
    Evaluates if the string matches the pattern.

    Patterns can contain regular characters as well as wildcards.
    Wildcard characters can be escaped using the single character
    specified for the escape parameter. Matching is case-sensitive.

    Note: The wildcard `%` represents 0, 1 or multiple characters
    and the wildcard `_` represents exactly one character.

    For example, the pattern `John%` will match any string that starts
    with `John`, such as `John`, `JohnDoe`, `JohnSmith`, etc.

    The pattern `John_` will match any string that starts with `John`
    and is followed by exactly one character, such as `JohnD`, `JohnS`, etc.
    but not `John`, `JohnDoe`, `JohnSmith`, etc.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The pattern to check the string against.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    is_john: bool = F.like(_.name, "John%")
    """
    return UnderscoreFunction("like", expr, pattern)


def regexp_replace(expr: Underscore | Any, pattern: str, replacement: str | None = None):
    """
    Replaces every instance of `expr` matched by the regular expression pattern in
    `pattern` with `replacement`. Capturing groups can be referenced in replacement
    using `$1`, `$2`, etc. for a numbered group or `${name}` for a named group.
    A dollar sign (`$`) may be included in the replacement by escaping it with a
    backslash. If a backslash is followed by any character other than
    a digit or another backslash in the replacement, the preceding backslash
    will be ignored.

    If no replacement is provided, the matched pattern will be removed from the string.

    Parameters
    ----------
    expr
        The string to replace the pattern in.
    pattern
        The regular expression pattern to replace.
    replacement
        The string to replace the pattern with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalize_regex: str
    ...    normalized_name: str = F.regexp_replace(_.name, _.normalize_regex, " ")
    """
    if replacement is not None:
        return UnderscoreFunction("regexp_replace", expr, pattern, replacement)
    return UnderscoreFunction("regexp_replace", expr, pattern)


def regexp_like(expr: Underscore | Any, pattern: Underscore | str | Any):
    """
    Evaluates the regular expression pattern and determines if it is contained within string.

    This function is similar to the `like` function, except that the pattern only needs to be
    contained within string, rather than needing to match all the string.
    In other words, this performs a contains operation rather than a match operation.
    You can match the entire string by anchoring the pattern using `^` and `$`.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    is_john: bool = F.regexp_like(_.name, "^John.*$")
    """
    return UnderscoreFunction("regexp_like", expr, pattern)


def regexp_extract(expr: Underscore | Any, pattern: str, group: int):
    """
    Finds the first occurrence of the regular expression pattern in the string and
    returns the capturing group number group.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.
    group
        The number of the capturing group to extract from the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class HiddenNumber:
    ...    id: str
    ...    hidden_number: str = "O0OOO",
    ...    number: str = F.regexp_extract(_.time,  r"([0-9]+)", 1)
    """
    return UnderscoreFunction("regexp_extract", expr, pattern, group)


def regexp_extract_all(expr: Underscore | Any, pattern: str, group: int):
    """
    Finds all occurrences of the regular expression pattern in string and
    returns the capturing group number group.

    Parameters
    ----------
    expr
        The string to check against the pattern.
    pattern
        The regular expression pattern to check the string against.
    group
        The number of the capturing group to extract from the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Time:
    ...    id: str
    ...    time: str = "1y 342d 20h 60m 6s",
    ...    processed_time: list[str] = F.regexp_extract_all(_.time, "([0-9]+)([ydhms])", 2)
    """
    return UnderscoreFunction("regexp_extract_all", expr, pattern, group)


def trim(expr: Underscore | Any):
    """
    Remove leading and trailing whitespace from a string.

    Parameters
    ----------
    expr
        The string to trim.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    trimmed_name: str = F.trim(_.name)
    """
    return UnderscoreFunction("trim", expr)


def starts_with(expr: Underscore | Any, prefix: Underscore | Any):
    """
    Evaluates if the string starts with the specified prefix.

    Parameters
    ----------
    expr
        The string to check against the prefix.
    prefix
        The prefix or feature to check if the string starts with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    is_food: bool = F.starts_with(_.name, "Food")
    """
    return UnderscoreFunction("starts_with", expr, prefix)


def ends_with(expr: Underscore | Any, suffix: Underscore | Any):
    """
    Evaluates if the string ends with the specified suffix.

    Parameters
    ----------
    expr
        The string to check against the suffix.
    suffix
        The suffix or feature to check if the string ends with.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    is_food: bool = F.ends_with(_.name, "Food")
    """
    return UnderscoreFunction("ends_with", expr, suffix)


def substr(expr: Underscore | Any, start: int, length: int | None = None):
    """
    Extract a substring from a string.

    Parameters
    ----------
    expr
        The string to extract the substring from.
    start
        The starting index of the substring (0-indexed).
    length
        The length of the substring. If None, the substring will extend to the end of the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    cat_first_three: str = F.substr(_.category, 0, 3)
    """
    if length is None:
        return UnderscoreFunction("substr", expr, start + 1)
    return UnderscoreFunction("substr", expr, start + 1, length)


def reverse(expr: Underscore | Any):
    """
    Reverse the order of a string.

    Parameters
    ----------
    expr
        The string to reverse.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    reversed_name: str = F.reverse(_.name)
    """
    return UnderscoreFunction("reverse", expr)


def levenshtein_distance(a: Underscore | Any, b: Underscore | Any):
    """
    Compute the Levenshtein distance between two strings.

    Parameters
    ----------
    a
        The first string.
    b
        The second string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    email: str
    ...    name_email_sim: int = F.levenshtein_distance(_.name, _.email)
    """
    return UnderscoreFunction("levenshtein_distance", a, b)


def lower(expr: Underscore | Any):
    """
    Convert a string to lowercase.

    Parameters
    ----------
    expr
        The string to convert to lowercase.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    normalized: str = F.trim(F.lower(_.name))
    """
    return UnderscoreFunction("lower", expr)


def upper(expr: Underscore | Any):
    """
    Convert a string to uppercase.

    Parameters
    ----------
    expr
        The string to convert to uppercase.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    category: str
    ...    normalized: str = F.trim(F.upper(_.category))
    """
    return UnderscoreFunction("upper", expr)


def string_to_bytes(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert a string to bytes using the specified encoding.

    Parameters
    ----------
    expr
        An underscore expression for a feature to a
        string feature that should be converted to bytes.
    encoding
        The encoding to use when converting the string to bytes.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    hashed_name: bytes = F.string_to_bytes(_.name, encoding="utf-8")
    """
    return UnderscoreFunction(_SUPPORTED_UNDERSCORE_STRING_TO_BYTES[encoding], expr)


def bytes_to_string(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert bytes to a string using the specified encoding.

    Parameters
    ----------
    expr
        A bytes feature to convert to a string.
    encoding
        The encoding to use when converting the bytes to a string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    hashed_name: bytes
    ...    decoded_name: str = F.bytes_to_string(_.hashed_name, encoding="utf-8")
    """
    return UnderscoreFunction(_SUPPORTED_UNDERSCORE_BYTES_TO_STRING[encoding], expr)


def split_part(expr: Any, delimiter: str, index: int):
    """
    Splits string by delimiter and returns the index'th element (0-indexed).
    If the index is larger than the number of fields, returns None.

    Parameters
    ----------
    expr:
        The string to split.
    delimiter:
        The delimiter to split the string on.
    index:
        The index of the the split to return.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CSVRow:
    ...    id: str
    ...    data: str
    ...    first_element: str = F.split_part(_.data, delimiter=",", index=0)
    """
    return UnderscoreFunction("split_part", expr, delimiter, index + 1)


def strpos(expr: Any, substring: Any):
    """
    Returns the position of the first occurrence of substring in string.
    Returns -1 if substring is not found.

    Parameters
    ----------
    expr:
        The string to search for the substring in.
    substring:
        The substring to search for in the string.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class CSVRow:"""


########################################################################################################################
# URLs                                                                                                                 #
########################################################################################################################


def url_extract_protocol(expr: Any):
    """
    Extract the protocol from a URL.

    For example, the protocol of `https://www.google.com/cats` is `https`.

    Parameters
    ----------
    expr
        The URL to extract the protocol from.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     protocol: str = F.url_extract_protocol(_.website)
    """
    return UnderscoreFunction("url_extract_protocol", expr)


def url_extract_host(expr: Any):
    """
    Extract the host from a URL.

    For example, the host of `https://www.google.com/cats` is `www.google.com`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     host: str = F.url_extract_host(_.website)
    """
    return UnderscoreFunction("url_extract_host", expr)


def url_extract_path(expr: Any):
    """Extract the path from a URL.

    For example, the host of `https://www.google.com/cats` is `/cats`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Company:
    ...     id: int
    ...     website: str
    ...     path: str = F.url_extract_path(_.website)
    """
    return UnderscoreFunction("url_extract_path", expr)


########################################################################################################################
# Hash functions                                                                                                       #
########################################################################################################################


def spooky_hash_v2_32(expr: Any):
    """
    Compute the SpookyHash V2 32-bit hash of a string.
    This hash function is not cryptographically secure,
    but it is deterministic and fast.

    Parameters
    ----------
    expr
        A string feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    name_hash: bytes = F.spooky_hash_v2_32(
    ...        F.string_to_bytes(_.name, "utf-8")
    ...    )
    """
    return UnderscoreFunction("spooky_hash_v2_32", expr)


def spooky_hash_v2_64(expr: Any):
    """
    Compute the SpookyHash V2 64-bit hash of a string.
    This hash function is not cryptographically secure,
    but it is deterministic and fast.

    Parameters
    ----------
    expr
        A string feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    name: str
    ...    name_hash: bytes = F.spooky_hash_v2_64(
    ...        F.string_to_bytes(_.name, "utf-8")
    ...    )
    """
    return UnderscoreFunction("spooky_hash_v2_64", expr)


def md5(expr: Any):
    """
    Compute the MD5 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    md5_bytes: bytes = F.md5(_.bytes_feature)
    """
    return UnderscoreFunction("md5", expr)


def sha1(expr: Any):
    """
    Compute the SHA-1 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    sha1_bytes: bytes = F.sha1(_.bytes_feature)
    """
    return UnderscoreFunction("sha1", expr)


def sha256(expr: Any):
    """
    Compute the SHA-256 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    sha256_bytes: bytes = F.sha256(_.bytes_feature)
    """
    return UnderscoreFunction("sha256", expr)


def sha512(expr: Any):
    """
    Compute the SHA-512 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    bytes_feature: bytes
    ...    sha512_bytes: bytes = F.sha512(_.bytes_feature)
    """
    return UnderscoreFunction("sha512", expr)


########################################################################################################################
# Misc                                                                                                                 #
########################################################################################################################


def coalesce(*vals: Any):
    """
    Return the first non-null entry

    Parameters
    ----------
    vals
        Expressions to coalesce. They can be a combination of underscores and literals,
        though types must be compatible (ie do not coalesce int and string).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    nickname: str | None
    ...    name: str | None
    ...    name_or_nickname: str = F.coalesce(_.name, _.nickname, "")
    """
    return UnderscoreFunction("coalesce", *vals)


def is_null(expr: Any):
    """
    Check if a value is null.

    Parameters
    ----------
    expr
        The value to check if it is null.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    nickname: str | None
    ...    missing_nickname: bool = F.is_null(_.nickname)
    """
    return UnderscoreFunction("is_null", expr)


class When:
    def __init__(self, parent: Then | None, condition: Any):
        super().__init__()
        self._then = parent
        self._condition = condition

    def then(self, value: Any) -> "Then":
        """The value to return if the condition is met.
        This method *must* be called after `.when(...)`.

        Parameters
        ----------
        value
            The value to return if the condition is met.
        """
        return Then(parent=self, value=value)


class Then:
    def __init__(self, parent: When, value: Any):
        super().__init__()
        self._when = parent
        self._value = value

    def when(self, condition: Any) -> When:
        """Add another condition to the conditional expression.

        After this method is called, it is expected that you will
        call `.then(...)` to specify the value to return if the
        condition is met.

        Parameters
        ----------
        condition
            The condition to evaluate.
        """
        return When(parent=self, condition=condition)

    def otherwise(self, default: Any) -> Any:
        """The default value to return if no conditions are met.

        Parameters
        ----------
        default
            The default value to return if no conditions are met.

        Returns
        -------
        Any
            The underscore expression. After this method has been called,
            you cannot add more conditions to the conditional expression.
        """
        result = default
        current: Then | None = self
        while current is not None:
            result = if_then_else(
                condition=current._when._condition,  # pyright: ignore[reportPrivateUsage]
                if_true=current._value,
                if_false=result,
            )
            current = current._when._then  # pyright: ignore[reportPrivateUsage]
        return result


def when(condition: Any) -> When:
    """Build a conditional expression.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    age: float
    ...    age_group: str = (
    ...      F.when(_.age < 1)
    ...       .then("baby")
    ...       .when(_.age < 3)
    ...       .then("toddler")
    ...       .when(_.age < 13)
    ...       .then("child")
    ...       .when(_.age < 18)
    ...       .then("teen")
    ...       .otherwise(F.cast(F.cast(F.floor(_.age / 10), int), str) + "0s")
    ...   )
    """
    return When(parent=None, condition=condition)


def if_then_else(condition: Underscore, if_true: Any, if_false: Any) -> Underscore:
    """
    Create a conditional expression, roughly equivalent to:

    ```
    if condition:
        return if_true
    else:
        return if_false
    ```

    Unlike a Python if/else, all three inputs `(condition, if_true, if_false)` are evaluated
    in parallel for all rows, and then the correct side is selected based on the result of
    the condition expression.

    Examples
    --------
    >>> from chalk import _
    >>> from chalk.features import features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    amount: int
    ...    risk_score: float = _.if_then_else(
    ...      _.amount > 10_000,
    ...      _.amount * 0.1,
    ...      _.amount * 0.05,
    ...    )
    """
    return UnderscoreFunction("if_else", condition, if_true, if_false)


KeyType = TypeVar("KeyType")
ValueType = TypeVar("ValueType")


def map_dict(
    d: dict[KeyType, ValueType],
    key: Underscore,
    *,
    default: ValueType | None,
):
    """
    Map a key to a value in a dictionary.

    Parameters
    ----------
    d
        The dictionary to map the key to a value in.
    key
        The key to look up in the dictionary.
    default
        The default value to return if the key is not found in the dictionary.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    merchant: str
    ...    merchant_risk_score: float = F.map_dict(
    ...        {"Amazon": 0.1, "Walmart": 0.08},
    ...        _.merchant,
    ...        default=0.,
    ...    )
    """
    if default is not None:
        return coalesce(map_get(d, key), default)
    return map_get(d, key)


def map_get(mapping: Mapping[KeyType, ValueType], key: Any):
    """
    Get the value for a key in a mapping.

    Parameters
    ----------
    mapping
        The mapping to get the value from.
    key
        The key to get the value for.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    merchant: str
    ...    merchant_risk_score: float = F.map_get(
    ...        {"Amazon": 0.1, "Walmart": 0.08},
    ...        _.merchant,
    ...    )
    """
    key_type = pa.scalar([k for k in mapping.keys()]).type.value_type
    value_type = pa.scalar([v for v in mapping.values()]).type.value_type
    map_type = pa.map_(key_type, value_type)
    return UnderscoreFunction("map_get", pa.scalar(mapping, type=map_type), key)


def sagemaker_predict(
    body: Underscore | Any,
    *,
    endpoint: str,
    content_type: str | None = None,
    target_model: str | None = None,
    target_variant: str | None = None,
    aws_access_key_id_override: str | None = None,
    aws_secret_access_key_override: str | None = None,
    aws_session_token_override: str | None = None,
    aws_region_override: str | None = None,
    aws_profile_name_override: str | None = None,
):
    """
    Runs a sagemaker prediction on the specified endpoint, passing in the serialized bytes as a feature.

    Parameters
    ----------
    body
        Bytes feature to be passed as the serialized input to the sagemaker endpoint.
    endpoint
        The name of the sagemaker endpoint.
    content_type
        The content type of the input data. If not specified, the content type will be inferred from the endpoint.
    target_model
        An optional argument which specifies the target model for the prediction.
        This should only be used for multimodel sagemaker endpoints.
    target_variant
        An optional argument which specifies the target variant for the prediction.
        This should only be used for multi variant sagemaker endpoints.
    aws_access_key_id_override
        An optional argument which specifies the AWS access key ID to use for the prediction.
    aws_secret_access_key_override
        An optional argument which specifies the AWS secret access key to use for the prediction.
    aws_session_token_override
        An optional argument which specifies the AWS session token to use for the prediction.
    aws_region_override
        An optional argument which specifies the AWS region to use for the prediction.
    aws_profile_name_override
        An optional argument which specifies the AWS profile name to use for the prediction

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    encoded_sagemaker_data: bytes
    ...    prediction: float = F.sagemaker_predict(
    ...        _.encoded_sagemaker_data,
    ...        endpoint="prediction-model_1.0.1_2024-09-16",
    ...        target_model="model_v2.tar.gz",
    ...        target_variant="blue"
    ...    )
    """
    return UnderscoreFunction(
        "sagemaker_predict",
        body,
        endpoint,
        content_type,
        target_model,
        target_variant,
        aws_access_key_id_override,
        aws_secret_access_key_override,
        aws_session_token_override,
        aws_region_override,
        aws_profile_name_override,
    )


def json_value(expr: Underscore, path: Union[str, Underscore]):
    """
    Extract a scalar from a JSON feature using a JSONPath expression. The value of the referenced path must be a JSON
    scalar (boolean, number, string).

    Parameters
    ----------
    expr
        The JSON feature to query.
    path
        The JSONPath-like expression to extract the scalar from the JSON feature.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk import JSON
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    profile: JSON
    ...    favorite_color: str = F.json_value(_.profile, "$.prefs.color")
    """

    return UnderscoreFunction("get_json_value", expr, path)


def json_extract_array(expr: Underscore, path: Union[str, Underscore]):
    """
    Extract a string array from a JSON feature using a JSONPath expression. The value of the referenced path must be a JSON
    node containing an array, or a wildcard object match like: $some_path[*].some_object_property.

    Only arrays of strings, bools, numbers, and nulls are supported. If the array contains objects, the function will
    return 'null'.

    Parameters
    ----------
    expr
        The JSON feature to query.
    path
        The JSONPath-like expression to extract the array from the JSON feature.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk import JSON
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    profile: JSON
    ...    favorite_categories: list[str] = F.json_extract_array(_.profile, "$.prefs.favorite_categories")
    """

    return UnderscoreFunction("json_extract_array", expr, path)


def gunzip(expr: Underscore):
    """
    Decompress a GZIP-compressed bytes feature.

    Parameters
    ----------
    expr
        The GZIP-compressed bytes feature to decompress.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    compressed_data: bytes
    ...    decompressed_data: bytes = F.gunzip(_.compressed_data)
    """
    return UnderscoreFunction("gunzip", expr)


def cosine_similarity(a: Underscore, b: Underscore):
    """
    Compute the cosine similarity between two vectors.

    Parameters
    ----------
    a
        The first vector.
    b
        The second vector.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    embedding: Vector[1536]
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    embedding: Vector[1536]
    >>> @features
    ... class UserMerchant:
    ...    id: str
    ...    user_id: User.id
    ...    user: User
    ...    merchant_id: Merchant.id
    ...    merchant: Merchant
    ...    similarity: float = F.cosine_similarity(_.user.embedding, _.merchant.embedding)
    """
    return UnderscoreFunction("cosine_similarity_vector", a, b)


########################################################################################################################
# Mathematical Functions                                                                                               #
########################################################################################################################


def power(a: Underscore | Any, b: Underscore | Any):
    """
    Raise a to the power of b. Alias for `a ** b`.

    Parameters
    ----------
    a
        The base.
    b
        The exponent.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    amount_std: float
    ...    amount_var: float = F.power(_.amount_std, 2)
    """
    return UnderscoreFunction("power", a, b)


def sqrt(expr: Underscore | Any):
    """
    Compute the square root of a number.

    Parameters
    ----------
    expr
        The number to compute the square root of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    amount_var: float
    ...    amount_std: float = F.sqrt(_.amount_var)
    """
    return UnderscoreFunction("sqrt", expr)


def safe_divide(x: Underscore | Any, y: Underscore | Any):
    """
    Computes x / y, returning None if y is 0.

    Parameters
    ----------
    x
        The numerator.
    y
        The denominator.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Merchant:
    ...    id: str
    ...    a: float
    ...    b: float
    ...    amount_std: float = F.safe_divide(_.a, _.b)
    """

    return if_then_else(
        condition=y == 0,
        if_true=None,
        if_false=x / y,
    )


def floor(expr: Underscore | Any):
    """
    Compute the floor of a number.

    Parameters
    ----------
    expr
        The number to compute the floor of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    amount_floor: float = F.floor(_.amount)
    """
    return UnderscoreFunction("floor", expr)


def ceil(expr: Underscore | Any):
    """
    Compute the ceiling of a number.

    Parameters
    ----------
    expr
        The number to compute the ceiling of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    amount_ceil: float = F.ceil(_.amount)
    """
    return UnderscoreFunction("ceil", expr)


def mod(dividend: Underscore | Any, divisor: Underscore | Any):
    """
    Compute the remainder of a division.

    Parameters
    ----------
    dividend
        The dividend.
    divisor
        The divisor.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    day_of_week_monday: int = F.day_of_week(_.date)
    ...    day_of_week_sunday: int = F.mod(_.day_of_week_monday, 7) + 1
    """
    return UnderscoreFunction("%", dividend, divisor)


def abs(expr: Underscore | Any):
    """
    Compute the absolute value of a number.

    Parameters
    ----------
    expr
        The number to compute the absolute value of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    amount_abs: float = F.abs(_.amount)
    """
    return UnderscoreFunction("abs", expr)


def sin(expr: Underscore | Any):
    """
    Compute the sine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    angle: float
    ...    sin_angle: float = F.sin(_.angle)
    """
    return UnderscoreFunction("sin", expr)


def asin(expr: Underscore | Any):
    """
    Compute the arcsine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    sin_angle: float
    ...    angle: float = F.asin(_.sin_angle)
    """
    return UnderscoreFunction("asin", expr)


def cos(expr: Underscore | Any):
    """
    Compute the cosine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    angle: float
    ...    cos_angle: float = F.cos(_.angle)
    """
    return UnderscoreFunction("cos", expr)


def acos(expr: Underscore | Any):
    """
    Compute the arccosine of an angle in radians.

    Parameters
    ----------
    expr
        The angle in radians.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    cos_angle: float
    ...    angle: float = F.acos(_.cos_angle)
    """
    return UnderscoreFunction("acos", expr)


def ln(expr: Underscore | Any):
    """
    Compute the natural logarithm of a number.

    Parameters
    ----------
    expr
        The number to compute the natural logarithm of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    hypotenuse: float
    ...    log_hypotenuse: float = F.ln(_.hypotenuse)
    """
    return UnderscoreFunction("ln", expr)


def exp(expr: Underscore | Any):
    """
    Returns Euler’s number raised to the power of x.

    Parameters
    ----------
    expr
        The exponent to raise Euler's number to.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Triangle:
    ...    id: str
    ...    x: float
    ...    e_to_x: float = F.exp(_.x)
    """
    return UnderscoreFunction("exp", expr)


def sigmoid(expr: Underscore | Any):
    """
    Compute the sigmoid of a number.

    Parameters
    ----------
    expr
        The number to compute the sigmoid of.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Sigmoid:
    ...    id: str
    ...    x: float
    ...    sigmoid_of_x: float = F.sigmoid(_.x)
    """
    return 1 / (1 + exp(-1 * expr))


########################################################################################################################
# Date and Time Functions                                                                                              #
########################################################################################################################


def format_datetime(input_dt: Any, format: str | Any):
    """Format a datetime feature using a format string.

    ```
    | Symbol | Meaning                      | Examples                           |
    |--------|------------------------------|------------------------------------|
    | G      | era                          | AD                                 |
    | C      | century of era (>=0)         | 20                                 |
    | Y      | year of era (>=0)            | 1996                               |
    | x      | weekyear                     | 1996                               |
    | w      | week of weekyear             | 27                                 |
    | e      | day of week                  | 2                                  |
    | E      | day of week                  | Tuesday; Tue                       |
    | y      | year                         | 1996                               |
    | D      | day of year                  | 189                                |
    | M      | month of year                | July; Jul; 07                      |
    | d      | day of month                 | 10                                 |
    | a      | halfday of day               | PM                                 |
    | K      | hour of halfday (0~11)       | 0                                  |
    | h      | clockhour of halfday (1~12)  | 12                                 |
    | H      | hour of day (0~23)           | 0                                  |
    | k      | clockhour of day (1~24)      | 24                                 |
    | m      | minute of hour               | 30                                 |
    | s      | second of minute             | 55                                 |
    | S      | fraction of second           | 978                                |
    | z      | time zone                    | Pacific Standard Time; PST         |
    | Z      | time zone offset/id          | -0800; -08:00; America/Los_Angeles |
    | '      | escape for text              |                                    |
    | ''     | single quote                 | '                                  |
    ```
    """
    return UnderscoreFunction("format_datetime", input_dt, format)


def total_seconds(delta: Underscore) -> Underscore:
    """
    Compute the total number of seconds covered in a duration.

    Parameters
    ----------
    delta
        The duration to convert to seconds.

    Examples
    --------
    >>> from datetime import date
    >>> from chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    signup: date
    ...    last_login: date
    ...    signup_to_last_login_days: float = F.total_seconds(_.las_login - _.signup) / (60 * 60 * 24)
    """
    return UnderscoreFunction("total_seconds", delta)


def unix_seconds(expr: Underscore | Any):
    """
    Extract the number of seconds since the Unix epoch.
    Returned as a float.

    Parameters
    ----------
    expr
        The datetime to extract the number of seconds since the Unix epoch from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    unix_seconds: float = F.unix_seconds(_.date)
    """
    return UnderscoreFunction("to_unixtime", expr)


def unix_milliseconds(expr: Underscore | Any):
    """
    Extract the number of milliseconds since the Unix epoch.
    Returned as a float.

    Parameters
    ----------
    expr
        The datetime to extract the number of milliseconds since the Unix epoch from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    unix_milliseconds: float = F.unix_milliseconds(_.date)
    """
    return UnderscoreFunction("to_unixtime", expr) * 1000.0


def from_unix_seconds(expr: Underscore | Any):
    """
    Converts a Unix timestamp (in seconds) to a utc timestamp.

    Parameters
    ----------
    expr
        The Unix timestamp to convert.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Linux:
    ...    id: str
    ...    unixtime_s: int = 0
    ...    unix: int = F.unix_milliseconds(_.date)
    """
    return UnderscoreFunction("from_unixtime", expr)


def from_unix_milliseconds(expr: Underscore | Any):
    """
    Converts a Unix timestamp (in milliseconds) to a utc timestamp.

    Parameters
    ----------
    expr
        A date represented as the number of millisecods since the Unix timestamp.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Linux:
    ...    id: int
    ...    unixtime_ms: int = 0
    ...    unixtime: datetime = F.from_unix_milliseconds(_.unix)
    """
    return UnderscoreFunction("from_unixtime", (expr / 1000))


def day_of_month(expr: Underscore | Any):
    """
    Extract the day of the month from a date.

    The supported types for x are date and datetime.

    Ranges from 1 to 31 inclusive.

    Parameters
    ----------
    expr
        The date to extract the day of the month from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_month(_.date)
    """
    return UnderscoreFunction("day_of_month", expr)


def day_of_week(
    expr: Underscore | Any,
    start_of_week: DayOfWeek = DayOfWeek.MONDAY,
):
    """
    Returns the ISO day of the week from x. The value ranges from 1 (`start_of_week`, default `MONDAY`)
    to 7 (`start_of_week + 6`, default `SUNDAY`).

    Parameters
    ----------
    expr
        The date to extract the day of the week from.
    start_of_week
        The day of the week that the week starts on. Defaults to Monday.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_week(_.date)
    """
    if start_of_week == DayOfWeek.MONDAY == 1:
        return UnderscoreFunction("day_of_week", expr)
    return ((UnderscoreFunction("day_of_week", expr) - int(start_of_week)) + 7) % 7 + 1


def day_of_year(expr: Underscore | Any):
    """
    Extract the day of the year from a date.

    The value ranges from 1 to 366.

    Parameters
    ----------
    expr
        The date to extract the day of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    day: int = F.day_of_year(_.date)
    """
    return UnderscoreFunction("day_of_year", expr)


def month_of_year(expr: Underscore | Any):
    """
    Extract the month of the year from a date.

    The value ranges from 1 to 12.

    Parameters
    ----------
    expr
        The date to extract the month of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    month: int = F.month_of_year(_.date)
    """
    return UnderscoreFunction("month", expr)


def week_of_year(expr: Underscore | Any):
    """
    Extract the week of the year from a date.

    The value ranges from 1 to 53.

    Parameters
    ----------
    expr
        The date to extract the week of the year from.

    Examples
    --------
    >>> from datetime import date
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: date
    ...    week: int = F.week_of_year(_.date)
    """
    return UnderscoreFunction("week_of_year", expr)


def hour_of_day(expr: Underscore | Any):
    """
    Extract the hour of the day from a datetime.

    The value ranges from 0 to 23.

    Parameters
    ----------
    expr
        The datetime to extract the hour of the day from.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    date: datetime
    ...    hour: int = F.hour_of_day(_.date)
    """
    return UnderscoreFunction("hour", expr)


def to_iso8601(expr: Underscore | Any):
    """
    Formats input datetime as an ISO 8601 string

    Parameters
    ----------
    expr
        The datetime to convert into ISO 8601 string.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class IsoStr:
    ...    id: str
    ...    iso_str: str = F.to_iso8601(_.iso_date)
    ...    iso_date: datetime
    """
    return UnderscoreFunction("to_iso8601", expr)


def is_us_federal_holiday(expr: Underscore | Any):
    """
    Returns `True` if the given date or datetime is a US Federal Holiday, else `False`

    Parameters
    ----------
    expr
        The date or datetime to be tested

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Event:
    ...    id: str
    ...    event_date: datetime
    ...    is_us_federal_holiday: F.is_us_federal_holiday(_.event_date)

    Notes
    -----
    Here is a list of the US Federal Holidays:
    - New Year's Day (January 1)*
    - Martin Luther King's Birthday (3rd Monday in January)
    - Washington's Birthday (3rd Monday in February)**
    - Memorial Day (last Monday in May)
    - Juneteenth National Independence Day (June 19)*
    - Independence Day (July 4)*
    - Labor Day (1st Monday in September)
    - Columbus Day (2nd Monday in October)
    - Veterans' Day (November 11)*
    - Thanksgiving Day (4th Thursday in November)
    - Christmas Day (December 25)*

    * If one of these dates would fall on a Saturday/Sunday, the federal holiday will
      be observed on the proceeding Friday/following Monday, respectively

    ** More commonly known as "Presidents' Day"

    *** Every four years, Inaguration Day (January 20) is recognized as a federal holiday
        exclusively in Washington D.C. Inaguration days are *not* accounted for in this underscore
    """
    return UnderscoreFunction("is_federal_holiday", expr)


########################################################################################################################
# DataFrame Aggregations                                                                                               #
########################################################################################################################


def max_by(dataframe: Underscore | Any, sort: Underscore | Any):
    """
    Returns the row in a dataframe or has-many relationship with the maximum value in a given column.

    Parameters
    ----------
    dataframe
        The `DataFrame` or has-many relationship to find the maximum value in.
        This `DataFrame` should refer to *exactly* one result column, which
        should reference the returned value. The `DataFrame` can include any
        necessary filters.
    sort
        The column on which to sort.

    Returns
    -------
    The maximum value row, or a transformed representation based on the columns provided.

    Examples
    --------
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_one
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     amount: float
    ...     user_id: "User.id"
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction]
    ...     biggest_transfer_id: Transaction.id = F.max_by(
    ...         _.transactions[_.category == "ach", _.id],
    ...         _.amount,
    ...     )
    ...     biggest_transfer: Transaction = has_one(
    ...         lambda: Transaction.id == User.biggest_transfer_id
    ...     )
    """
    return UnderscoreFunction("max_by", dataframe, sort)


def min_by(dataframe: Underscore | Any, sort: Underscore | Any):
    """
    Returns the row in a dataframe or has-many relationship with the minimum value in a given column.

    Parameters
    ----------
    dataframe
        The `DataFrame` or has-many relationship to find the minimum value in.
        This `DataFrame` should refer to *exactly* one result column, which
        should reference the returned value. The `DataFrame` can include any
        necessary filters.
    sort
        The column on which to sort.

    Returns
    -------
    The minimum value row, or a transformed representation based on the columns provided.

    Examples
    --------
    >>> from chalk import DataFrame, _
    >>> from chalk.features import features, has_one
    >>> import chalk.functions as F
    >>> @features
    ... class Transaction:
    ...     id: int
    ...     amount: float
    ...     user_id: "User.id"
    >>> @features
    ... class User:
    ...     id: int
    ...     transactions: DataFrame[Transaction]
    ...     smallest_transfer_id: Transaction.id = F.min_by(
    ...         _.transactions[_.category == "ach", _.id],
    ...         _.amount,
    ...     )
    ...     smallest_transfer: Transaction = has_one(
    ...         lambda: Transaction.id == User.smallest_transfer_id
    ...     )
    """
    return UnderscoreFunction("min_by", dataframe, sort)


def head(dataframe: Underscore | Any, n: Underscore | int):
    """
    Returns the first n items from a dataframe or has-many

    Parameters
    ----------
    dataframe
        the has-many from which the first n items are taken
    n
        how many items to take

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk import windowed, DataFrame, Windowed
    >>> from chalk.features import _, features, Primary
    >>> @features
    >>> class Merchant:
    ...     id: str
    >>> @features
    >>> class ConfirmedFraud:
    ...     id: int
    ...     trn_dt: datetime
    ...     is_fraud: int
    ...     mer_id: Merchant.id
    >>> @features
    >>> class MerchantFraud:
    ...     mer_id: Primary[Merchant.id]
    ...     merchant: Merchant
    ...     confirmed_fraud: DataFrame[ConfirmedFraud] = dataframe(
    ...         lambda: ConfirmedFraud.mer_id == MerchantFraud.mer_id,
    ...     )
    ...     first_five_merchant_window_fraud: Windowed[list[int]] = windowed(
    ...         "1d",
    ...         "30d",
    ...         expression=F.head(_.confirmed_fraud[_.trn_dt > _.chalk_window, _.id, _.is_fraud == 1], 5)
    ...     )
    """
    return slice(UnderscoreFunction("array_agg", dataframe), 0, n)


########################################################################################################################
# Array Functions                                                                                                      #
########################################################################################################################
def _convert_to_0_index(index: Underscore | int):
    if isinstance(index, int):
        return index if index < 0 else index + 1
    else:
        return UnderscoreFunction(
            "if_else", UnderscoreFunction("<", index, 0), index, UnderscoreFunction("+", index, 1)
        )


def slice(arr: Underscore | list[Any], offset: Underscore | int, length: Underscore | int):
    """
    Returns a subset of the original array.

    Parameters
    ----------
    arr
        The array to slice
    offset
        Starting index of the slice (0-indexed). If negative, slice starts from the end of the array
    length
        The length of the slice.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    three_most_recent_words: list[str] = F.slice(_.words, -3, 3) # computes ["zebra", "hello", "world"]
    """

    start = _convert_to_0_index(offset)
    return UnderscoreFunction("slice", arr, start, length)


def array_sort(expr: Underscore | Any, descending: bool = False):
    """
    Returns an array which has the sorted order of the input
    array. Null elements will be placed at the end of the
    returned array.

    Parameters
    ----------
    expr
        The array to sort
    descending
        Whether to sort the array in descending order. Defaults to False.
    """
    if descending:
        return UnderscoreFunction("array_sort_desc", expr)
    return UnderscoreFunction("array_sort", expr)


def array_agg(expr: Underscore | Any):
    """Extract a single-column `DataFrame` into a list of values for that column.

    Parameters
    ----------
    expr
        The expression to extract into a list.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk import DataFrame
    >>> from chalk.features import _, features
    >>> @features
    >>> class Merchant:
    ...     id: str
    ...     events: "DataFrame[FraudEvent]"
    ...     fraud_codes: list[str] = F.array_agg(_.events[_.is_fraud == True, _.tag])
    >>> @features
    >>> class FraudEvent:
    ...     id: int
    ...     tag: str
    ...     is_fraud: bool
    ...     mer_id: Merchant.id
    """
    return UnderscoreFunction("array_agg", expr)


def array_join(arr: Underscore | list[Any], delimiter: str):
    """
    Concatenate the elements of an array into a single string with a delimiter.

    Parameters
    ----------
    arr
        The array to join. The values will be casted to strings if they are not already strings.
    delimiter
        The delimiter to use to join the elements of the array.

    Examples
    --------
    >>> from datetime import datetime
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    >>> class Wordle:
    ...    id: str
    ...    words: list[str]
    ...    words_str: str = F.array_join(_.words, ", ")
    """
    return UnderscoreFunction("array_join", arr, delimiter)


def element_at(arr: Underscore | list[Any], index: int | Underscore):
    """
    Returns the element of an array at the given index.

    Parameters
    ----------
    arr
        The array.
    index
        The index to extract the element from (0-indexed).

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str] = ["crane", "kayak", "plots", "fight", "exact", "zebra", "hello", "world"]
    ...    first_word: str = F.element_at(_.words, 0)
    """
    return UnderscoreFunction("element_at", arr, _convert_to_0_index(index))


def array_count_value(expr: Underscore, value: Union[str, Underscore]):
    """
    Returns the count of a string value in an array.

    Parameters
    ----------
    expr
        The string array.
    value
        The value to count in the array

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Bookstore:
    ...    id: str
    ...    inventory_types: list[str] = ["fiction", "non-fiction", "fiction", "fiction", "non-fiction"
    ...    books: str = F.array_count_value(_.inventory_types, "fiction")
    """
    return UnderscoreFunction(
        "cardinality",
        UnderscoreFunction(
            "array_filter",
            expr,
            UnderscoreFunction(
                "lambda",
                "x",
                pa.large_string(),
                UnderscoreFunction("lambda_parameter", "x", pa.large_string()) == value,
            ),
        ),
    )


def contains(arr: Underscore | list[Any], value: Any):
    """
    Returns whether the array contains the value.

    Parameters
    ----------
    arr
        The array to check for the value.
    value
        The value to check for in the array.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class APIRequest:
    ...    id: str
    ...    headers: list[str]
    ...    has_user_agent: bool = F.contains(_.headers, "User-Agent")
    """
    return UnderscoreFunction("contains", arr, value)


def cardinality(arr: Underscore):
    """
    Returns the number of elements in an array.

    Parameters
    ----------
    arr
        The array to count the number of elements in.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Wordle:
    ...    id: str
    ...    words: list[str]
    ...    num_words: int = F.cardinality(_.words)
    """
    return UnderscoreFunction("cardinality", arr)


########################################################################################################################
# Additional Aggregations                                                                                              #
########################################################################################################################


def haversine(
    lat1: Underscore | Any,
    lon1: Underscore | Any,
    lat2: Underscore | Any,
    lon2: Underscore | Any,
):
    """
    Compute the haversine distance (in kilometers) between two points on the Earth.

    Parameters
    ----------
    lat1
        The latitude of the first point.
    lon1
        The longitude of the first point.
    lat2
        The latitude of the second point.
    lon2
        The longitude of the second point.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Location:
    ...    id: str
    ...    lat1: float
    ...    lon1: float
    ...    lat2: float
    ...    lon2: float
    ...    distance: float = F.haversine(_.lat1, _.lon1, _.lat2, _.lon2)
    """
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = power(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * power(sin(dlon / 2), 2)
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers.
    return if_then_else(
        is_null(lat1) | is_null(lon1) | is_null(lat2) | is_null(lon2),
        None,
        c * r,
    )


def cast(expr: Any, dtype: pa.DataType | type[Any]):
    """Cast an expression to a different type.

    Parameters
    ----------
    expr
        The expression to cast.
    dtype
        The type to cast the expression to.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    user_id: "User.id"
    ...    merchant_id: "Merchant.id"
    ...    user_merchant_id: "UserMerchant.id" = (
    ...        F.cast(_.user_id, str) + "_" +
    ...        F.cast(_.merchant_id, str)
    ...    )
    """
    if isinstance(dtype, type) and issubclass(dtype, Enum):
        return if_then_else(contains([member.value for member in dtype], expr), expr, None)
    return UnderscoreCast(expr, dtype if isinstance(dtype, pa.DataType) else rich_to_pyarrow(dtype, "underscore cast"))


def from_base(value: Any, base: int | Underscore):
    """Convert a number in a base to an integer.

    Parameters
    ----------
    value
        The number to convert.
    base
        The base of the number. Must be between 2 and 36.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    base_16: str
    ...    base_10: int = F.from_base(_.base_16, 16)
    """
    if isinstance(base, int) and (base < 2 or base > 36):
        raise ValueError(f"Base must be between 2 and 36. Got {base}.")
    return UnderscoreFunction("from_base", value, base)


def round(value: Any):
    """Round a number to the nearest integer.

    Parameters
    ----------
    value
        The number to round.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class Transaction:
    ...    id: str
    ...    amount: float
    ...    rounded_amount: int = F.round(_.amount)
    """
    return UnderscoreFunction("round", value)


def max(*values: Any):
    """
    Returns the maximum value in a list of values.
    This function is meant to be supplied with several
    columns, not with a single has-many or `DataFrame`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    score_1: float
    ...    score_2: float
    ...    max_score: float = F.max(_.score_1, _.score_2)
    """
    result = values[0] if len(values) > 0 else None
    for e in values[1:]:
        result = if_then_else(e > result, e, result)
    return result


def min(*values: Any):
    """
    Returns the minimum value in a list of values.
    This function is meant to be supplied with several
    columns, not with a single has-many or `DataFrame`.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> @features
    ... class User:
    ...    id: str
    ...    score_1: float
    ...    score_2: float
    ...    min_score: float = F.min(_.score_1, _.score_2)
    """
    result = values[0] if len(values) > 0 else None
    for e in values[1:]:
        result = if_then_else(e < result, e, result)
    return result


__all__ = (
    "DayOfWeek",
    "Then",
    "When",
    "abs",
    "acos",
    "array_agg",
    "array_count_value",
    "array_join",
    "array_sort",
    "asin",
    "bytes_to_string",
    "cardinality",
    "cast",
    "ceil",
    "coalesce",
    "contains",
    "cos",
    "cosine_similarity",
    "day_of_month",
    "day_of_week",
    "day_of_year",
    "element_at",
    "ends_with",
    "exp",
    "floor",
    "format_datetime",
    "from_base",
    "from_unix_milliseconds",
    "from_unix_seconds",
    "gunzip",
    "haversine",
    "head",
    "hour_of_day",
    "if_then_else",
    "is_null",
    "is_us_federal_holiday",
    "json_extract_array",
    "json_value",
    "levenshtein_distance",
    "like",
    "ln",
    "lower",
    "map_dict",
    "map_get",
    "max",
    "max_by",
    "md5",
    "min",
    "min_by",
    "mod",
    "month_of_year",
    "power",
    "regexp_extract",
    "regexp_extract_all",
    "regexp_like",
    "regexp_replace",
    "replace",
    "reverse",
    "round",
    "safe_divide",
    "sagemaker_predict",
    "sha1",
    "sha256",
    "sha512",
    "sigmoid",
    "sin",
    "slice",
    "split_part",
    "spooky_hash_v2_32",
    "spooky_hash_v2_64",
    "sqrt",
    "starts_with",
    "string_to_bytes",
    "strpos",
    "substr",
    "to_iso8601",
    "total_seconds",
    "trim",
    "unix_milliseconds",
    "unix_seconds",
    "upper",
    "url_extract_host",
    "url_extract_path",
    "url_extract_protocol",
    "week_of_year",
    "when",
)
