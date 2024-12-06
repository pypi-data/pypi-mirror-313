# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# pylint: disable=unused-variable
# pylint: disable=broad-exception-raised
import json
import csv
from io import BytesIO, StringIO, TextIOWrapper
import os
import time
import logging
import uuid
import datetime
from typing import List, Dict, Any, Union, Optional, Tuple
from google.api_core.exceptions import NotFound
from google.cloud import  bigquery , secretmanager
from google.cloud.secretmanager import SecretManagerServiceClient
from google.cloud.storage import Client as GCSClient
from ipulse_shared_base_ftredge import (DuplicationHandling,
                                        DuplicationHandlingStatus,
                                        MatchConditionType,
                                        DataSourceType,
                                        LogLevel,
                                        DataActionType,
                                        log_debug, log_info, log_warning, log_error)
from ipulse_shared_data_eng_ftredge import (ContextLog,
                                            Pipelinemon)

from ..utils.utils_exceptions import handle_operation_exception


############################################################################
##################### SECRET MANAGER ##################################
############################################################################

def get_secret_from_gcp_secret_manager_extended(
    secret_id: str,
    gcp_project_id: str,
    version_id: str = "latest",
    secret_client: Optional[SecretManagerServiceClient] = None,
    pipelinemon = None,
    logger = None,
    print_out: bool = False,
    raise_e: bool = True
) -> Dict[str, Any]:
    """GCP-specific secret fetching implementation"""

    result = {"data":None,
               "status":{
                    "execution_state":"",
                    "overall_status": "",
                    "issues": "",
                    "details": {
                        "secret_id": secret_id,
                        "gcp_project_id": gcp_project_id,
                        "version_id": version_id
                }
              }
            }

    try:
        # Create client if not provided
        if not secret_client:
            secret_client = secretmanager.SecretManagerServiceClient()

        name = f"projects/{gcp_project_id}/secrets/{secret_id}/versions/{version_id}"
        response = secret_client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        result["data"] = secret_value
        result["status"]["execution_state"] += ">SUCCESS"
        msg=f"Successfully retrieved secret: {secret_id}"
        log_info(msg=msg, logger=logger, print_out=print_out)
        log_debug(msg=result["status"], logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(LogLevel.READ_SECRET_FROM_SECRET_MANAGER_COMPLETE, subject=msg, description=result["status"]))

    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_READ_SECRET_FROM_SECRET_MANAGER_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)
    return result

############################################################################
##################### GOOGLE CLOUD STORAGE ##################################
############################################################################


def read_file_from_gcs_extended(storage_client:GCSClient, bucket_name:str, file_path:str,
                                 file_extension:DataSourceType=None,
                                 pipelinemon:Pipelinemon=None, logger=None, print_out=False, raise_e=False)-> Dict[str, Any]:
    """Helper function to read a JSON or CSV file from Google Cloud Storage with optional Pipelinemon monitoring."""

    result = {
        "data": None,
        "status":{
            "execution_state":"",
            "overall_status": "",
            "issues": None,
            "details": {
                "bucket_name": bucket_name,
                "file_path": file_path
            }
        }
    }

    try:
        # Determine the file extension
        base_file_name, ext = os.path.splitext(file_path)  # ext includes the dot (.) if present
        ext = ext.lower()
        if not ext:
            if file_extension:
                ext = file_extension.value
                if not ext.startswith('.'):
                    ext = f".{ext}"
                file_path = f"{base_file_name}{ext}"
            else:
                raise ValueError(f"File '{file_path}' has no extension and no file_extension parameter provided.")
        else:
            if file_extension:
                expected_ext = file_extension.value
                if not expected_ext.startswith('.'):
                    expected_ext = f".{expected_ext}"
                if ext != expected_ext:
                    raise ValueError(f"File extension '{ext}' does not match the expected extension '{expected_ext}'")


        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)

        # Check if the blob (file) exists
        if not blob.exists():
            raise NotFound(f"File '{file_path}' not found in bucket '{bucket_name}'")

        # Download the file content
        data_string = blob.download_as_text()


        # Check if the file is empty , better alternative to if blob.size == 0 as blob.size might not be populated or accurate without reloading the blob metadata
        if not data_string:
            raise ValueError(f"File '{file_path}' is empty in bucket '{bucket_name}'")
        
        result["status"]["execution_state"] += ">BLOB_DOWNLOADED"
        # Initialize data variable
        data = None

        # Parse the data based on file extension
        if ext == ".json":
            try:
                data = json.loads(data_string)
            except json.JSONDecodeError as e:
                raise ValueError( f"Error decoding JSON from GCS: {file_path} in bucket {bucket_name}: {e}") from e
        elif ext == ".csv":
            try:
                data_io = StringIO(data_string)
                reader = csv.DictReader(data_io)
                data = list(reader)
            except csv.Error as e:
                raise ValueError(f"Error reading CSV from GCS: {file_path} in bucket {bucket_name}: {e}") from e
        else:
            raise ValueError(f"Unsupported file extension '{ext}'")

        result["status"]["execution_state"] += ">IMPORTING_SUCCESS"
        result["data"] = data
        msg=f"Successfully read file from GCS: {file_path} in bucket {bucket_name}"
        log_info(msg=msg, logger=logger, print_out=print_out)
        log_debug(msg=result["status"], logger=logger, print_out=print_out)
        if pipelinemon:
            pipelinemon.add_log(ContextLog(level=LogLevel.READ_FILE_FROM_CLOUD_STORAGE_COMPLETE,
                                           subject=f"blob {file_path} in {bucket_name}",
                                           description=result["status"]))

    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)
    return result


