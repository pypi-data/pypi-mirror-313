import logging
import tempfile
from typing import TYPE_CHECKING
from typing import Optional

from tecton_core import _gen_version
from tecton_core import conf


if TYPE_CHECKING:
    from duckdb import DuckDBPyConnection
logger = logging.getLogger(__name__)


def get_ext_version():
    return "latest" if _gen_version.VERSION == "99.99.99" else _gen_version.VERSION


class DuckDBContext:
    """
    Singleton holder of DuckDB connection.
    """

    _current_context_instance = None

    def __init__(self, connection: "DuckDBPyConnection", home_dir_override: Optional[str] = None) -> None:
        self._connection = connection
        # Needed to export to S3
        if home_dir_override:
            connection.sql(f"SET home_directory='{home_dir_override}'")
        connection.sql("INSTALL httpfs;")
        connection.sql("LOAD httpfs;")
        connection.sql(f"SET http_retries='{conf.get_or_raise('DUCKDB_HTTP_RETRIES')}'")

        if conf.get_bool("DUCKDB_DISK_SPILLING_ENABLED"):
            # The directory will be deleted when the TemporaryDirectory object is destroyed even if we don't call
            # __enter__. This means as long as we store the object somewhere the directory will live as the context and
            # will be cleaned up at interpreter exit.
            self._temporary_directory = tempfile.TemporaryDirectory(suffix=".tecton_duckdb")
            connection.sql(f"SET temp_directory = '{self._temporary_directory.name}'")
        else:
            self._temporary_directory = None
        duckdb_memory_limit = conf.get_or_none("DUCKDB_MEMORY_LIMIT")
        if duckdb_memory_limit:
            if conf.get_bool("DUCKDB_DEBUG"):
                print(f"Setting duckdb memory limit to {duckdb_memory_limit}")

            connection.sql(f"SET memory_limit='{duckdb_memory_limit}'")

        num_duckdb_threads = conf.get_or_none("DUCKDB_NTHREADS")
        if num_duckdb_threads:
            connection.sql(f"SET threads TO {num_duckdb_threads};")
            if conf.get_bool("DUCKDB_DEBUG"):
                print(f"Setting duckdb threads to {num_duckdb_threads}")
        # This is a workaround for pypika not supporting the // (integer division) operator
        connection.sql("CREATE OR REPLACE MACRO _tecton_int_div(a, b) AS a // b")
        extension_repo = conf.get_or_none("DUCKDB_EXTENSION_REPO")
        if extension_repo:
            versioned_extension_repo = extension_repo.format(version=get_ext_version())
            connection.sql(f"SET custom_extension_repository='{versioned_extension_repo}'")
            if conf.get_bool("DUCKDB_ALLOW_CACHE_EXTENSION"):
                # Allow using local cached version of extension
                connection.sql("INSTALL tecton")
            else:
                # Otherwise, always download the latest version of the duckdb extension
                # from the repo.
                connection.sql("FORCE INSTALL tecton")
            connection.sql("LOAD tecton")

        connection.sql("SET TimeZone='UTC'")

    def get_connection(self):
        return self._connection

    @classmethod
    def get_instance(cls, home_dir_override: Optional[str] = None) -> "DuckDBContext":
        """
        Get the singleton instance of DuckDBContext.
        """
        if cls._current_context_instance is None:
            try:
                import duckdb
            except ImportError:
                msg = (
                    "Couldn't initialize Rift compute. "
                    "To use Rift install all Rift dependencies first by executing `pip install tecton[rift]`."
                )
                raise RuntimeError(msg)

            conn_config = {}
            if conf.get_or_none("DUCKDB_EXTENSION_REPO"):
                conn_config["allow_unsigned_extensions"] = "true"

            if conf.get_bool("DUCKDB_PERSIST_DB"):
                conn = duckdb.connect("duckdb.db", config=conn_config)
            else:
                conn = duckdb.connect(config=conn_config)

            cls._current_context_instance = cls(conn, home_dir_override)

        return cls._current_context_instance
