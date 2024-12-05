from inspect import signature
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Set
from typing import Union

import attrs
import pandas as pd
import pyspark
from google.protobuf import empty_pb2
from typeguard import typechecked

from tecton._internals import display
from tecton._internals import errors
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import spark_api
from tecton._internals import validations_api
from tecton._internals.repo import function_serialization
from tecton.cli import repo_utils as cli_common
from tecton.framework import base_tecton_object
from tecton.framework import data_frame
from tecton.framework.utils import get_transformation_mode_enum
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import materialization_context
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.args import pipeline_pb2
from tecton_proto.args import transformation_pb2 as transformation__args_proto
from tecton_proto.args.transformation_pb2 import TransformationMode
from tecton_proto.common import fco_locator_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2


class Constant:
    """
    Wraps a const value that can be used as arguments to a Pipeline functions.
    """

    ALLOWED_TYPES = [str, int, float, bool, type(None)]

    def __init__(self, value: Optional[Union[str, int, float, bool]]):
        """Declare a Const object.
        :param value: The constant value encapsulated by this Const object.
        """
        self.value = value
        self.value_type = type(value)

        if self.value_type not in self.ALLOWED_TYPES:
            raise errors.InvalidConstantType(value, self.ALLOWED_TYPES)

    def __repr__(self):
        return f"Constant(value={self.value}, type={self.value_type})"


def const(value: Optional[Union[str, int, float, bool]]) -> Constant:
    """
    Wraps a const and returns a ``Constant`` object that can be used as arguments to a pipeline functions.

    :param value: The constant value that needs to be wrapped and used in the pipeline function.
    :return: A :class:`Constant` object.
    """
    return Constant(value)


@attrs.define
class PipelineNodeWrapper:
    """A dataclass used to build feature view pipelines.

    Attributes:
        node_proto: The Pipeline node proto that this wrapper represents.
        transformations: The set of Transformation objects included by this node or its dependencies.
    """

    node_proto: pipeline_pb2.PipelineNode
    transformations: Set["Transformation"] = attrs.field(factory=set)

    @classmethod
    def create_from_arg(
        cls,
        arg: Union["PipelineNodeWrapper", Constant, materialization_context.UnboundMaterializationContext],
        transformation_name: str,
    ) -> "PipelineNodeWrapper":
        if isinstance(arg, PipelineNodeWrapper):
            return arg
        elif isinstance(arg, Constant):
            constant_node = pipeline_pb2.ConstantNode()
            if arg.value is None:
                constant_node.null_const.CopyFrom(empty_pb2.Empty())
            elif arg.value_type == str:
                constant_node.string_const = arg.value
            elif arg.value_type == int:
                constant_node.int_const = repr(arg.value)
            elif arg.value_type == float:
                constant_node.float_const = repr(arg.value)
            elif arg.value_type == bool:
                constant_node.bool_const = arg.value
            return PipelineNodeWrapper(node_proto=pipeline_pb2.PipelineNode(constant_node=constant_node))
        elif isinstance(arg, materialization_context.UnboundMaterializationContext):
            node = pipeline_pb2.PipelineNode(materialization_context_node=pipeline_pb2.MaterializationContextNode())
            return PipelineNodeWrapper(node_proto=node)
        else:
            raise errors.InvalidTransformInvocation(transformation_name, arg)

    def add_transformation_input(
        self, input: "PipelineNodeWrapper", arg_index: Optional[int] = None, arg_name: Optional[str] = None
    ):
        assert self.node_proto.HasField(
            "transformation_node"
        ), "add_transformation_input should only be used with Transformation Nodes."
        assert (arg_index is None) != (arg_name is None), "Exactly one of arg_index or arg_name should be set."
        input_proto = pipeline_pb2.Input(
            arg_index=arg_index,
            arg_name=arg_name,
            node=input.node_proto,
        )
        self.node_proto.transformation_node.inputs.append(input_proto)
        self.transformations.update(input.transformations)