def write_file_to_gcs_extended(storage_client: GCSClient,
                               data: dict | list | str, bucket_name: str, file_path: str,
                                duplication_handling: DuplicationHandling,
                                duplication_match_condition_type: MatchConditionType,
                                duplication_match_condition: str = "",
                                max_retries: int = 2,
                                max_deletable_files: int = 1,
                                file_extension:DataSourceType =None,
                                logger=None, print_out=False, raise_e=False, pipelinemon: Pipelinemon = None) -> Dict[str, Any]:

    """Saves data to Google Cloud Storage with optional Pipelinemon monitoring.

    Handles duplication with strategies: OVERWRITE, INCREMENT, SKIP, or RAISE_ERROR.

    !! As of now only supporting STRING duplication_match_condition !!
    """

    max_deletable_files_allowed = 3
    cloud_storage_ref = DataSourceType.GCS.value

    # GCS-related metadata
    saved_to_path = None
    matched_duplicates_count = 0
    matched_duplicates_deleted = []
    data_str = None
    data_bytes = None
    content_type = None

    increment = 0
    attempts = 0
    success = False
    result = {
        "data": None,
        "status":{
                "action_type": DataActionType.WRITE_TO_FILE.value,
                "execution_state": "NOT_STARTED",
                "issues": None,
                "details": {
                    "cloud_storage_ref": cloud_storage_ref,
                    "bucket_name": bucket_name,
                    "file_path": file_path,
                    "saved_to_path": saved_to_path,
                    "matched_duplicates_count": matched_duplicates_count,
                    "matched_duplicates_deleted": matched_duplicates_deleted,
                    "duplication_handling_status": None,
                    "duplication_match_condition_type": duplication_match_condition_type.value,
                    "duplication_match_condition": duplication_match_condition
                }
        }
    }
    supported_match_condition_types = [MatchConditionType.EXACT, MatchConditionType.PREFIX]
    supported_duplication_handling = [DuplicationHandling.RAISE_ERROR, DuplicationHandling.OVERWRITE, DuplicationHandling.INCREMENT, DuplicationHandling.SKIP]

    try:
        if max_deletable_files > max_deletable_files_allowed:
            raise ValueError(f"max_deletable_files should be less than or equal to {max_deletable_files_allowed} for safety.")
        if duplication_handling not in supported_duplication_handling:
            msg = f"Error: Duplication handling not supported. Supported types: {[dh.value for dh in supported_duplication_handling]}"
            raise ValueError(msg)
        if duplication_match_condition_type not in supported_match_condition_types:
            msg = f"Error: Match condition type not supported. Supported types: {[mct.value for mct in supported_match_condition_types]}"
            raise ValueError(msg)
        elif duplication_match_condition_type != MatchConditionType.EXACT and not duplication_match_condition:
            msg = f"Error: Match condition is required for match condition type: {duplication_match_condition_type.value}"
            raise ValueError(msg)

        # Determin extension
        base_file_name, ext = os.path.splitext(file_path) ## ext is the file extension with the dot (.) included
        ext = ext.lower()
        if not ext:
            if file_extension:
                ext = file_extension.value
                if not ext.startswith('.'):
                    ext = f".{ext}"
                file_path = f"{base_file_name}{ext}"
            else:
                raise ValueError(f"File '{file_path}' has no extension and no file_extension parameter provided.")
        else:
            if file_extension:
                expected_ext = file_extension.value
                if not expected_ext.startswith('.'):
                    expected_ext = f".{expected_ext}"
                if ext != expected_ext:
                    raise ValueError(f"File extension '{ext}' does not match the expected extension '{expected_ext}'")

        if ext == '.json':
            if isinstance(data, (list, dict)):
                data_str = json.dumps(data, indent=2)
            else:
                data_str = data  # Assuming data is already a JSON-formatted string
            data_bytes = data_str.encode('utf-8')  # Encode the string to UTF-8 bytes
            content_type = 'application/json'
        elif ext == '.csv':
            # Convert data to CSV
            if isinstance(data, (list, dict)):
                # output = StringIO()
                output_bytes = BytesIO()
                output_text = TextIOWrapper(output_bytes, encoding='utf-8', newline='\n')
                if isinstance(data, dict):
                    # Convert dict to list of dicts with a single item
                    data = [data]
                # Assuming data is a list of dicts
                if len(data) == 0:
                    raise ValueError("Cannot write empty data to CSV.")
                fieldnames = data[0].keys()
                writer = csv.DictWriter(output_text, fieldnames=fieldnames,quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n') # Add quoting and line terminator
                writer.writeheader()
                writer.writerows(data)
                output_text.flush()
                output_bytes.seek(0)
                data_bytes = output_bytes.getvalue()
                # Remove any trailing newlines
                data_bytes = data_bytes.rstrip(b'\n')
            else:
                data_bytes = data.encode('utf-8')  # Assuming data is already a CSV-formatted string
            # print(data_bytes.decode('utf-8'))
            content_type = 'text/csv'
        else:
            raise ValueError(f"Unsupported file extension '{ext}'")

        result["status"]["execution_state"] += ">DATA_READY"
        # Check for existing files based on duplication_match_condition_type
        files_matched_on_condition = []
        bucket = storage_client.bucket(bucket_name)
        if duplication_match_condition_type == MatchConditionType.PREFIX:
            files_matched_on_condition = list(bucket.list_blobs(prefix=duplication_match_condition))
        elif duplication_match_condition_type == MatchConditionType.EXACT:
            duplication_match_condition = file_path if not duplication_match_condition else duplication_match_condition
            if bucket.blob(duplication_match_condition).exists():
                files_matched_on_condition = [bucket.blob(file_path)]

        matched_duplicates_count = len(files_matched_on_condition)
        result["status"]["details"]["matched_duplicates_count"] = matched_duplicates_count

        # Handle duplication based on duplication_handling
        if matched_duplicates_count:
            msg = f"Duplicate FOUND, matched_duplicates_count: {matched_duplicates_count}"
            log_info(msg=msg, logger=logger, print_out=print_out)  # Only logs or prints if logger is provided and print_out is True
            if pipelinemon:
                pipelinemon.add_log(ContextLog(LogLevel.NOTICE_FILE_IN_CLOUD_STORAGE_ALREADY_EXISTS, subject="duplicate_found", description=msg))
            

            if duplication_handling == DuplicationHandling.RAISE_ERROR:
                raise FileExistsError("File(s) matching the condition already exist.")

            if duplication_handling == DuplicationHandling.SKIP:
                result["status"]["details"]["duplication_handling_status"] = DuplicationHandlingStatus.SKIPPED.value
                log_msg = f"SKIPPING Write to GCS, result: {result}"
                log_info(log_msg, logger=logger, print_out=print_out)  # Only logs or prints if logger is provided and print_out is True
                return result

            if duplication_handling == DuplicationHandling.OVERWRITE:
                if matched_duplicates_count > max_deletable_files:
                    raise ValueError(f"Error: Attempt to delete {matched_duplicates_count} matched files, but limit is {max_deletable_files}. Operation Cancelled.")

                for blob in files_matched_on_condition:
                    cloud_storage_path_to_delete = f"gs://{bucket_name}/{blob.name}"
                    blob.delete()
                    matched_duplicates_deleted.append(cloud_storage_path_to_delete)
                    log_msg = f"File deleted as part of overwrite: {cloud_storage_path_to_delete}"
                    if pipelinemon:
                        pipelinemon.add_system_impacted(f"delete: {cloud_storage_ref}_bucket_file: {cloud_storage_path_to_delete}")
                        pipelinemon.add_log(ContextLog(LogLevel.ACTION_DELETE_IN_CLOUD_STORAGE_COMPLETE, subject="delete_duplicate", description=log_msg))
                    log_info(log_msg, logger=logger, print_out=print_out)

                result["status"]["details"]["matched_duplicates_deleted"] = matched_duplicates_deleted
                result["status"]["details"]["duplication_handling_status"] = DuplicationHandlingStatus.OVERWRITTEN.value

            elif duplication_handling == DuplicationHandling.INCREMENT:
                while bucket.blob(file_path).exists():
                    increment += 1
                    file_path = f"{base_file_name}_v{increment}{ext}"
                saved_to_path = f"gs://{bucket_name}/{file_path}"
                result["status"]["details"]["duplication_handling_status"] = DuplicationHandlingStatus.INCREMENTED.value
                log_msg = "INCREMENTING as Duplicate FOUND"
                log_info(log_msg, logger=logger, print_out=print_out)  # Only logs or prints if logger is provided and print_out is True

        # GCS Upload
        saved_to_path = f"gs://{bucket_name}/{file_path}"
        while attempts < max_retries and not success:
            try:
                blob = bucket.blob(file_path)
                blob.upload_from_string(data_bytes, content_type=content_type)
                result["status"]["execution_state"] += ">WRITE_FILE_SUCCESS"
                log_msg = f"File uploaded to GCS: {saved_to_path}"
                log_info(msg=msg, logger=logger, print_out=print_out)
                log_debug(msg=result["status"], logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"upload: {cloud_storage_ref}_bucket_file: {saved_to_path}")
                    pipelinemon.add_log(ContextLog(LogLevel.ACTION_WRITE_IN_CLOUD_STORAGE_COMPLETE, subject="file_upload", description=log_msg))
                
                success = True
            except Exception as e:
                attempts += 1
                if attempts < max_retries:
                    time.sleep(2 ** attempts)
                else:
                    raise e
        result["status"]["details"]["saved_to_path"] = saved_to_path if success else None
    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_WRITE_IN_CLOUD_STORAGE_FAILED,
                                    pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)

    return result



