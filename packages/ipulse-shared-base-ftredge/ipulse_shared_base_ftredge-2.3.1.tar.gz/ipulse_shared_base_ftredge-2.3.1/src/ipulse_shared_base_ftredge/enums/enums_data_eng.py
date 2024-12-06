# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import Enum


class AttributeType(Enum):
    RECENT_DATE = "recent_date"
    RECENT_TIMESTAMP = "recent_timestamp"
    RECENT_DATETIME = "recent_datetime"
    OLDEST_DATE = "oldest_date"
    OLDEST_TIMESTAMP = "oldest_timestamp"
    OLDEST_DATETIME = "oldest_datetime"
    MAX_VALUE = "max_value"
    MIN_VALUE = "min_value"
    TOTAL_COUNT = "total_count"
    TOTAL_SUM = "total_sum"
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    STANDARD_DEVIATION = "standard_deviation"
    NB_FIELDS_PER_RECORDS = "nb_fields_per_records"
    def __str__(self):
        return self.value



    
class DataPrimaryCategory(Enum):
    SIMULATION="simulation" # Simulation data, based on models and simulations
    HISTORIC = "historic" # Historical data, usually accurate and complete
    REALTIME="realtime" # Real-time data, not always certain, can have error
    ANALYTICS="analytics" # Analytical data and modelling, derived from historical and prediction data. Normally shall be making Human readable sense. vs. Features
    FEATURES="features" # Feature data, used for training models
    PREDICTIVE="predictive" # Predictive data, based on models and simulations
    def __str__(self):
        return self.value

class DataState(Enum):
    RAW = "raw"
    FORMATTED= "formatted"
    CLEANED = "cleaned"
    PROCESSED = "processed"
    SIMULATED = "simulated"
    ANALYZED = "analyzed"
    VALIDATED = "validated"
    INVALID = "invalid"

    def __str__(self):
        return self.value

class DatasetScope(Enum):
    FULL = "full_dataset"
    LATEST= "latest_record"
    INCREMENTAL = "incremental_dataset"
    BACKFILLING = "backfilling_dataset"
    PARTIAL = "partial_dataset"
    FILTERED = "filtered_dataset"
    SOURCING_METADATA = "sourcing_metadata"
    DATASET_METADATA = "dataset_metadata"
    CHANGE_METADATA = "change_metadata"
    UNKNOWN = "unknown_dataset_scope"

    def __str__(self):
        return self.value


class DataSourceType(Enum):
    # --- General ---
    API = "api"
    RPC = "rpc"
    GRPC = "grpc"
    WEBSITE = "website"
    # --SQL Databases--
    ORACLE = "oracle"
    POSTGRESQL = "postgresql"
    SQLSERVER = "sqlserver"
    MYSQL = "mysql"
    BIGQUERY = "bigquery"
    SNOWFLAKE = "snowflake"
    REDSHIFT = "redshift"
    ATHENA = "athena"
    # --NOSQL Databases--
    MONGODB = "mongodb"
    REDIS = "redis"
    CASSANDRA = "cassandra"
    NEO4J = "neo4j"
    FIRESTORE = "firestore"
    DYNAMODB = "dynamodb"
    # --NEWSQL Databases--
    COCKROACHDB = "cockroachdb"
    SPANNER = "spanner"
    # --- Messaging ---
    MESSAGING_KAFKA = "messaging_kafka"
    MESSAGING_SQS = "messaging_sqs"
    MESSAGING_PUBSUB = "messaging_pubsub"
    # --- Real-time Communication ---
    REALTIME_WEBSOCKET = "websocket"
     # --- Notifications ---
    NOTIFICATION_WEBHOOK = "webhook"
    # --- Storage ---
    LOCAL_STORAGE = "local_storage"
    INMEMORY = "inmemory"
    GCS = "gcs"
    S3 = "s3"
    AZURE_BLOB = "azure_blob"
    HDFS = "hdfs"

    SECRET_MANAGER="secret_manager"

    # --- Files ---
    FILE = "file"
    FILE_JSON = ".json"
    FILE_CSV = ".csv"
    FILE_EXCEL = ".xlsx"
    FILE_TXT = ".txt"
    FILE_PDF = ".pdf"
    FILE_PARQUET = ".parquet"
    FILE_AVRO = ".avro"
    FILE_WORD = ".docx"
    FILE_PPT = ".pptx"
    FILE_HTML = ".html"
    FILE_MARKDOWN = ".md"
    FILE_XML = ".xml"
    FILE_YAML = ".yaml"
    FILE_TOML = ".toml"
    FILE_JPG = ".jpg"
    FILE_JPEG = ".jpeg"
    FILE_PNG = ".png"
    FILE_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
    FILE_VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"]
    FILE_AUDIO_EXTENSIONS = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"]


    def __str__(self):
        return self.value

