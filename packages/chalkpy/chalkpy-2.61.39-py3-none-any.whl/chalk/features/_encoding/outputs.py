from typing import Any, List, Sequence, Union

from chalk.features import Feature, FeatureWrapper, Resolver
from chalk.features.feature_set import is_features_cls


def encode_outputs(output: Sequence[Union[str, Any]]) -> List[str]:
    """Returns a list of encoded outputs and warnings"""
    encoded_output: List[str] = []
    for o in output:
        if isinstance(o, (Feature, FeatureWrapper)):
            encoded_output.append(str(o))
        elif is_features_cls(o):
            encoded_output.append(o.namespace)
        elif isinstance(o, Resolver):
            encoded_output.append(o.fqn.split(".")[-1])
        else:
            encoded_output.append(str(o))
    return encoded_output