###########################################################################################
###########################################################################################
#################################### GOOGLE BIGQUERY ######################################
###########################################################################################
###########################################################################################


###########################################################################################
#################################### BIGQUERY SCHEMA/TYPES UTILS AND FUNCTIONS ############################
###########################################################################################

def _convert_python_type_to_bigquery(value: Any) -> str:
    """
    Determine BigQuery column type from Python value.        
    Returns:
        str: BigQuery data type
    """
    if value is None:
        raise ValueError("Cannot determine BigQuery type from None value")
    if isinstance(value, datetime.datetime):
        return "TIMESTAMP"
    if isinstance(value, datetime.date):
        return "DATE"
    if isinstance(value, str):
        if not value.strip():
            raise ValueError("Cannot determine BigQuery type from empty string")
        try:
            datetime.datetime.strptime(value, '%Y-%m-%d')
            return "DATE"
        except ValueError:
            return "STRING"
            
    # Handle numeric types
    if isinstance(value, int):
        return "INTEGER"
    if isinstance(value, float):
        return "FLOAT"
    if isinstance(value, bool):
        return "BOOLEAN"
        
    return "STRING"

def create_bigquery_schema_from_json_schema(json_schema: list) -> list:
    schema = []
    for field in json_schema:
        if "max_length" in field:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"], max_length=field["max_length"]))
        else:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]))
    return schema


def _convert_cerberus_type_to_bigquery(field_rules: dict) -> str:
    """Maps a Cerberus type to a BigQuery data type, handling custom rules."""

    if 'check_with' in field_rules:
        if field_rules['check_with'] == 'standard_str_date':
            return 'DATE'
        if field_rules['check_with'] == 'iso_str_timestamp':
            return 'TIMESTAMP'
        if field_rules['check_with'] == 'standard_str_time':
            return 'TIME'

    # Default type mapping if no custom rule is found
    type_mapping = {
        'string': 'STRING',
        'integer': 'INT64',
        'float': 'FLOAT64',
        'boolean': 'BOOL',
        'datetime': 'TIMESTAMP',
        'date': 'DATE',
        'time': 'TIME'
    }
    # Handle the case where 'type' is a list
    field_type = field_rules.get('type', 'string')
    if isinstance(field_type, list):
        # Choose the first valid type from the list or default to 'STRING'
        for ft in field_type:
            if ft in type_mapping:
                return type_mapping[ft]
        return 'STRING'  # Default if no valid type found
    else:
        return type_mapping.get(field_type, 'STRING')


def create_bigquery_schema_from_cerberus_schema(cerberus_schema: dict) -> list:
    """Converts a Cerberus validation schema to a BigQuery schema.
        Handles 'custom_date' and 'custom_timestamp' rules as DATE and TIMESTAMP.
    """
    bq_schema = []
    for field_name, field_rules in cerberus_schema.items():
        field_type = _convert_cerberus_type_to_bigquery(field_rules)  # Pass field_name for rule checks
        mode = 'REQUIRED' if field_rules.get('required') else 'NULLABLE'
        max_length = field_rules.get('maxlength')

        field = bigquery.SchemaField(field_name, field_type, mode=mode)
        if max_length:
            field._properties['max_length'] = max_length

        bq_schema.append(field)

    return bq_schema