class PipelineTriggerType(Enum):
    MANUAL = "manual"
    SCHEDULER = "scheduler"
    SCHEDULER_MAIN = "scheduler_main"
    SCHEDULER_FALLBACK = "scheduler_fallback"
    SCHEDULER_RETRY = "scheduler_retry"
    SCHEDULER_VERIFICATION = "scheduler_verification"
    EVENT_GCS_UPLOAD= "event_gcs_upload"
    EVENT_PUBSUB= "event_pubsub"
    ANOTHER_PIPELINE = "another_pipeline"

    def __str__(self):
        return self.value


class DataActionType(Enum):
    # --- Read Actions ---
    SOURCE="source" # For reading data from source
    QUERY = "query" # For databases or systems that support queries
    SCAN = "scan" # For reading all data sequentially (e.g., files)
    READ= "read" # For general read operations
    READ_FROM_FILE = "read_from_file"
    READ_FROM_SECRET_MANAGER = "read_from_secret_manager"
    HTTP_GET= "http_get" # For getting a single record
    IMPORT = "import"
    # --- Transform Actions ---
    NO_CHANGE = "no_change"
    TRANSFORM = "transform"
    PREPROCESS = "preprocess"
    ENRICH = "enrich"
    NORMALIZE = "normalize"
    JOIN = "join"
    AGGREGATE = "aggregate"
    FILTER = "filter"
    SORT = "sort"
    GROUP = "group"
    # --- Write Actions ---
    
    HTTP_POST= "http_post" # For creating new records
    HTTP_PUT= "http_put"
    HTTP_PATCH= "http_patch"
    WRITE = "write"
    WRITE_TO_FILE = "write_to_file"
    APPEND = "append"
    UPSERT = "upsert"
    INSERT = "insert"
    OVERWRITE = "overwrite"
    INCREMENT = "increment"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    COPY = "copy"
    MERGE = "merge" ## For merging data, combines INSERT, UPDATE, DELETE operations
    MERGE_UPSERT = "merge_upsert" ## For merging data, combines INSERT, UPDATE, DELETE operations
    BIGQUERY_WRITE_APPEND = "bigquery_write_append" # For emptying table and writing data, specific to BIGQUERY
    BIGQUERY_WRITE_TRUNCATE = "bigquery_write_truncate" #For writing data to empty table, fails if table not empty, specific to BIGQUERY
    BIGQUERY_WRITE_EMPTY = "bigquery_write_empty" # For updating or inserting records
    # --- Create Actions ---
    CREATE_TABLE = "create_table"
    CREATE_TABLE_FROM_JSON = "create_table_from_json"
    CREATE_DATABASE = "create_database"
    CREATE_COLLECTION = "create_collection"
    CREATE_INDEX = "create_index"
    CREATE_SCHEMA = "create_schema"
    CREATE_MODEL = "create_model"
    CREATE_VIEW = "create_view"
    # --- Alter Actions ---
    ALTER_TABLE = "alter_table"
    ALTER_DATABASE = "alter_database"
    ALTER_COLLECTION = "alter_collection"
    ALTER_INDEX = "alter_index"
    ALTER_SCHEMA = "alter_schema"
    ALTER_MODEL = "alter_model"
    ALTER_VIEW = "alter_view"
    # --- DROP/DELETE Actions ---
    DROP_TABLE = "drop_table"
    DELETE_TABLE = "delete_table"
    DELETE_DATABASE = "drop_database"
    DELETE_COLLECTION = "drop_collection"
    DELETE_INDEX = "drop_index"
    DELETE_SCHEMA = "drop_schema"
    DELETE_MODEL = "drop_model"
    DELETE_VIEW = "drop_view"
    DROP_VIEW = "drop_view"
    # --- Truncate Actions ---
    TRUNCATE_TABLE = "truncate_table"
    TRUNCATE_COLLECTION = "truncate_collection"
    # --- Validate Actions ---
    VALIDATE_SCHEMA = "validate_schema"

    def __str__(self):
        return self.value

class MatchConditionType(Enum):
    EXACT = "exact"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    CONTAINS = "contains"
    REGEX = "regex"
    IN_RANGE = "in_range"
    NOT_IN_RANGE = "not_in_range"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    IN_LIST = "in_list"
    NOT_IN_LIST = "not_in_list"
    ON_FIELD_MATCH = "on_field_match"
    ON_FIELD_EQUAL = "on_field_equal"
    ON_FIELDS_EQUAL_TO = "on_fields_equal_to"
    ON_FIELDS_COMBINATION = "on_fields_combination"
    NOT_APPLICABLE = "not_applicable"

    def __str__(self):
        return self.value


