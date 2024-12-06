import collections
import dataclasses
from typing import Any, Dict, List, Mapping, Sequence, Tuple, cast

from chalk.features import Features, TPrimitive, ensure_feature
from chalk.features._encoding.json import FeatureEncodingOptions, unstructure_primitive_to_json
from chalk.features.feature_field import FeatureNotFoundException
from chalk.utils.json import TJSON


@dataclasses.dataclass
class InputEncodeOptions:
    encode_structs_as_objects: bool
    """c.f. encode_structs_as_objects in chalk.features._encoding.json.FeatureEncodingOptions"""

    json_encode: bool
    """
    If True, encode feature values into JSON. Specifically, structs/datetimes/bytes/etc. are encoded
    into a JSON-compatible format.
    If False, encode features values into a 'primitive' type (TPrimitive) but don't apply json encoding.
    This is needed for the HTTP client which sends feature data in JSON requests. However, the GRPC
    client transmits Arrow data which supports a richer set of types.
    """


HTTP_ENCODE_OPTIONS = InputEncodeOptions(json_encode=True, encode_structs_as_objects=False)
GRPC_ENCODE_OPTIONS = InputEncodeOptions(json_encode=False, encode_structs_as_objects=True)


def _recursive_unstructure_primitive_to_json(val: TPrimitive) -> TJSON:
    if isinstance(val, dict):
        return {cast(str, k): _recursive_unstructure_primitive_to_json(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple)):
        return [_recursive_unstructure_primitive_to_json(x) for x in val]
    else:
        return unstructure_primitive_to_json(val)


def recursive_encode_bulk_inputs(
    inputs: Mapping[str, Sequence[Any]], options: InputEncodeOptions
) -> Tuple[Dict[str, List[TJSON]], List[str]]:
    all_warnings: List[str] = []
    encoded_inputs: Dict[str, List[TJSON]] = collections.defaultdict(list)
    for wrapped_feature, vv in inputs.items():
        try:
            feature = ensure_feature(wrapped_feature)
        except FeatureNotFoundException:
            fqn = str(wrapped_feature)
            all_warnings.append(
                f"Input '{fqn}' not recognized. Recursively JSON encoding '{fqn}' and requesting anyways"
            )
            if options.json_encode:
                encoded_inputs[str(fqn)] = [_recursive_unstructure_primitive_to_json(v) for v in vv]
            else:
                encoded_inputs[str(fqn)] = list(iter(vv))
            continue

        if feature.is_has_many:
            for v in vv:
                if not isinstance(v, list):
                    raise TypeError(f"has-many feature '{feature.fqn}' must be a list, but got {type(v).__name__}")

                has_many_result: List[Dict[str, TJSON]] = []
                assert feature.joined_class is not None
                foreign_namespace = feature.joined_class.namespace
                for item in v:
                    # The value can be either a feature instance or a dict
                    if isinstance(item, Features):
                        item = dict(item.items())
                    if not isinstance(item, dict):
                        raise TypeError(
                            (
                                f"Has-many feature '{feature.root_fqn}' must be a list of dictionaries or feature set instances, "
                                f"but got a list of `{type(item).__name__}`"
                            )
                        )
                    # Prepend the namespace onto the dict keys, if it's not already there
                    item = {
                        k if str(k).startswith(f"{foreign_namespace}.") else f"{foreign_namespace}.{str(k)}": sub_v
                        for (k, sub_v) in item.items()
                    }
                    result, inner_warnings = recursive_encode_inputs(item, options=options)
                    all_warnings.extend(inner_warnings)
                    has_many_result.append(result)

                encoded_inputs[feature.root_fqn].append(has_many_result)
        elif feature.is_has_one:
            assert feature.joined_class is not None
            foreign_namespace = feature.joined_class.namespace
            for v in vv:
                # The value can be either a feature instance or a dict
                if isinstance(v, Features):
                    v = dict(v.items())
                if not isinstance(v, dict):
                    raise TypeError(
                        (
                            f"Has-one feature '{feature.root_fqn}' must be a list of dictionaries or feature set instances, "
                            f"but got a list of `{type(v).__name__}`"
                        )
                    )
                # Prepend the namespace onto the dict keys, if needed
                v = {
                    k if str(k).startswith(f"{foreign_namespace}.") else f"{foreign_namespace}.{str(k)}": sub_v
                    for (k, sub_v) in v.items()
                }
                has_one_values, inner_warnings = recursive_encode_inputs(v, options=options)
                all_warnings.extend(inner_warnings)
                # Flatten the has-one inputs onto the encoded inputs dict -- similar to how input
                # features
                root_parts = feature.root_fqn.split(".")
                for k, encoded_v in has_one_values.items():
                    # Chop off the namespace from the nested features, as the
                    # namespace is implied by the has-one feature
                    root_fqn = ".".join((*root_parts, *k.split(".")[1:]))
                    encoded_inputs[root_fqn].append(encoded_v)
        else:
            for v in vv:
                if feature.primary:
                    if not isinstance(v, (int, str)):
                        raise TypeError(
                            f"Input '{v}' for primary feature {feature.root_fqn} must be of type int or str"
                        )
                if options.json_encode:
                    converted_value = feature.converter.from_rich_to_json(
                        v,
                        # Allowing missing values because the server could be on a different version of the code that has a default
                        missing_value_strategy="allow",
                        # (pyarrow.RecordBatch.from_pydict expects dict's for struct data, as opposed to an array.)
                        options=FeatureEncodingOptions(encode_structs_as_objects=options.encode_structs_as_objects),
                    )
                else:
                    converted_value = feature.converter.from_rich_to_primitive(
                        v,
                        # Allowing missing values because the server could be on a different version of the code that has a default
                        missing_value_strategy="allow",
                    )

                encoded_inputs[feature.root_fqn].append(converted_value)
    return encoded_inputs, all_warnings


def recursive_encode_inputs(
    inputs: Mapping[str, Any], options: InputEncodeOptions = HTTP_ENCODE_OPTIONS
) -> Tuple[Dict[str, TJSON], List[str]]:
    bulk_result, warnings = recursive_encode_bulk_inputs({k: [v] for k, v in inputs.items()}, options=options)
    return {k: next(iter(v)) for (k, v) in bulk_result.items()}, warnings