def _parse_bigquery_response_dates_to_string(query_response: bigquery.table.RowIterator, date_column: str) -> List[str]:
    """
    Process BigQuery query results and format dates as strings.
    
    Args:
        query_response: BigQuery RowIterator containing query results
        date_column: Name of the date column to process
        
    Returns:
        List of formatted date strings
    """
    if not query_response:
        return []
        
    result = []
    for row in query_response:
        value = row[date_column]
        if value is not None:
            if isinstance(value, datetime.date):
                result.append(value.strftime('%Y-%m-%d'))
            else:
                result.append(str(value))
                
    return result


###########################################################################################
#################################### BIGQUERY JOBS HELPER FUNCTIONS ###############################
###########################################################################################

def _get_bigquery_job_details(job: Union[bigquery.LoadJob, bigquery.QueryJob, bigquery.CopyJob, bigquery.ExtractJob]) -> Dict[str, Any]:

    """
    Get BigQuery job status while preserving existing values through appending.
    Returns a status dict with appended values instead of overwriting.
    """
    details ={} # shortcut
    details["execution_errors_count"]= len(job.errors or [])
    details["bigquery_job_id"] = job.job_id or ""
    details["job_user_email"] = job.user_email or ""

    if isinstance(job, bigquery.QueryJob):
        details["total_bytes_billed"] = job.total_bytes_billed
        details["total_bytes_processed"] = job.total_bytes_processed
        details["cache_hit"] = job.cache_hit
        details["slot_millis"] = job.slot_millis
        details["num_dml_affected_rows"] = job.num_dml_affected_rows
        if job.started and job.ended:
            details["duration_ms"] = (job.ended - job.started).total_seconds() * 1000
    elif isinstance(job, bigquery.LoadJob): # Add LoadJob specifics
        if job.started and job.ended:
            details["job_duration_ms"] = (job.ended - job.started).total_seconds() * 1000
        details["job_output_bytes"] = job.output_bytes or 0
        details["job_output_rows"] = job.output_rows or 0    
    elif isinstance(job, (bigquery.CopyJob, bigquery.ExtractJob)): # Add any required fields for other job types
        pass # for now we will keep this empty, you might need to add specific fields

    return details

def _summarize_bigquery_job_errors(job: Union[bigquery.LoadJob, bigquery.QueryJob, bigquery.CopyJob, bigquery.ExtractJob], max_errors_to_log: int = 7) -> str:
    """Summarizes job errors for logging."""
    if job.errors:
        limited_errors = " >> ERRORS DURING JOB:\n"
        limited_errors += "\n".join(str(error) for error in job.errors[:max_errors_to_log])
        if len(job.errors) > max_errors_to_log:
            limited_errors += f"\n...and {len(job.errors) - max_errors_to_log} more errors."
        return limited_errors
    return ""


###########################################################################################
#################################### BIGQUERY CREATE TABLES ###############################
###########################################################################################


def create_bigquery_table_extended(project_id: str,
                          dataset_name: str,
                          table_name: str,
                          schema: List[bigquery.SchemaField],
                          replace_if_exists: bool = False,
                          bigquery_client: Optional[bigquery.Client] = None,
                          pipelinemon: Optional[Pipelinemon]  = None,
                          logger: Optional[logging.Logger] = None,
                          print_out: bool = False,
                          raise_e: bool = False) -> Dict[str, Any]:
    """
    Creates a BigQuery table. If create_or_replace is True, it will replace the table if it already exists.
    
    Parameters:
        project_id (str): GCP Project ID.
        dataset_name (str): BigQuery Dataset name.
        table_name (str): BigQuery Table name.
        schema (List[bigquery.SchemaField]): BigQuery table schema.
        replace_if_exists (bool): Flag to create or replace the table if it exists.
        bigquery_client (Optional[bigquery.Client]): Pre-initialized BigQuery client. If not provided, a new client is created.
        pipelinemon (Optional): Pipeline monitoring object (if applicable).
        logger (Optional[logging.Logger]): Logger for logging messages.
    """
    result = {
        "data": None,
        "status":{
        "action_type": DataActionType.CREATE_TABLE.value,
        "execution_state": "NOT_STARTED",
        "issues": ""
        }
    }
    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)

        # Check if the DATASET exists, and create it if it does not
        dataset_ref = bigquery_client.dataset(dataset_name)
        try:
            bigquery_client.get_dataset(dataset_ref)  # Will raise NotFound if dataset does not exist
            log_info(msg=f"Dataset {dataset_name} already exists.", logger=logger)
        except NotFound as e:
            # Create the dataset if it doesn't exist
            raise ValueError(f"Dataset {dataset_name} does not exist. Please create it first.") from e

     # Check if the TABLE exists before attempting to delete it
        table_ref = dataset_ref.table(table_name)
        table_exists = False
        try:
            bigquery_client.get_table(table_ref)
            table_exists = True
            pipelinemon.add_log(ContextLog(level=LogLevel.NOTICE_ALREADY_EXISTS, subject=table_name, description=f"Table {table_name} already existed in {dataset_name}."))
        except NotFound:
            table_exists = False

        if replace_if_exists and table_exists:
            bigquery_client.delete_table(table_ref)
            result["status"]["execution_state"] += ">TABLE_DELETED"
            msg=f"Table {table_name} in dataset {dataset_name} was deleted."
            log_info(msg=msg, logger=logger)
            if pipelinemon:
                pipelinemon.add_system_impacted(f"bigquery_delete_table: {table_name}")
                pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_DELETE_CLOUD_DB_TABLE_COMPLETE, subject=msg, description=result["status"]))

        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        result["status"]["execution_state"] += ">TABLE_CREATED"
        msg=f"Table {table_name} created in dataset {dataset_ref}."
        log_info(msg=msg, logger=logger, print_out=print_out)
        log_debug(msg=result["status"], logger=logger, print_out=print_out)

        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_create_table: {table_name}")
            pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_CREATE_CLOUD_DB_TABLE_COMPLETE, subject=msg, description=result["status"]))
        
    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_CREATE_CLOUD_DB_TABLE_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)
    return result


###########################################################################################
#################################### BIGQUERY WRITE INSERT AND MERGE ###############################
###########################################################################################