class DuplicationHandling(Enum):
    RAISE_ERROR = "raise_error"
    OVERWRITE = "overwrite"
    INCREMENT = "increment"
    SKIP = "skip"
    SYSTEM_DEFAULT = "system_default"
    ALLOW = "allow" ## applicable for databases allowing this operation i.e. BigQuery 
    MERGE_DEFAULT = "merge_default"
    MERGE_PRESERVE_SOURCE_ON_DUPLICATES = "merge_preserve_source_on_dups"
    MERGE_PRESERVE_TARGET_ON_DUPLICATES = "merge_preserve_target_on_dups"
    MERGE_PRESERVE_BOTH_ON_DUPLICATES = "merge_preserve_both_on_dups"
    MERGE_RAISE_ERROR_ON_DUPLICATES = "merge_raise_error_on_dups"
    MERGE_CUSTOM = "merge_custom"

    def __str__(self):
        return self.value


class DuplicationHandlingStatus(Enum):
    ALLOWED = "allowed"
    RAISED_ERROR = "raised_error"
    SYSTEM_DEFAULT = "system_default"
    OVERWRITTEN = "overwritten"
    SKIPPED = "skipped"
    INCREMENTED = "incremented"
    OPERATION_CANCELLED = "operation_cancelled"
    MERGED = "merged"
    MERGED_PRESERVED_SOURCE = "merged_preserved_source"
    MERGED_PRESERVED_TARGET = "merged_preserved_target"
    MERGED_PRESERVED_BOTH = "merged_preserved_both"
    MERGED_RAISED_ERROR = "merged_raised_error"
    MERGED_CUSTOM = "merged_custom"
    NO_DUPLICATES = "no_duplicates"
    UNKNOWN = "unknown"
    UNEXPECTED_ERROR= "unexpected_error"
    CONDITIONAL_ERROR = "conditional_error"
    NOT_APPLICABLE = "not_applicable"

    def __str__(self):
        return self.value

class CodingLanguage(Enum):
    PYTHON = "python"
    NODEJS = "nodejs"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    REACTJS = "reactjs"

    def __str__(self):
        return self.value


class ExecutionLocation(Enum):
# Add local execution environments
    LOCAL_SCRIPT = "local_script"
    LOCAL_JUPYTER_NOTEBOOK = "local_jupyter_notebook"
    LOCAL_SERVER = "local_server"
    LOCAL_DOCKER = "local_docker"  # Add local Docker environment
    LOCAL_KUBERNETES = "local_kubernetes"  # Add local Kubernetes environment

    LOCAL_GCP_CLOUD_FUNCTION = "local_gcp_cloud_function"
    LOCAL_GCP_CLOUD_RUN = "local_gcp_cloud_run"

# Add GCP execution environments
    CLOUD_GCP_JUPYTER_NOTEBOOK = "cloud_gcp_jupyter_notebook"
    CLOUD_GCP_CLOUD_FUNCTION = "cloud_gcp_cloud_function"
    CLOUD_GCP_CLOUD_RUN = "cloud_gcp_cloud_run"
    CLOUD_GCP_COMPUTE_ENGINE = "cloud_gcp_compute_engine"
    CLOUD_GCP_DATAPROC = "cloud_gcp_dataproc"
    CLOUD_GCP_DATAFLOW = "cloud_gcp_dataflow"
    CLOUD_GCP_BIGQUERY = "cloud_gcp_bigquery"
# Add AWS execution environments
    CLOUD_AWS_LAMBDA = "cloud_aws_lambda"
    CLOUD_AWS_EC2 = "cloud_aws_ec2"
    CLOUD_AWS_EMR = "cloud_aws_emr"
    CLOUD_AWS_GLUE = "cloud_aws_glue"
    CLOUD_AWS_ATHENA = "cloud_aws_athena"
    CLOUD_AWS_REDSHIFT = "cloud_aws_redshift"
# Add Azure execution environments
    CLOUD_AZURE_FUNCTIONS = "cloud_azure_functions"
    CLOUD_AZURE_VIRTUAL_MACHINES = "cloud_azure_virtual_machines"
    CLOUD_AZURE_SYNAPSE_ANALYTICS = "cloud_azure_synapse_analytics"
    CLOUD_AZURE_DATA_FACTORY = "cloud_azure_data_factory"

    def __str__(self):
        return self.value

class ExecutionComputeType(Enum):

    CPU_INTEL = "cpu_intel"
    CPU_AMD = "cpu_amd"
    CPU_ARM = "cpu_arm"
    GPU_NVIDIA = "gpu_nvidia"
    GPU_AMD = "gpu_amd"
    GPU_INTEL = "gpu_intel"
    TPU_GOOGLE = "tpu_google"
    TPU_INTEL = "tpu_intel"
    TPU_AMD = "tpu_amd"

    def __str__(self):
        return self.value
