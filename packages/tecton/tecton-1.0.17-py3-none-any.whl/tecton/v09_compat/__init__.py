"""V09 Module for backwards compatibility.

This module contains variants of Tecton classes and functions compatible with the 0.9 SDK. It's used to
ease upgrades from 0.9 to 1.0. Users may replace `from tecton import *` with `from tecton.v09_compat import *` as an
initial step when upgrading to 1.0. Then users may update their repository incrementally.
"""

from tecton._internals.find_spark import find_spark as __find_spark


__initializing__ = True


__find_spark()

# ruff: noqa: F401 E402
from tecton import version as __version_lib
from tecton._internals.materialization_api import MaterializationAttempt
from tecton._internals.materialization_api import MaterializationJob
from tecton.fco_listers import list_workspaces
from tecton.framework.configs import BigQueryConfig
from tecton.framework.configs import BigtableConfig
from tecton.framework.configs import CacheConfig
from tecton.framework.configs import DatabricksClusterConfig
from tecton.framework.configs import DatabricksJsonClusterConfig
from tecton.framework.configs import DataprocJsonClusterConfig
from tecton.framework.configs import DatetimePartitionColumn
from tecton.framework.configs import DeltaConfig
from tecton.framework.configs import DynamoConfig
from tecton.framework.configs import EMRClusterConfig
from tecton.framework.configs import EMRJsonClusterConfig
from tecton.framework.configs import FileConfig
from tecton.framework.configs import HiveConfig
from tecton.framework.configs import KafkaConfig
from tecton.framework.configs import KafkaOutputStream
from tecton.framework.configs import KinesisConfig
from tecton.framework.configs import KinesisOutputStream
from tecton.framework.configs import LifetimeWindow
from tecton.framework.configs import LoggingConfig
from tecton.framework.configs import OfflineStoreConfig
from tecton.framework.configs import PandasBatchConfig
from tecton.framework.configs import ParquetConfig
from tecton.framework.configs import PushConfig
from tecton.framework.configs import RedisConfig
from tecton.framework.configs import RedshiftConfig
from tecton.framework.configs import RequestSource
from tecton.framework.configs import RiftBatchConfig
from tecton.framework.configs import Secret
from tecton.framework.configs import SnowflakeConfig
from tecton.framework.configs import SparkBatchConfig
from tecton.framework.configs import SparkStreamConfig
from tecton.framework.configs import TimeWindow
from tecton.framework.configs import TimeWindowSeries
from tecton.framework.configs import UnityCatalogAccessMode
from tecton.framework.configs import UnityConfig
from tecton.framework.configs import pandas_batch_config
from tecton.framework.configs import spark_batch_config
from tecton.framework.configs import spark_stream_config
from tecton.framework.data_frame import DataFrame
from tecton.framework.data_frame import FeatureVector
from tecton.framework.data_frame import TectonDataFrame
from tecton.framework.data_source import FilteredSource
from tecton.framework.dataset import Dataset
from tecton.framework.feature_view import BatchTriggerType
from tecton.framework.feature_view import FeatureReference
from tecton.framework.feature_view import FeatureView
from tecton.framework.feature_view import MaterializedFeatureView
from tecton.framework.feature_view import StreamProcessingMode
from tecton.framework.model_config import ModelConfig
from tecton.framework.transformation import const
from tecton.framework.utils import PANDAS_MODE
from tecton.framework.utils import PYSPARK_MODE
from tecton.framework.utils import PYTHON_MODE
from tecton.framework.utils import SNOWFLAKE_SQL_MODE
from tecton.framework.utils import SNOWPARK_MODE
from tecton.framework.utils import SPARK_SQL_MODE
from tecton.framework.workspace import Workspace
from tecton.framework.workspace import get_data_source
from tecton.framework.workspace import get_entity
from tecton.framework.workspace import get_feature_service
from tecton.framework.workspace import get_feature_table
from tecton.framework.workspace import get_feature_view
from tecton.framework.workspace import get_transformation
from tecton.framework.workspace import get_workspace
from tecton.identities.credentials import clear_credentials
from tecton.identities.credentials import complete_login
from tecton.identities.credentials import get_caller_identity
from tecton.identities.credentials import login
from tecton.identities.credentials import login_with_code
from tecton.identities.credentials import logout
from tecton.identities.credentials import set_credentials
from tecton.identities.credentials import test_credentials
from tecton.identities.credentials import who_am_i
from tecton.tecton_context import get_current_workspace
from tecton.tecton_context import set_tecton_spark_session
from tecton.v09_compat.configs import Aggregation
from tecton.v09_compat.framework import BatchFeatureView
from tecton.v09_compat.framework import BatchSource
from tecton.v09_compat.framework import DataSource
from tecton.v09_compat.framework import Entity
from tecton.v09_compat.framework import FeatureService
from tecton.v09_compat.framework import FeatureTable
from tecton.v09_compat.framework import OnDemandFeatureView
from tecton.v09_compat.framework import PushSource
from tecton.v09_compat.framework import StreamFeatureView
from tecton.v09_compat.framework import StreamSource
from tecton.v09_compat.framework import Transformation
from tecton.v09_compat.framework import batch_feature_view
from tecton.v09_compat.framework import on_demand_feature_view
from tecton.v09_compat.framework import stream_feature_view
from tecton.v09_compat.framework import transformation
from tecton.v09_compat.workspace import ValidationMode
from tecton.v09_compat.workspace import set_validation_mode
from tecton_core import conf
from tecton_core.compute_mode import ComputeMode
from tecton_core.filter_context import FilterContext
from tecton_core.materialization_context import materialization_context
from tecton_core.online_serving_index import OnlineServingIndex


__version__ = __version_lib.get_version()
__initializing__ = False