def write_load_from_json_into_bigquery_extended(project_id: str,
                                    data: Union[Dict[str, Any], List[Dict[str, Any]]],
                                    table_full_path: str,
                                    max_job_errors_to_log: int=7,
                                    create_table_if_not_exists: bool=False,
                                    bigquery_client: Optional[bigquery.Client] =None,
                                    schema: Optional[List[bigquery.SchemaField]]=None,
                                    pipelinemon: Optional[Pipelinemon]=None,
                                    logger: Optional[logging.Logger] =None,
                                    print_out: bool=False,
                                    raise_e: bool=False
                                )-> Dict[str, Any]:
    """Executes a BigQuery batch load job and logs the results.
    !!!!! Load Inserting into Bigquery allows for duplicate rows. !!!!!
    returns result: dict
    """
   
    result={
        "data":None,
        "status":{
            "action_type":DataActionType.INSERT.value,
            "execution_state": "NOT_STARTED",
            "issues": "",
            "details": {}
        }
    }
    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)

        success_action_log_levl=LogLevel.ACTION_WRITE_BULK_IN_CLOUD_DB_COMPLETE
        # Handle single record case consistently
        if isinstance(data, dict):
            data = [data]
            success_action_log_levl=LogLevel.ACTION_WRITE_IN_CLOUD_DB_COMPLETE

        job_config = bigquery.LoadJobConfig()
        if schema:
            job_config.schema = schema
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Append to existing data
        if create_table_if_not_exists:
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED  # Create New table if not exists
        else:
            job_config.create_disposition = bigquery.CreateDisposition.CREATE_NEVER  # Don't create Create New table if not exists

        result["status"]["execution_state"] += ">INSERT_JOB_STARTED"
        load_job =bigquery_client.load_table_from_json(data, table_full_path, job_config=job_config,project=project_id)
        load_job.result()  # Wait for job completion
        if pipelinemon:
            pipelinemon.add_system_impacted(f"bigquery_load: {table_full_path}")
        result["status"]["details"].update(_get_bigquery_job_details(job=load_job))
        result["status"]["issues"]+= _summarize_bigquery_job_errors(job=load_job, max_errors_to_log=max_job_errors_to_log)
        # Check job status
        if load_job.state == "DONE" and load_job.errors is None:
            result["status"]["execution_state"] += ">INSERT_JOB_SUCCESS"
            msg=f"Successful load_table_from_json {load_job.job_id} for table {table_full_path}."
            log_info(msg=msg, logger=logger, print_out=print_out)
            log_debug(msg=result["status"], logger=logger, print_out=print_out) 
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=success_action_log_levl,subject=msg,description=result["status"]))
        else:
            result["status"]["execution_state"] += ">INSERT_WITH_ERRORS"
            error_message = f"ERRORED Bigquery load_table_from_json {load_job.job_id} for table {table_full_path}. Job Results: {result["status"]}."
            log_warning(msg=error_message, logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_WRITE_IN_CLOUD_DB_WITH_ERRORS, subject=error_message,description=result["status"]))
    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_WRITE_IN_CLOUD_DB_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)

    return result


def write_merge_batch_into_bigquery_extended(
    project_id: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    table_full_path: str,
    merge_key_columns: Union[str, List[str]], # Columns to use for identifying duplicates
    max_job_errors_to_log: int = 7,
    bigquery_client: Optional[bigquery.Client] = None,
    schema: Optional[List[bigquery.SchemaField]] = None,
    pipelinemon: Optional[Pipelinemon]=None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False,
) -> Dict[str, Any]:
    """
    Merges data into a BigQuery table, avoiding duplicates based on the provided merge key columns.
    Returns:
        Dict[str, Any]: Status information about the merge operation.
    """

    result = {
        "data":None,
        "status":{
            "action_type":DataActionType.MERGE.value,
            "execution_state": "NOT_STARTED",
            "issues": "",
            "details": {}
            }
    }

    error_already_logged=False
    temp_table_name=None

    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)

         ############################################################
         # 1. Stage Incoming Data into TEMP table:
         ############################################################
        ########## checking if data is a single record (in a dict format)
        if isinstance(data, dict):
            data = [data]
        # Extract dataset and table name
        dataset_name = table_full_path.split('.')[1]  # Extract the dataset name
        table_name = table_full_path.split('.')[2]  # Extract the table name
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        temp_table_name = f"{table_name}_temp_{current_date}_{uuid.uuid4().hex[:8]}"
        temp_table_full_path = f"{project_id}.{dataset_name}.{temp_table_name}"

        ############################################################
         # 2. LOAD TEMP Table
         ############################################################
        create_temp_table_from_json_result=write_create_bigquery_table_from_json_extended(bigquery_client=bigquery_client,
                                                                      data=data,
                                                                      project_id=project_id,
                                                                      table_full_path=temp_table_full_path,
                                                                      max_job_errors_to_log=max_job_errors_to_log,
                                                                      schema=schema,
                                                                      pipelinemon=pipelinemon,
                                                                      logger=logger,
                                                                      print_out=print_out,)
        result[">create_temp_table_from_json_status"]=create_temp_table_from_json_result["status"]
        excep_or_error=create_temp_table_from_json_result["status"]["issues"]
        if excep_or_error:
            error_already_logged=True
            result["status"]["execution_state"] += ">TEMP_TABLE_CREATION_FAILED"
            result["status"]["issues"]+=excep_or_error
            raise Exception(create_temp_table_from_json_result["status"]["issues"])
        ############################################################
         # 2. Perform the Merge:
         ############################################################
        
        merge_temp_table_into_target_table_result=write_merge_two_bigquery_tables_extended(bigquery_client=bigquery_client,
                                                                                        project_id=project_id,
                                                                                        target_table_full_path=table_full_path,
                                                                                        source_table_full_path=temp_table_full_path,
                                                                                        merge_key_columns=merge_key_columns,
                                                                                        pipelinemon=pipelinemon,
                                                                                        logger=logger,
                                                                                        raise_e=raise_e,
                                                                                        print_out=print_out)

        result[">merge_temp_table_into_target_table_status"]=merge_temp_table_into_target_table_result["status"]
        excep_or_error=merge_temp_table_into_target_table_result["status"]["issues"]
        if excep_or_error:
            error_already_logged=True
            result["status"]["execution_state"] += ">MERGE_FAILED"
            result["status"]["issues"]+=excep_or_error
            raise Exception(merge_temp_table_into_target_table_result["status"]["issues"])
        result["status"]["execution_state"] += ">MERGE_SUCCESS"
    except Exception as e:
        if not error_already_logged:
            handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_MERGE_FAILED,
                                    pipelinemon=pipelinemon,
                                    logger=logger, print_out=print_out, raise_e=raise_e) 

    ############################################################
    # 3. Clean Up Temporary Table:
    ############################################################   
    finally:
        if temp_table_name:
            try:
                bigquery_client.delete_table(temp_table_full_path, not_found_ok=True)
                log_info(msg=f"Temp table {temp_table_full_path} deleted.", logger=logger, print_out=print_out)
                if pipelinemon:
                    pipelinemon.add_system_impacted(f"delete bigquery_temp_table: {temp_table_full_path}")
                    pipelinemon.add_log(
                        ContextLog(
                            level=LogLevel.ACTION_DELETE_CLOUD_DB_TABLE_COMPLETE,
                            subject="temp_table_cleanup",
                            description=f"Temp table {temp_table_full_path} deleted. Event Results Status: {result["status"]}"
                        )
                    )
                # Update final status after cleanup
                result["status"]["execution_state"] += ">TEMP_TABLE_DELETED"
                
            except Exception as e:
                handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_DELETE_CLOUD_DB_TABLE_FAILED,
                                          pipelinemon=pipelinemon,
                                           logger=logger, print_out=print_out, raise_e=raise_e)
                
    return result


