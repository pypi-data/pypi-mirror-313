import sys
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

from tecton_core import materialization_context
from tecton_core.errors import TectonValidationError
from tecton_proto.args.user_defined_function_pb2 import UserDefinedFunction


# TODO(deprecated_after=0.5): handle backward-compatibility for builtin transformations that did not use tecton.materialization_context
# but instead directly accessed tecton_spark.materialization_context
sys.modules["tecton_spark.materialization_context"] = materialization_context


def from_proto(
    serialized_transform: UserDefinedFunction,
    globals_: Optional[Dict[str, Any]] = None,
    locals_: Optional[Dict[str, Any]] = None,
) -> Callable:
    """
    deserialize into the provided scope, by default we deserialize the functions into their own scopes
    """

    if globals_ is None:
        globals_ = {}

    assert serialized_transform.HasField("body") and serialized_transform.HasField(
        "name"
    ), "Invalid UserDefinedFunction."

    try:
        exec(serialized_transform.body, globals_, locals_)
    except NameError as e:
        msg = "Failed to serialize function. Please note that all imports must be in the body of the function (not top-level) and type annotations cannot require imports. Additionally, be cautious of variables that shadow other variables. See https://docs.tecton.ai/docs/defining-features/feature-views/transformations for more details."
        raise TectonValidationError(
            msg,
            e,
        )

    # Return function pointer
    try:
        fn = eval(serialized_transform.name, globals_, locals_)
        fn._code = serialized_transform.body
        return fn
    except Exception as e:
        msg = "Invalid transform"
        raise ValueError(msg) from e


# This version of function deserialization uses the "main scope".
# This has historically been the behavior of function deserialization.
# Generally this should be avoided since it can cause hard to debug issues,
# e.g. two helper functions of the same name can shadow each other. This global
# scope can also cause issues since it allows for users to access imported
# libraries that they did not import themselves.
def from_proto_to_main(serialized_transform: UserDefinedFunction) -> Callable:
    """
    deserialize into global scope by default
    """

    main_scope = __import__("__main__").__dict__
    return from_proto(serialized_transform, globals_=main_scope)
