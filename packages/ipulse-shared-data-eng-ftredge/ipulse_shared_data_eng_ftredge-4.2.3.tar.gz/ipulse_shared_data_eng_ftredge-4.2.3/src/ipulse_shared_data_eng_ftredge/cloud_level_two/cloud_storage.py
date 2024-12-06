# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=invalid-name

from typing import Dict, List, Optional
from ipulse_shared_base_ftredge import (LogLevel, DataSourceType,
                                        log_warning, log_info, log_debug)

from ipulse_shared_data_eng_ftredge import (check_format_against_schema_template,
                                            read_file_from_cloud_storage_extended,
                                            ContextLog,
                                            Pipelinemon)

def import_file_with_data_and_metadata_from_cloud_storage(
                                                       cloud_storage:DataSourceType,
                                                       storage_client,
                                                       file_name:str,
                                                       source_bucket_name:str,
                                                       pipelinemon:Pipelinemon,
                                                       data_schema:Optional[List[Dict]]=None,
                                                       data_formatting_issues_allowed_before_stop_checking=8,
                                                       dataset_issues_allowed_to_return=0,
                                                       metadata_schema:Optional[List[Dict]]=None,
                                                       metadata_issues_allowed_to_return=0,
                                                       logger=None):
    """
    Imports market data (and metadata if present) from cloud storage. Automatically detects if the file contains metadata.
    CAUTION: Pipelinemon is already logging some actions inside read_json_from_cloud_storage_extended, avoid duplicating logs.
    """
    contains_metadata = False
    records_metadata = None
    records_json = None
    #####################################################################
    ##################### 1. IMPORT FILE CONTENT ########################
    try:
        with pipelinemon.context("importing_data"):
            try:
                json_data = read_file_from_cloud_storage_extended(pipelinemon=pipelinemon, cloud_storage=cloud_storage, storage_client=storage_client, file_path=file_name, bucket_name=source_bucket_name)
                # Check if the data contains metadata by inspecting the structure
                if json_data:
                    if isinstance(json_data, dict) and 'metadata' in json_data and 'data' in json_data:
                        records_metadata = json_data.get('metadata')
                        records_json = json_data.get('data')
                        contains_metadata = True
                        log_info(f'Successfully read file {file_name} from bucket {source_bucket_name}. Total {len(records_json)} records and metadata.', logger=logger)
                    else:
                        records_json = json_data
                        log_info(f'Successfully read file {file_name} from bucket {source_bucket_name}. Total {len(records_json)} records.', logger=logger)
                else:
                    log_warning(f"File {file_name} is empty or not found in bucket {source_bucket_name}.", logger=logger)
                    return None
            except Exception as e:
                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_READ_FILE_FROM_CLOUD_STORAGE_FAILED, e=e, subject=file_name))
                log_warning(f"Exception when reading file {file_name}: {type(e).__name__} - {str(e)}", logger=logger)
                return None

        ################################################################
        ##################### 2. PERFORM CHECKS WITH METADATA ########################
        if data_schema:
            with pipelinemon.context("checking_dataset_schema_format"):
                try:
                    for record in records_json:
                        _, warnings_or_error = check_format_against_schema_template(schema=data_schema, data_to_check=record)
                        if warnings_or_error and len(warnings_or_error)>0:
                            pipelinemon.add_logs(warnings_or_error)
                            # Early stopping if warnings/errors exceed max allowed. Better to allow until max allowed, to get a better picture of dataset
                            if pipelinemon.count_warnings_and_errors_for_current_context()>data_formatting_issues_allowed_before_stop_checking:
                                log_warning(f" Early_Stopping schema check, as nb of warnings/errors already exceeds max allowed : {data_formatting_issues_allowed_before_stop_checking}.", logger=logger)
                                break
                    if pipelinemon.count_warnings_and_errors_for_current_context()>dataset_issues_allowed_to_return: # Still don't proceed if at leastr 1 warning is identified
                        msg=f"Data checked against Schema. With total Warnings+Errors/[allowed to return dataset; allowed during dataset check]  : {pipelinemon.count_warnings_and_errors_for_current_and_nested_contexts()}/[{dataset_issues_allowed_to_return}; {data_formatting_issues_allowed_before_stop_checking}]"
                        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_DATA_QUALITY_THRESHOLD_REACHED,
                                        subject=f"data of {file_name}",
                                        description=msg))
                        log_debug(msg, logger=logger)
                        return None
                except Exception as e:
                    log_warning(f"ERROR: Exception occured in {pipelinemon.current_context} : {type(e).__name__} - {str(e)}", logger=logger)
                    pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e, subject=file_name))
                    return None

        if contains_metadata:
            if metadata_schema:
                with pipelinemon.context("checking_metadata_schema_format"):
                    try:
                        _, metadata_warnings_or_error = check_format_against_schema_template(schema=metadata_schema, data_to_check=records_metadata)
                        if metadata_warnings_or_error and len(metadata_warnings_or_error)>0:
                            pipelinemon.add_logs(metadata_warnings_or_error)
                            if len(metadata_warnings_or_error)>metadata_issues_allowed_to_return:
                                log_warning(f"Early_Stopping. Metadata checked against Schema. With total Warnings/Errors: {len(metadata_warnings_or_error)}", logger=logger)
                                pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_METADATA_QUALITY_THRESHOLD_REACHED,
                                                subject=f"metadata of {file_name}",
                                                description=f"Metadata Schema Check finished with with Errors/Warnings : {len(metadata_warnings_or_error)}"))
                                return None
                        log_debug(msg="Metadata checked against Schema with 0  Warnings/Errors. ", logger=logger)
                    except Exception as e:
                        log_warning(f"ERROR: Exception occured in {pipelinemon.current_context} : {type(e).__name__} - {str(e)}", logger=logger)
                        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
                        return None
        
        return json_data

            ############### SETTING SOME PARAMETERS #####################
    except Exception as e:
        log_warning(f"Exception when perfoming checks for file {file_name}: {type(e).__name__} - {str(e)}", logger=logger)
        pipelinemon.add_log(ContextLog(level=LogLevel.ERROR_EXCEPTION, e=e))
        return None
    