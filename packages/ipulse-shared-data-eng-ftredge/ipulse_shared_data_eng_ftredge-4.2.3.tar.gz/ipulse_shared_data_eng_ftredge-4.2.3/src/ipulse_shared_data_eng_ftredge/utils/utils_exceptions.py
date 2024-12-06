from typing import Any, Dict, Optional, Union
import logging
import inspect
import traceback
import json
from ipulse_shared_base_ftredge import (
                                        LogLevel,
                                        log_warning)
from ipulse_shared_data_eng_ftredge import Pipelinemon, ContextLog


def format_detailed_error(e: Exception, operation_name: str) -> str:
    parts = [
        f"EXCEPTION during '{operation_name}':",
        f"Type: {type(e).__name__}",
        f"Message: {str(e)}",
        f"Caused_by: {e.__cause__ or ''}",
        f"Stack Trace:",
        ''.join(traceback.format_tb(e.__traceback__))
    ]
    return ' \n '.join(parts)

def format_multiline_message(msg: Union[str, dict, set, Any]) -> str:
    """
    Format multiline messages for better readability in logs.
    Handles dictionaries, sets, and other types.
    """
    if isinstance(msg, dict):
        # Convert any non-serializable values in dict
        serializable_dict = {}
        for k, v in msg.items():
            if isinstance(v, set):
                serializable_dict[k] = list(v)
            else:
                serializable_dict[k] = v
        return json.dumps(serializable_dict, indent=2, default=str)
    elif isinstance(msg, set):
        return json.dumps(list(msg), indent=2, default=str)
    return str(msg)

def handle_operation_exception(
    e: Exception,
    result: Dict[str, Any],
    log_level: LogLevel,
    pipelinemon: Optional[Pipelinemon] = None,
    logger: Optional[logging.Logger] = None,
    print_out: bool = False,
    raise_e: bool = False
) -> None:
    """Centralized error handler for GCP operations"""

    caller_frame = inspect.currentframe().f_back
    operation_name = caller_frame.f_code.co_name if caller_frame else "unknown_operation"
    error_msg = format_detailed_error(e, operation_name)
    # error_msg = f"EXCEPTION: {operation_name} failed: {type(e).__name__} - {str(e)}"
    result["status"]["execution_state"] += ">EXCEPTION"
    result["status"]["overall_status"] = "FAILED"
    # Append to error history with separator if previous errors exist
    if result["status"]["issues"]:
        result["status"]["issues"] += ">>" + error_msg
    else:
        result["status"]["issues"] = error_msg

    formatted_status = format_multiline_message(result['status'])
    log_warning(
        msg=f"EXCEPTION occurred. --> {formatted_status}",
        logger=logger,
        print_out=print_out
    )
    
    if pipelinemon:
        pipelinemon.add_log(ContextLog(
            level=log_level,
            e=e,
            description=formatted_status
        ))

    if raise_e:
        raise e from e