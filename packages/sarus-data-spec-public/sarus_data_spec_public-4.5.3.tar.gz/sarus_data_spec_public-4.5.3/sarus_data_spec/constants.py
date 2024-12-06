from enum import Enum

from sarus_data_spec import typing as st

DATA = "sarus_data"
PU_COLUMN = "sarus_privacy_unit"
PID_COLUMN = PU_COLUMN
WEIGHTS = "sarus_weights"
PUBLIC = "sarus_is_public"

# constants used in protection stored in each struct
NON_EMPTY_PRIVACY_UNIT_TRACKING_PATHS = "non_zero_protected_values"
STRUCT_KIND = "merge_paths"
TO_MERGE = "fks_for_merging"

# protection constants for paths in types
LIST_VALUES = "sarus_list_values"
ARRAY_VALUES = "sarus_array_values"
OPTIONAL_VALUE = "sarus_optional_value"
CONSTRAINED_VALUE = "sarus_constrained_value"


class StructKind(Enum):
    HAS_PU = "0"
    NO_PU = "1"
    TO_MERGE = "2"


# constants for type properties
TEXT_MIN_LENGTH = "min_length"
TEXT_MAX_LENGTH = "max_length"
TEXT_CHARSET = "text_char_set"
TEXT_EXACT_CHARSET = "FullUserInput"
TEXT_ALPHABET_NAME = "text_alphabet_name"
SQL_MAPPING = "sql_mapping"
FLOAT_DISTRIBUTION = "distribution_model"
FLOAT_DIST_PARAMS = "parameters"
MAX_MAX_MULT = "max_max_multiplicity"
MULTIPLICITY = "multiplicity"
RECOMPUTE_TYPE_RANGES = "recompute_type_ranges"

# constants for dataset properties
DATASET_SLUGNAME = "slugname"

# constants for schema properties
PRIMARY_KEYS = "primary_keys"
FOREIGN_KEYS = "foreign_keys"

# names when transforming datetime type in struct
DATETIME_YEAR = "year"
DATETIME_MONTH = "month"
DATETIME_DAY = "day"
DATETIME_HOUR = "hour"
DATETIME_MINUTES = "minutes"
DATETIME_SECONDS = "seconds"


# sql, to_sql, push_sql status
TO_SQL_TASK = "sql_preparation"
SQL_TASK = "sql"
PUSH_SQL_TASK = "push_sql"

# Big Data Status
BIG_DATA_TASK = "big_data_dataset"
BIG_DATA_THRESHOLD = "threshold"
IS_BIG_DATA = "is_big_data"
DATASET_N_LINES = "dataset_n_lines"
DATASET_N_BYTES = "dataset_n_bytes"
THRESHOLD_TYPE = "threshold_type"
SAMPLE_SIZE_N_LINES = "sample_size_n_lines"

# Caching Status
TO_PARQUET_TASK = "to_parquet"
CACHE = TO_PARQUET_TASK
CACHE_PATH = "path"
COMPUTATION_QUEUED = "computation_queued"
TO_SQL_CACHING_TASK = "to_sql_caching"
SQL_CACHING_URI = "sql_caching_uri"
TABLE_MAPPING = "table_mapping"
EXTENDED_TABLE_MAPPING = "extended_table_mapping"

# Caching infos for scalar
CACHE_TYPE = "cache_type"
CACHE_PROTO = "cache_proto"
SCALAR_TASK = "scalar_value"


class ScalarCaching(Enum):
    PICKLE = "pickle"
    PROTO = "protobuf"
    TRAIN_STATE = "train_state"


# Attributes Status
SCHEMA_TASK = "schema"
SIZE_TASK = "size"
MULTIPLICITY_TASK = "multiplicity"
BOUNDS_TASK = "bounds"
MARGINALS_TASK = "marginals"
ARROW_TASK = "arrow"
PRIVACY_UNIT_TRACKING_TASK = "privacy_unit_tracking_task"
USER_SETTINGS_TASK = "user_settings_task"
PUBLIC_TASK = "public_task"
CACHE_SCALAR_TASK = "cache_scalar"
QB_TASK = "query_builder"
LINKS_TASK = "links_statistics"
SYNTHETIC_TASK = "synthetic"
PROCESSING_INFO = "processing_info"


# Privacy
PUP_TOKEN = "pup_token"
NO_TOKEN = "no_token"
IS_PUBLIC = "is_public"
IS_SYNTHETIC = "is_synthetic"
PRIVACY_LIMIT = "privacy_limit"
CONSTRAINT_KIND = "constraint_kind"
BEST_ALTERNATIVE = "best_alternative"

# QUERYBUILDER
QUERIES = "queries"

# Attributes names
PRIVATE_QUERY = "private_query"
IS_REMOTE = "is_remote"
VARIANT_UUID = "variant_uuid"
RELATIONSHIP_SPEC = "relationship_spec"
VALIDATED_TYPE = "validated_type"
IS_VALID = "is_valid"
IS_DP = "is_dp"
IS_DP_ABLE = "is_dp_able"
IS_DP_WRITABLE = "is_dp_writable"
IS_PUP_ABLE = "is_pup_able"
IS_PUP_WRITABLE = "is_pup_writable"
IS_PUBLISHED = "is_published"
IS_PUBLISHABLE = "is_publishable"
IS_BIG_DATA_COMPUTABLE = "is_big_data_computable"

# SYNTHETIC DATA
MODEL_PROPERTIES = "model_properties"
SYNTHETIC_MODEL = "sarus_synthetic_model"


class SyntheticDataSettings:
    """Namespace for SD generation settings"""

    BATCH_SIZE = 64
    EPOCHS = 10


# map between sqlalchemy dialect names to sarus notion of dialects
SQLALCHEMY_DIALECT_MAP = {
    "postgresql": st.SQLDialect.POSTGRES,
    "mongodb": st.SQLDialect.MONGODB,
    "mssql": st.SQLDialect.SQL_SERVER,
    "mysql": st.SQLDialect.MY_SQL,
    "sqlite": st.SQLDialect.SQLLITE,
    "oracle": st.SQLDialect.ORACLE,
    "bigquery": st.SQLDialect.BIG_QUERY,
    "redshift": st.SQLDialect.REDSHIFT,
    "hive": st.SQLDialect.HIVE,
    "databricks": st.SQLDialect.DATABRICKS,
}

# Possible values
POSSIBLE_VALUES_LENGTH = "possible_values_length"
POSSIBLE_VALUES = "possible_values"

# Model checkpoints
TRAIN_STATE = "state"
MODEL_NAME = "model_name"
PROMPT = "text"

# relationship spec
SHARED_ID_SPACES = "shared-id-spaces"


# sarus default output (for empty mock/synthetic)
SARUS_DEFAULT_OUTPUT = "sarus_default_output"
