
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable
import traceback
import json
from datetime import datetime, timezone
from typing import List, Optional
from ipulse_shared_base_ftredge import Status, LogLevel

############################################################################
##################### SETTING UP custom LOGGING format= DICT ##########################
### Cloud  Agnostic, can be used with any cloud provider , jsut use to_dict() method to get the log in dict format
class ContextLog:

    def __init__(self, level: LogLevel, base_context: Optional[str] = None,
                 collector_id: Optional[str] = None,
                 task_id: Optional[str] = None,
                context: Optional[str] = None, description: Optional[str] = None,
                note:Optional[str] = None, subject: Optional[str] = None,
                systems_impacted: Optional[List[str]] = None,
                log_status:Optional[Status] = Status.OPEN,
                 e: Optional[Exception] = None, e_type: Optional[str] = None,
                e_message: Optional[str] = None, e_traceback: Optional[str] = None, **kwargs):

        if e is not None:
            e_type = type(e).__name__ if e_type is None else e_type
            e_message = str(e) if e_message is None else e_message
            e_traceback = traceback.format_exc() if e_traceback is None else e_traceback
        elif not e_traceback and (e_type or e_message):
            e_traceback = traceback.format_exc()

        self.level = level
        self.subject = subject
        self.description = description
        self._base_context = base_context
        self._context = context
        self._systems_impacted = systems_impacted if systems_impacted else []
        self.collector_id = collector_id
        self.exception_type = e_type
        self.exception_message = e_message
        self.exception_traceback = e_traceback
        self.log_status = log_status
        self._note = note
        self._task_id = task_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    @property
    def base_context(self):
        return self._base_context

    @base_context.setter
    def base_context(self, value):
        self._base_context = value

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, value):
        self._note = value

    @property
    def task_id(self):
        return self._task_id
    
    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @property
    def systems_impacted(self):
        return self._systems_impacted

    @systems_impacted.setter
    def systems_impacted(self, list_of_si: List[str]):
        self._systems_impacted = list_of_si

    def add_system_impacted(self, system_impacted: str):
        if self._systems_impacted is None:
            self._systems_impacted = []
        self._systems_impacted.append(system_impacted)

    def remove_system_impacted(self, system_impacted: str):
        if self._systems_impacted is not None:
            self._systems_impacted.remove(system_impacted)

    def clear_systems_impacted(self):
        self._systems_impacted = []

    def _format_traceback(self, e_traceback, e_message, max_field_len:int, max_traceback_lines:int):
        if not e_traceback or e_traceback == 'None\n':
            return None

        traceback_lines = e_traceback.splitlines()

            # Check if the traceback is within the limits
        if len(traceback_lines) <= max_traceback_lines and len(e_traceback) <= max_field_len:
            return e_traceback

        # Remove lines that are part of the exception message if they are present in traceback
        message_lines = e_message.splitlines() if e_message else []
        if message_lines:
            for message_line in message_lines:
                if message_line in traceback_lines:
                    traceback_lines.remove(message_line)

        # Filter out lines from third-party libraries (like site-packages)
        filtered_lines = [line for line in traceback_lines if "site-packages" not in line]

        # If filtering results in too few lines, revert to original traceback
        if len(filtered_lines) < 2:
            filtered_lines = traceback_lines

        # Combine standalone bracket lines with previous or next lines
        combined_lines = []
        for line in filtered_lines:
            if line.strip() in {"(", ")", "{", "}", "[", "]"} and combined_lines:
                combined_lines[-1] += " " + line.strip()
            else:
                combined_lines.append(line)

            # Ensure the number of lines doesn't exceed MAX_TRACEBACK_LINES
        if len(combined_lines) > max_traceback_lines:
            keep_lines_start = min(max_traceback_lines // 2, len(combined_lines))
            keep_lines_end = min(max_traceback_lines // 2, len(combined_lines) - keep_lines_start)
            combined_lines = (
                combined_lines[:keep_lines_start] +
                ['... (truncated) ...'] +
                combined_lines[-keep_lines_end:]
            )

        formatted_traceback = '\n'.join(combined_lines)

        # Ensure the total length doesn't exceed MAX_TRACEBACK_LENGTH
        if len(formatted_traceback) > max_field_len:
            truncated_length = max_field_len - len('... (truncated) ...')
            half_truncated_length = truncated_length // 2
            formatted_traceback = (
                formatted_traceback[:half_truncated_length] +
                '\n... (truncated) ...\n' +
                formatted_traceback[-half_truncated_length:]
            )
        return formatted_traceback

    def to_dict(self, max_field_len:int =10000, size_limit:float=256 * 1024 * 0.80,max_traceback_lines:int = 30):
        size_limit = int(size_limit)  # Ensure size_limit is an integer

        # Unified list of all fields
        systems_impacted_str = f"{len(self.systems_impacted)} system(s): " + " ,,, ".join(self.systems_impacted) if self.systems_impacted else None
        fields = [
            ("collector_id", str(self.collector_id)),
            ("task_id", str(self.task_id)),
            ("log_status", str(self.log_status.name)),
            ("level_code", self.level.value),
            ("level_name", str(self.level.name)),
            ("base_context", str(self.base_context)),
            ("context", str(self.context)),  # special sizing rules apply to it
            ("subject", str(self.subject)),
            ("description", str(self.description)),
            ("systems_impacted", systems_impacted_str),
            ("note", str(self.note)),
            ("exception_type", str(self.exception_type)),
            ("exception_message", str(self.exception_message)),
            ("exception_traceback", str(self._format_traceback(self.exception_traceback,self.exception_message, max_field_len, max_traceback_lines))),
            ("timestamp", str(self.timestamp))
        ]

        # Function to calculate the byte size of a JSON-encoded field
        def field_size(key, value):
            return len(json.dumps({key: value}).encode('utf-8'))

        # Function to truncate a value based on its type
        # Function to truncate a value based on its type
        def truncate_value(value, max_size):
            if isinstance(value, str):
                half_size = max_size // 2
                return value[:half_size] + '...' + value[-(max_size - half_size - 3):]
            return value

         # Ensure no field exceeds max_field_len
        for i, (key, value) in enumerate(fields):
            if isinstance(value, str) and len(value) > max_field_len:
                fields[i] = (key, truncate_value(value, max_field_len))

        # Ensure total size of the dict doesn't exceed size_limit
        total_size = sum(field_size(key, value) for key, value in fields)
        log_dict = {}
        truncated = False

        if total_size > size_limit:
            truncated = True
            remaining_size = size_limit
            remaining_fields = len(fields)

            for key, value in fields:
                if remaining_fields > 0:
                    max_size_per_field = remaining_size // remaining_fields
                else:
                    max_size_per_field = 0

                field_sz = field_size(key, value)
                if field_sz > max_size_per_field:
                    value = truncate_value(value, max_size_per_field)
                    field_sz = field_size(key, value)

                log_dict[key] = value
                remaining_size -= field_sz
                remaining_fields -= 1
        else:
            log_dict = dict(fields)

        log_dict['trunc'] = truncated

        return log_dict

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        return self.__str__()