def write_create_bigquery_table_from_json_extended(
    
    data: Union[Dict[str, Any], List[Dict[str, Any]]],
    project_id: str,
    table_full_path: str,
    schema: Optional[List[bigquery.SchemaField]],
    bigquery_client: Optional[bigquery.Client] = None,
    temp: bool=False,
    pipelinemon: Optional[Pipelinemon] = None,
    max_job_errors_to_log: int = 7,
    logger: Optional[logging.Logger] = None,
    raise_e: bool = False,
    print_out: bool = False,
) -> Dict[str, Any]:
    """Load data into temporary table."""

        ########## checking if data is a single record (in a dict format)
    if isinstance(data, dict):
        data = [data]
    temp_str="TEMP" if temp else ""
    result = {
        "data": None,
        "status":{
            "execution_state":"",
            "overall_status": "",
            "issues": "",
            "details": {}
        }
    }
    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED
        )

        result["status"]["execution_state"] += f">{temp_str}_TABLE_LOAD_STARTED"
        load_job = bigquery_client.load_table_from_json(data, table_full_path, job_config=job_config, project=project_id)
        load_job.result()  # Wait for job completion
        if pipelinemon:
            pipelinemon.add_system_impacted(f"create bigquery_table: {table_full_path}")
        
        result["status"]["details"].update(_get_bigquery_job_details(job=load_job))
        result["status"]["issues"]+= _summarize_bigquery_job_errors(job=load_job, max_errors_to_log=max_job_errors_to_log)
        if load_job.state == "DONE" and load_job.errors is None:
            result["status"]["execution_state"] +=f">{temp_str}_TABLE_CREATE_AND_LOAD_SUCCESS"
            msg=f"Successful load_table_from_json: {table_full_path} ."
            log_info(msg=msg, logger=logger, print_out=print_out)
            log_debug(msg=result["status"], logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_CREATE_AND_LOAD_CLOUD_DB_TABLE_COMPLETE ,subject=msg,description=result["status"]))
        else:
            result["status"]["execution_state"] += f">{temp_str}_TABLE_CREATE_AND_LOAD_WITH_ERRORS"
            error_message = f"ERRORED Bigquery load_table_from_json {load_job.job_id} for Table {table_full_path}. Result Status: {result["status"]}"
            log_warning(msg=error_message, logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_CREATE_AND_LOAD_CLOUD_DB_TABLE_FAILED, subject=error_message, description=result["status"]))       

    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_CREATE_AND_LOAD_CLOUD_DB_TABLE_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)
        
    return result


def write_merge_two_bigquery_tables_extended(target_table_full_path: str,
                                              source_table_full_path: str,
                                              merge_key_columns: Union[str, List[str]],
                                              project_id: str, 
                                              bigquery_client: Optional[bigquery.Client] = None,
                                              max_job_errors_to_log: int = 7,
                                              pipelinemon: Optional[Pipelinemon] = None,
                                              logger: Optional[logging.Logger] = None,
                                              print_out: bool = False,
                                              raise_e: bool = False) -> Dict[str, Any]:
    """
    Merges data between two BigQuery tables based on the provided merge key columns.
    Returns:
        Dict[str, Any]: Status information about the merge operation.
    """
    result = {
        "data": None,
        "status":{
            "execution_state":"",
            "overall_status": "",
            "issues": "",
            "details": {}
        }
    }
    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)

        if isinstance(merge_key_columns, str):
            merge_key_columns = [merge_key_columns]
        merge_condition = " AND ".join([f"table1.{col} = table2.{col}" for col in merge_key_columns])
        merge_query = f"""
        MERGE `{target_table_full_path}` AS table1
        USING `{source_table_full_path}` AS table2
        ON {merge_condition}
        WHEN NOT MATCHED THEN
            INSERT ROW
        """
        result["status"]["execution_state"] += ">MERGE_QUERY_STARTED"
        query_merge_job = bigquery_client.query(merge_query)
        query_merge_job.result()  # Wait for the merge to complete
        result["status"]["details"].update(_get_bigquery_job_details(job=query_merge_job))
        result["status"]["issues"]+=_summarize_bigquery_job_errors(job=query_merge_job, max_errors_to_log=max_job_errors_to_log)
        # Check job status
        if query_merge_job.state == "DONE" and query_merge_job.errors is None:
            result["status"]["execution_state"] += ">MERGE_SUCCESS"
            msg = f"Successful MergeJob {query_merge_job.job_id} into {target_table_full_path} from {source_table_full_path}."
            log_info(msg=msg, logger=logger, print_out=print_out)
            log_debug(msg=result["status"], logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_MERGE_BULK_IN_CLOUD_DB_COMPLETE,subject=msg,description=result["status"]))
        else:
            result["status"]["execution_state"] += ">MERGE_WITH_ERRORS"
            error_message = f"ERRORED MergeJob {query_merge_job.job_id} into {target_table_full_path} from {source_table_full_path}. Event Results: {result["status"]}"
            log_warning(msg=error_message, logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_MERGE_WITH_ERRORS, subject=error_message,description=result["status"]))
    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_MERGE_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)
    return result