@attrs.define(eq=False)
class Transformation(base_tecton_object.BaseTectonObject):
    """A Tecton Transformation. Transformations are used encapsulate and share transformation logic between Feature Views.

    Use the :py:func:`tecton.transformation` decorator to create a Transformation.
    """

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied
    # and fetched from the Tecton backend.
    _args: transformation__args_proto.TransformationArgs = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    # A transformation spec, i.e. a dataclass representation of the Tecton object that is used in most functional
    # use cases, e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e.
    # applied objects fetched from the backend, are assumed valid.
    _spec: Optional[specs.TransformationSpec] = attrs.field(repr=False)

    # The user function for this transformation. Only set if this object was defined locally. It is needed to create
    # the Transformation spec from args.
    _user_function: Optional[Callable] = attrs.field(repr=False)

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str],
        tags: Optional[Dict[str, str]],
        owner: Optional[str],
        prevent_destroy: bool,
        mode: str,
        user_function: Callable[..., Union[str, "pyspark.sql.DataFrame"]],
        options: Optional[Dict[str, str]] = None,
    ):
        """Creates a new Transformation. Use the ``@transformation`` decorator to create a Transformation instead of directly
        using this constructor.

        :param name: A unique name of the Transformation.
        :param description: A human-readable description.
        :param tags: Tags associated with this Tecton Transformation (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply.
        :param mode: The transformation mode. Valid values are "spark_sql", "pyspark", "snowflake_sql", "snowpark",
            "python", or "pandas".
        :param user_function: The user function for this transformation.
        :param options: Additional options to configure the Transformation. Used for advanced use cases and beta features.
        """

        if function_serialization.should_serialize_function(user_function):
            serialized_user_function = function_serialization.to_proto(user_function)
        else:
            serialized_user_function = None

        args = transformation__args_proto.TransformationArgs(
            transformation_id=id_helper.IdHelper.generate_id(),
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            info=basic_info_pb2.BasicInfo(name=name, description=description, owner=owner, tags=tags),
            prevent_destroy=prevent_destroy,
            transformation_mode=get_transformation_mode_enum(mode, name),
            user_function=serialized_user_function,
            options=options,
        )

        source_info = cli_common.construct_fco_source_info(args.transformation_id)
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.transformation_id)

        self.__attrs_init__(
            info=info,
            spec=None,
            args=args,
            source_info=source_info,
            user_function=user_function,
        )
        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.TransformationSpec) -> "Transformation":
        """Create a Transformation from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None, user_function=None)
        return obj

    @sdk_decorators.assert_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(transformation=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                transformation=validator_pb2.TransformationValidationArgs(
                    args=self._args,
                )
            )
        else:
            return self._spec.validation_args

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    def __call__(self, *args, **kwargs) -> PipelineNodeWrapper:
        """Override the user defined transformation function.

        Returns a PipelineNode for this transformation which is used to construct the pipelines for feature views."""
        node_wrapper = PipelineNodeWrapper(
            node_proto=pipeline_pb2.PipelineNode(
                transformation_node=pipeline_pb2.TransformationNode(transformation_id=self.info._id_proto)
            ),
            transformations={self},
        )
        user_function = self._spec.user_function if self._spec is not None else self._user_function

        try:
            bound_user_function = signature(user_function).bind(*args, **kwargs)
        except TypeError as e:
            msg = f"while binding inputs to function {self.info.name}, TypeError: {e}"
            raise TypeError(msg)

        materialization_context_count = 0
        # Construct input nodes from args for the user function
        for i, arg in enumerate(args):
            input_node_wrapper = PipelineNodeWrapper.create_from_arg(arg, self.info.name)
            node_wrapper.add_transformation_input(input_node_wrapper, arg_index=i)
            if isinstance(arg, materialization_context.UnboundMaterializationContext):
                materialization_context_count += 1

        # Construct input nodes from kwargs for the user function
        for arg_name, arg in kwargs.items():
            input_node_wrapper = PipelineNodeWrapper.create_from_arg(arg, self.info.name)
            node_wrapper.add_transformation_input(input_node_wrapper, arg_name=arg_name)
            if isinstance(arg, materialization_context.UnboundMaterializationContext):
                materialization_context_count += 1

        # Construct input nodes for default params for the user function
        for param in signature(user_function).parameters.values():
            if isinstance(param.default, materialization_context.UnboundMaterializationContext):
                if param.name in bound_user_function.arguments:
                    # the user passed in context explicitly, so no need to double register
                    continue
                input_node_wrapper = PipelineNodeWrapper.create_from_arg(param.default, self.info.name)
                node_wrapper.add_transformation_input(input_node_wrapper, arg_name=param.name)
                materialization_context_count += 1
            elif param.default is materialization_context:
                msg = "It seems you passed in tecton.materialization_context. Did you mean tecton.materialization_context()?"
                raise Exception(msg)

        if materialization_context_count > 1:
            msg = f"Only 1 materialization_context can be passed into transformation {self.info.name}"
            raise Exception(msg)

        return node_wrapper

    @property
    def transformer(self):
        """The user function for this transformation."""
        if self._spec is None:
            return self._user_function
        return self._spec.user_function

    @property
    def transformation_mode(self) -> TransformationMode:
        if self._spec is None:
            return self._args.transformation_mode
        else:
            return self._spec.transformation_mode

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
            indentation_level,
        )
        self._spec = specs.TransformationSpec.from_args_proto(self._args, self._user_function)

    def _on_demand_run(self, *inputs: Union[pd.DataFrame, Dict[str, Any]]) -> Union[data_frame.TectonDataFrame, Dict]:
        for _input in inputs:
            if not isinstance(_input, pd.DataFrame) and not isinstance(_input, dict):
                msg = f"Input must be of type pandas.DataFrame or Dict, but was {type(_input)}."
                raise TypeError(msg)

        output = self.transformer(*inputs)
        if isinstance(output, pd.DataFrame):
            return data_frame.TectonDataFrame._create(output)
        else:
            return output

    @sdk_decorators.sdk_public_method
    @typechecked
    def run(
        self,
        *inputs: Union[
            "pd.DataFrame",
            "pd.Series",
            "data_frame.TectonDataFrame",
            "pyspark.sql.DataFrame",
            Dict,
            spark_api.CONST_TYPE,
        ],
        context: materialization_context.BaseMaterializationContext = None,
    ) -> Union[data_frame.TectonDataFrame, Dict]:
        """Run the transformation against inputs.

        Currently, this method only supports spark_sql, pyspark, and pandas modes.

        :param inputs: positional arguments to the transformation function. For PySpark and SQL transformations,
                       these are either ``pandas.DataFrame`` or ``pyspark.sql.DataFrame`` objects.
                       For on-demand transformations, these are ``pandas.Dataframe`` objects.
        :param context: An optional materialization context object.
        """
        # TODO(TEC-11512): add support for other modes
        if self.transformation_mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_SPARK_SQL:
            return spark_api.run_transformation_mode_spark_sql(
                *inputs, transformer=self.transformer, context=context, transformation_name=self.info.name
            )
        elif self.transformation_mode == transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYSPARK:
            return spark_api.run_transformation_mode_pyspark(*inputs, transformer=self.transformer, context=context)
        elif self.transformation_mode in {
            transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PANDAS,
            transformation__args_proto.TransformationMode.TRANSFORMATION_MODE_PYTHON,
        }:
            return self._on_demand_run(*inputs)
        msg = f"{self.transformation_mode} does not support `run(...)`"
        raise RuntimeError(msg)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self):
        """Displays a human readable summary of this Transformation."""
        request = metadata_service_pb2.GetTransformationSummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetTransformationSummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.assert_local_object
    def _create_unvalidated_spec(self) -> specs.TransformationSpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        return specs.TransformationSpec.from_args_proto(self._args, self._user_function)


@typechecked
def transformation(
    mode: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    options: Optional[Dict[str, str]] = None,
):
    """Declares a Transformation that wraps a user function. Transformations are assembled in a pipeline function of a Feature View.

    :param mode: The mode for this transformation must be one of "spark_sql", "pyspark", "snowflake_sql", "snowpark", "pandas" or "python".
    :param name: Unique, human friendly name that identifies the Transformation. Defaults to the function name.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be set to
        False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
        only enforced in live (i.e. non-dev) workspaces.
    :param options: Additional options to configure the Transformation. Used for advanced use cases and beta features.
    :return: A wrapped transformation

    Examples of Spark SQL, PySpark, Pandas, and Python transformation declarations:

        .. code-block:: python

            from tecton import transformation
            from pyspark.sql import DataFrame
            import pandas as pd

            # Create a Spark SQL transformation.
            @transformation(mode="spark_sql",
                            description="Create new column by splitting the string in an existing column")
            def str_split(input_data, column_to_split, new_column_name, delimiter):
                return f'''
                    SELECT
                        *,
                        split({column_to_split}, {delimiter}) AS {new_column_name}
                    FROM {input_data}
                '''

            # Create a PySpark transformation.
            @transformation(mode="pyspark",
                            description="Add a new column 'user_has_good_credit' if score is > 670")
            def user_has_good_credit_transformation(credit_scores):
                from pyspark.sql import functions as F

                (df = credit_scores.withColumn("user_has_good_credit",
                    F.when(credit_scores["credit_score"] > 670, 1).otherwise(0))
                return df.select("user_id", df["date"].alias("timestamp"), "user_has_good_credit") )

            # Create a Pandas transformation.
            @transformation(mode="pandas",
                            description="Whether the transaction amount is considered high (over $10000)")
            def transaction_amount_is_high(transaction_request):
                import pandas as pd

                df = pd.DataFrame()
                df['amount_is_high'] = (request['amount'] >= 10000).astype('int64')
                return df

            @transformation(mode="python",
                            description="Whether the transaction amount is considered high (over $10000)")
            # Create a Python transformation.
            def transaction_amount_is_high(transaction_request):

                result = {}
                result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
                return result
    """

    def decorator(user_function):
        transform_name = name or user_function.__name__
        transform = Transformation(
            name=transform_name,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            mode=mode,
            user_function=user_function,
            options=options,
        )

        return transform

    return decorator
