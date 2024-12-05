from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attrs
from typeguard import typechecked

from tecton._internals import display
from tecton._internals import metadata_service
from tecton._internals import sdk_decorators
from tecton._internals import validations_api
from tecton.framework import base_tecton_object
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import specs
from tecton_proto.args import basic_info_pb2
from tecton_proto.args import entity_pb2 as entity__args_pb2
from tecton_proto.args import fco_args_pb2
from tecton_proto.common import fco_locator_pb2
from tecton_proto.metadataservice import metadata_service_pb2
from tecton_proto.validation import validator_pb2


@attrs.define(eq=False)
class Entity(base_tecton_object.BaseTectonObject):
    """A Tecton Entity, used to organize and join features.

    An Entity is a class that represents an Entity that is being modeled in Tecton. Entities are used to index and
    organize features - a :class:`FeatureView` contains at least one Entity.

    Entities contain metadata about *join keys*, which represent the columns that are used to join features together.

    Example of an Entity declaration:

    .. code-block:: python

        from tecton import Entity

        customer = Entity(
            name='customer',
            join_keys=['customer_id'],
            description='A customer subscribing to a Sports TV subscription service',
            owner='matt@tecton.ai',
            tags={'release': 'development'}
    """

    # An entity spec, i.e. a dataclass representation of the Tecton object that is used in most functional use cases,
    # e.g. constructing queries. Set only after the object has been validated. Remote objects, i.e. applied objects
    # fetched from the backend, are assumed valid.
    _spec: Optional[specs.EntitySpec] = attrs.field(repr=False)

    # A Tecton "args" proto. Only set if this object was defined locally, i.e. this object was not applied and fetched
    # from the Tecton backend.
    _args: Optional[entity__args_pb2.EntityArgs] = attrs.field(repr=False, on_setattr=attrs.setters.frozen)

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        join_keys: Optional[Union[str, List[str]]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Declare a new Entity.

        :param name: Unique name for the new entity.
        :param description: Short description of the new entity.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param join_keys: Names of columns that uniquely identify the entity in FeatureView's SQL statement
            for which features should be aggregated. Defaults to using ``name`` as the entity's join key.
        :param options: Additional options to configure the Entity. Used for advanced use cases and beta features.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        from tecton.cli import repo_utils as cli_common

        if not join_keys:
            resolved_join_keys = [name]
        elif isinstance(join_keys, str):
            resolved_join_keys = [join_keys]
        else:
            resolved_join_keys = join_keys

        args = entity__args_pb2.EntityArgs(
            entity_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            join_keys=resolved_join_keys,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.entity_id)
        source_info = cli_common.construct_fco_source_info(args.entity_id)
        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info)
        base_tecton_object._register_local_object(self)

    @classmethod
    @typechecked
    def _from_spec(cls, spec: specs.EntitySpec) -> "Entity":
        """Create an Entity from directly from a spec. Specs are assumed valid and will not be re-validated."""
        info = base_tecton_object.TectonObjectInfo.from_spec(spec)
        obj = cls.__new__(cls)  # Instantiate the object. Does not call init.
        obj.__attrs_init__(info=info, spec=spec, args=None, source_info=None)
        return obj

    @sdk_decorators.assert_local_object
    def _build_args(self) -> fco_args_pb2.FcoArgs:
        return fco_args_pb2.FcoArgs(entity=self._args)

    def _build_fco_validation_args(self) -> validator_pb2.FcoValidationArgs:
        if self.info._is_local_object:
            return validator_pb2.FcoValidationArgs(
                entity=validator_pb2.EntityValidationArgs(
                    args=self._args,
                )
            )
        else:
            return self._spec.validation_args

    @property
    def _is_valid(self) -> bool:
        return self._spec is not None

    @property
    def join_keys(self) -> List[str]:
        """Join keys of the entity."""
        if self._spec is None:
            return list(self._args.join_keys)
        return list(self._spec.join_keys)

    def _validate(self, indentation_level: int = 0) -> None:
        if self._is_valid:
            return

        validations_api.run_backend_validation_and_assert_valid(
            self,
            validator_pb2.ValidationRequest(validation_args=[self._build_fco_validation_args()]),
            indentation_level,
        )

        self._spec = specs.EntitySpec.from_args_proto(self._args)

    @sdk_decorators.sdk_public_method
    @sdk_decorators.assert_remote_object
    def summary(self) -> display.Displayable:
        """Displays a human readable summary of this Feature View."""
        request = metadata_service_pb2.GetEntitySummaryRequest(
            fco_locator=fco_locator_pb2.FcoLocator(id=self._spec.id_proto, workspace=self._spec.workspace)
        )
        response = metadata_service.instance().GetEntitySummary(request)
        return display.Displayable.from_fco_summary(response.fco_summary)

    @sdk_decorators.assert_local_object
    def _create_unvalidated_spec(self) -> specs.EntitySpec:
        """Create an unvalidated spec. Used for user unit testing, where backend validation is unavailable."""
        return specs.EntitySpec.from_args_proto(self._args)