###########################################################################################
#################################### BIGQUERY WRITE QUERY FUNCTIONS ###############################
###########################################################################################




def write_query_sql_bigquery_table_extended(project_id: str,
                                    query: str,
                                    bigquery_client: Optional[bigquery.Client] = None,
                                    pipelinemon: Optional[Pipelinemon] = None,
                                    max_job_errors_to_log: int = 7,
                                    print_out: bool = False,
                                    logger: Optional[logging.Logger] = None,
                                    raise_e:bool=False) -> Dict[str, Any]:
    """Executes a BigQuery SQL query for write operations and logs the results."""
    if not bigquery_client:
        if not project_id:
            raise ValueError("project_id is required when bigquery_client is not provided.")
        bigquery_client = bigquery.Client(project=project_id)

    result = {
        "data": None,
        "status":{
            "execution_state":"",
            "overall_status": "",
            "issues": "",
            "details": {}
            }
    }
    try:
        result["status"]["execution_state"]= "QUERY_WRITE_JOB_STARTED"
        query_write_job = bigquery_client.query(query, project=project_id)
        query_write_job.result()  # Wait for the job to complete
        
        result["status"]["details"].update(_get_bigquery_job_details(job=query_write_job))
        result["status"]["issues"]+= _summarize_bigquery_job_errors(job=query_write_job, max_errors_to_log=max_job_errors_to_log)
        # Check job status
        if query_write_job.state == "DONE" and not query_write_job.errors:
            result["status"]["execution_state"] += ">QUERY_WRITE_JOB_SUCCESS"
            msg=f"Successfully executed write query. Rows affected: {query_write_job.num_dml_affected_rows}."
            log_info(msg, logger=logger, print_out=print_out)
            log_debug(msg=result['status'], logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ACTION_WRITE_IN_CLOUD_DB_COMPLETE, subject=msg, description=result["status"]))
        else:
            # Handle query execution errors
            result["status"]["execution_state"] += ">QUERY_WRITE_WITH_ERRORS"
            error_msg = f"Failed to execute write query. State: {query_write_job.state},result status : {result["status"]}"
            log_warning(msg=error_msg, logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_ACTION_WRITE_IN_CLOUD_DB_WITH_ERRORS, subject=error_msg, description=result["status"]))

    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_ACTION_WRITE_IN_CLOUD_DB_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)
        
    return result


###########################################################################################
#################################### BIGQUERY READ QUERY FUNCTIONS ###############################
###########################################################################################

def read_query_sql_bigquery_table_extended( project_id: str,
                                            query: str,
                                            bigquery_client: Optional[bigquery.Client] = None,
                                            max_job_errors_to_log: int = 7,
                                            pipelinemon: Optional[Pipelinemon] = None,
                                            logger: Optional[logging.Logger] = None,
                                            print_out: bool = False,
                                            raise_e: bool = False
                                        ) -> Dict[str, Any]:
    """Executes a BigQuery SQL query and logs the results.
    Args:
        project_id (str): The Google Cloud project ID.
        query (str): The SQL query to execute.
        bigquery_client (Optional[bigquery.Client], optional): The BigQuery client instance. Defaults to None.
        pipelinemon (Optional[Pipelinemon], optional): The Pipelinemon instance for monitoring. Defaults to None.
        logger (Optional[logging.Logger], optional): The logger instance. Defaults to None.
    """
    
    result = {
        "data": None,
        "status":{
            "execution_state":"",
            "overall_status": "",
            "issues": "",
            "details": {}
        }
    }
    try:
        if not bigquery_client:
            if not project_id:
                raise ValueError("project_id is required when bigquery_client is not provided.")
            bigquery_client = bigquery.Client(project=project_id)

        result["status"]["execution_state"] += ">QUERY_READ_JOB_STARTED"
        query_read_job = bigquery_client.query(query, project=project_id)
        query_response = query_read_job.result()  # Wait for query to complete
        result["status"]["details"].update(_get_bigquery_job_details(job=query_read_job))
        result["status"]["issues"]+=_summarize_bigquery_job_errors(job=query_read_job, max_errors_to_log=max_job_errors_to_log)

        if query_read_job.state == 'DONE' and query_read_job.errors is None:
            result["data"] = [dict(row) for row in query_response]
            result["status"]["execution_state"] += ">QUERY_READ_JOB_SUCCESS "
            log_info(msg=f"Successfully executed query. Found {len(result['data'])} records.", logger=logger, print_out=print_out)
            log_debug(msg=result['status'], logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(
                    ContextLog(
                        level=LogLevel.READ_CLOUD_DB_COMPLETE,
                        subject="query_job",
                        description=f"Query Job Completed Successfully. Results: {result['status']}"
                    )
                )
        else:
             # Handle query execution errors
            result["status"]["execution_state"] += ">QUERY_READ_JOB_WITH_ERRORS"
            error_msg = f"Failed to execute query. State: {query_read_job.state}, result status: {result['status']}"
            log_warning(msg=error_msg, logger=logger, print_out=print_out)
            if pipelinemon:
                pipelinemon.add_log(
                    ContextLog(
                        level=LogLevel.ERROR_READ_DB_WITH_ERRORS,
                        subject="query_job",
                        description=error_msg
                    )
                )
    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_READ_DB_FAILED,
                                    pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)

    return result


def read_query_for_rows_matching_dates_bigquery_extended(
    project_id: str,
    table_full_path: str,
    date_column: str,
    rows_list: Dict[str, Any],
    date_range: Optional[Tuple[Any, Any]] = None,
    max_job_errors_to_log: int = 7,
    bigquery_client: Optional[bigquery.Client] = None,
    pipelinemon: Optional[Any] = None,
    logger: Optional[logging.Logger] = None,
    raise_e: bool = False,
    print_out: bool = False,
) -> Dict[str, Any]:
    """
    Queries existing records in BigQuery and returns a set of existing values from a specified column.
    """

    result = {
        "data": None,
        "status":{
            "execution_state":"",
            "overall_status": "",
            "issues": "",
            "details": {}
        }
    }

    try:
        # Initialize client
        bigquery_client = bigquery_client or bigquery.Client(project=project_id)

        # Build the WHERE clause dynamically
        where_clauses = []
        query_parameters = []

        # Add field conditions
        for field, value in rows_list.items():
            where_clauses.append(f"{field} = @{field}")
            param_type = "STRING" if isinstance(value, str) else "INTEGER"
            query_parameters.append(bigquery.ScalarQueryParameter(field, param_type, value))

        # Add date range if provided
        if date_range:
            start_date, end_date = date_range
            column_type = _convert_python_type_to_bigquery(start_date or end_date )
            if start_date and end_date:
                where_clauses.append(f"{date_column} BETWEEN @start_date AND @end_date")
                query_parameters.extend([
                    bigquery.ScalarQueryParameter("start_date", column_type, start_date),
                    bigquery.ScalarQueryParameter("end_date", column_type, end_date)
                ])
            elif start_date:
                where_clauses.append(f"{date_column} >= @start_date")
                query_parameters.append(
                    bigquery.ScalarQueryParameter("start_date", column_type, start_date)
                )
            elif end_date:
                where_clauses.append(f"{date_column} <= @end_date")
                query_parameters.append(
                    bigquery.ScalarQueryParameter("end_date", column_type, end_date)
                )

    ####### RETURNING ONLY DATE COLUMN IN STRING FORMAT
        query = f"""
                SELECT 
                FORMAT_DATE('%Y-%m-%d', {date_column}) as {date_column}
                FROM `{table_full_path}`
                WHERE {" AND ".join(where_clauses)}
                ORDER BY {date_column} DESC
                """

#### EXAMPLE HOW IT WILL LOOK TRANSLATES:
# query = f"""SELECT date_id FROM `{table_full_path}`
#              WHERE asset_id = @asset_id AND date_id BETWEEN @records_oldest_date AND @records_recent_date  """
# job_config = bigquery.QueryJobConfig(
#                   query_parameters=[bigquery.ScalarQueryParameter("asset_id", "STRING", asset_id),
#                                    bigquery.ScalarQueryParameter("records_recent_date", "DATE", sourced_records_recent_date),
#                                    bigquery.ScalarQueryParameter("records_oldest_date", "DATE", sourced_records_oldest_date))   


        result["status"]["execution_state"] += ">QUERY_READ_JOB_STARTED"
        query_read_job = bigquery_client.query(
                        query,
                        job_config=bigquery.QueryJobConfig(query_parameters=query_parameters),
                        project=project_id
                    )
        query_response = query_read_job.result() # Wait for the job to complete
        result["status"]["details"].update(_get_bigquery_job_details(job=query_read_job))
        result["status"]["issues"] = _summarize_bigquery_job_errors(job=query_read_job, max_errors_to_log=max_job_errors_to_log)

        if query_read_job.state == 'DONE' and query_read_job.errors is None:
            result["data"] = [row[date_column] for row in query_response]
            succss_msg=f" >QUERY_READ_JOB_SUCCESS. Fetched {len(result["data"]) } records."
            result["status"]["execution_state"] += succss_msg
            log_info(msg=succss_msg, logger=logger)
            log_debug(msg=result['status'], logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.READ_CLOUD_DB_COMPLETE, subject=succss_msg, description=result['status']))
        else:
            result["status"]["execution_state"] += ">QUERY_JOB_WITH_ERRORS"
            error_msg = f"QUERY_JOB_WITH_ERRORS. Result Status: {result["status"]}"
            log_warning(msg=error_msg, logger=logger)
            if pipelinemon:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_READ_DB_FAILED, subject=error_msg, description=result['status']))

    except Exception as e:
        handle_operation_exception(e=e, result=result, log_level=LogLevel.ERROR_READ_DB_FAILED,
                                   pipelinemon=pipelinemon,
                                   logger=logger, print_out=print_out, raise_e=raise_e)

    return result




###########################################################################################
#################################### BIGQUERY READ QUERY FUNCTIONS ###############################
###########################################################################################


def read_json_from_gcs(storage_client:GCSClient, bucket_name:str, file_name:str, logger=None,print_out=False, raise_e=False):
    """ Helper function to read a JSON or CSV file from Google Cloud Storage """

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data = json.loads(data_string)
        return data
    except NotFound as exc:
        msg = f"The file {file_name} was not found in the bucket {bucket_name}."
        log_error(msg=msg, exc_info=True, logger=logger, print_out=print_out)
        if raise_e:
            raise ValueError(msg) from exc
        return None
    except json.JSONDecodeError as exc:
        msg = f"Error: The file {file_name} could not be decoded as JSON. In bucket '{bucket_name} "
        log_error(msg=msg ,exc_info=True, logger=logger, print_out=print_out)
        if raise_e:
            raise ValueError(msg) from exc
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", exc_info=True, logger=logger, print_out=print_out)
        if raise_e:
            raise e from e
        return None

def read_csv_from_gcs(bucket_name:str, file_name:str, storage_client:GCSClient, logger=None, print_out=False):
    """ Helper function to read a CSV file from Google Cloud Storage """

    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        data_string = blob.download_as_text()
        data_file = StringIO(data_string)
        reader = csv.DictReader(data_file)
        return list(reader)
    except NotFound:
        log_error(msg=f"Error: The file {file_name} was not found in the bucket {bucket_name}.", logger=logger, print_out=print_out)
        return None
    except csv.Error:
        log_error(msg=f"Error: The file {file_name} could not be read as CSV.", logger=logger, print_out=print_out)
        return None
    except Exception as e:
        log_error(msg=f"An unexpected error occurred: {e}", logger=logger, print_out=print_out, exc_info=True)
        return None