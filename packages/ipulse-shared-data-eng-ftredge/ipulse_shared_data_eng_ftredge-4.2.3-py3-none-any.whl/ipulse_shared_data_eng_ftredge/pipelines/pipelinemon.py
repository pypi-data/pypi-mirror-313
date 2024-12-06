# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught
import json
import uuid
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import List, Optional, Union, Set, Dict, Any
import logging
from ipulse_shared_base_ftredge import LogLevel
from .context_log import  ContextLog

############################################################################
##### PIPINEMON Collector for Logs and Statuses of running pipelines #######
class Pipelinemon:
    """A class for collecting logs and statuses of running pipelines.
    This class is designed to be used as a context manager, allowing logs to be
    collected, stored and reported in a structured format. The logs can be retrieved and
    analyzed at the end of the pipeline execution, or only the counts.
    """

    LEVELS_DIFF = 1000  # The difference in value between major log levels
    PIPELINE_LEVELS =  [LogLevel.INFO_PIPELINE_STARTED,
                        LogLevel.INFO_PIPELINE_CANCELLED,
                        LogLevel.SUCCESS_PIPELINE_COMPLETE,
                        LogLevel.SUCCESS_PIPELINE_COMPLETE_WITH_NOTICES,
                        LogLevel.SUCCESS_PIPELINE_COMPLETE_WITH_WARNINGS,
                        LogLevel.FAILED_PIPELINE_COMPLETE_WITH_ERRORS,
                        LogLevel.FAILED_PIPELINE_EARLY_EXITED,
                        LogLevel.FAILED_CRITICAL_SYSTEM_FAILURE ]
    
    SUBJECT_LEVELS= [LogLevel.INFO_SUBJECT_STARTED,
                     LogLevel.SUCCESS_SUBJECT_COMPLETE,
                     LogLevel.SUCCESS_SUBJECT_COMPLETE_WITH_NOTICES,
                     LogLevel.SUCCESS_SUBJECT_COMPLETE_WITH_WARNINGS,
                     LogLevel.FAILED_SUBJECT,
                     LogLevel.FAILED_SUBJECT_COMPLETE_WITH_ERRORS,
                     ]
    SUBJECT_GROUP_LEVELS = [LogLevel.INFO_SUBJECT_GROUP_STARTED,
                            LogLevel.SUCCESS_SUBJECT_GROUP_COMPLETE,
                            LogLevel.SUCCESS_SUBJECT_GROUP_COMPLETE_WITH_NOTICES,
                            LogLevel.SUCCESS_SUBJECT_GROUP_COMPLETE_WITH_WARNINGS,
                            LogLevel.FAILED_SUBJECT_GROUP,
                            LogLevel.FAILED_SUBJECT_GROUP_COMPLETE_WITH_ERRORS
                            ]
    

    def __init__(self, base_context: str, logger,
                 max_log_field_size:int =10000,
                 max_log_dict_size:float=256 * 1024 * 0.80,
                 max_log_traceback_lines:int = 30):
        self._id = str(uuid.uuid4())
        self._logs = []
        self._early_stop = False
        self._early_stop_reason = None  # Track what caused early stop
        self._systems_impacted = []
        self._by_level_counts = {level.name: 0 for level in LogLevel}
        self._base_context = base_context
        self._context_stack = []
        self._logger = logger
        self._max_log_field_size = max_log_field_size
        self._max_log_dict_size = max_log_dict_size
        self._max_log_traceback_lines = max_log_traceback_lines
        self._start_time = None  # Add start time variable

    @contextmanager
    def context(self, context: str):
        """Safer context management with type checking"""
        if not isinstance(context, str):
            raise TypeError("Context must be a string")
        self.push_context(context)
        try:
            yield
        finally:
            self.pop_context()

    def push_context(self, context):
        self._context_stack.append(context)

    def pop_context(self):
        if self._context_stack:
            self._context_stack.pop()

    @property
    def current_context(self):
        return " >> ".join(self._context_stack)

    @property
    def base_context(self):
        return self._base_context
    
    @base_context.setter
    def base_context(self, value):
        self._base_context = value

    @property
    def id(self):
        return self._id

    @property
    def systems_impacted(self):
        return self._systems_impacted

    @systems_impacted.setter
    def systems_impacted(self, list_of_si: List[str]):
        self._systems_impacted = list_of_si

    def add_system_impacted(self, system_impacted: str)-> None:
        if self._systems_impacted is None:
            self._systems_impacted = []
        self._systems_impacted.append(system_impacted)

    def clear_systems_impacted(self):
        self._systems_impacted = []

    @property
    def max_log_dict_size(self):
        return self._max_log_dict_size

    @max_log_dict_size.setter
    def max_log_dict_size(self, value):
        self._max_log_dict_size = value

    @property
    def max_log_field_size(self):
        return self._max_log_field_size

    @max_log_field_size.setter
    def max_log_field_size(self, value):
        self._max_log_field_size = value

    @property
    def max_log_traceback_lines(self):
        return self._max_log_traceback_lines

    @max_log_traceback_lines.setter
    def max_log_traceback_lines(self, value):
        self._max_log_traceback_lines = value

    @property
    def early_stop(self):
        return self._early_stop

    def set_early_stop(self, reason: str):
        """Sets the early stop flag and optionally logs an error."""
        self._early_stop = True
        self._early_stop_reason = reason  # Store the reason for early stop
        

    def reset_early_stop(self):
        self._early_stop = False

    @property
    def early_stop_reason(self):
        return self._early_stop_reason


    def start(self, pipeline_description: str):
        """Logs the start of the pipeline execution."""
        self._start_time = datetime.now(timezone.utc)  # Capture the start time
        self.add_log(ContextLog(
                        level=LogLevel.INFO_PIPELINE_STARTED,
                        subject="PIPELINE_START",
                        description=pipeline_description
                    ))

    def get_duration_since_start(self) -> Optional[str]:
        """Returns the duration since the pipeline started, formatted as HH:MM:SS."""
        if self._start_time is None:
            return None
        elapsed_time = datetime.now(timezone.utc) - self._start_time
        return str(elapsed_time)


    def _update_counts(self, level: LogLevel, remove=False):
        """Updates the counts for the specified log level."""
        if remove:
            self._by_level_counts[level.name] -= 1
        else:
            self._by_level_counts[level.name] += 1



    def add_log(self, log: ContextLog ):
        log.base_context = self.base_context
        log.context = self.current_context if self.current_context else "root"
        log.collector_id = self.id
        log.systems_impacted = self.systems_impacted
        log_dict = log.to_dict(max_field_len=self.max_log_field_size,
                               size_limit=self.max_log_dict_size,
                               max_traceback_lines=self.max_log_traceback_lines)
        self._logs.append(log_dict)
        self._update_counts(level=log.level)  # Pass the context to _update_counts

        if self._logger:
            # We specifically want to avoid having an ERROR log level for this structured Pipelinemon reporting, to ensure Errors are alerting on Critical Application Services.
            # A single ERROR log level is usually added at the end of the entire pipeline
            if log.level.value >= LogLevel.WARNING.value:
                self._logger.warning(log_dict)
            else:
                self._logger.info(log_dict)

    def add_logs(self, logs: List[ContextLog]):
        for log in logs:
            self.add_log(log)

    def clear_logs_and_counts(self):
        self._logs = []
        self._by_level_counts = {level.name: 0 for level in LogLevel}

    def clear_logs(self):
        self._logs = []

    def get_all_logs(self,in_json_format=False):
        if in_json_format:
            return json.dumps(self._logs)
        return self._logs

    def get_logs_for_level(self, level: LogLevel):
        return [log for log in self._logs if log["level_code"] == level.value]

    def get_logs_by_str_in_context(self, context_substring: str):
        return [
            log for log in self._logs
            if context_substring in log["context"]
        ]
    
    def contains_any_logs_for_level(self,
    levels: Union[LogLevel, List[LogLevel]],
    entire_level_range: bool = False
    ) -> bool:
        """
        Check if any logs exist using _by_level_counts
        """
        if isinstance(levels, LogLevel):
            if entire_level_range:
                # Check any level in range has count > 0
                return any(
                    self._by_level_counts.get(level.name, 0) > 0
                    for level in LogLevel
                    if levels.value <= level.value < levels.value + self.LEVELS_DIFF
                )
            else:
                # Check single level
                return self._by_level_counts.get(levels.name, 0) > 0
        else:
            # Check list of levels
            return any(
                self._by_level_counts.get(level.name, 0) > 0
                for level in levels
            )
    
    def count_logs_for_levels_and_context(
        self,
        levels: Union[LogLevel, List[LogLevel]],
        entire_level_range: False,
        context: Optional[str] = None,
        exclude_nested_contexts: bool = False,
        exclude_levels: Optional[Union[LogLevel, List[LogLevel]]] = None
    ) -> int:
        """
        Count logs for one or multiple levels with flexible context matching.
        
        Args:
            levels: Single LogLevel or List of LogLevels to count
            entire_level_range: Whether to count entire range for each level
            context: Context to filter by (None for all contexts)
            excluded_nested_contexts: Whether to match context exactly
            exclude_levels: Levels to exclude from counting
        """

        # Convert input to list
        if isinstance(levels, LogLevel):
            # Single level - can use range if requested
            level_values = set(range(levels.value, levels.value + self.LEVELS_DIFF)) if entire_level_range else {levels.value}
        else:
            # List of levels - ignore range flag
            level_values = {level.value for level in levels}

        # Handle exclusions
        if exclude_levels:
            excluded_values = set()
            if isinstance(exclude_levels, LogLevel):
                excluded_values.add(exclude_levels.value)
            elif isinstance(exclude_levels, (list, tuple)):
                excluded_values.update(lvl.value for lvl in exclude_levels)
            level_values -= excluded_values

        if context is None:
            return sum(
                1 for log in self._logs
                if log["level_code"] in level_values
            )
        
        return sum(
            1 for log in self._logs
            if log["level_code"] in level_values and
            (log["context"] == context if exclude_nested_contexts else log["context"].startswith(context))
        )
    
    
    def count_logs_for_current_context(self, levels: Union[LogLevel, List[LogLevel]], entire_level_range: bool = False, exclude_nested_contexts=False) -> int:
        """Count logs for given level in the current context"""
        return self.count_logs_for_levels_and_context(levels=levels, entire_level_range=entire_level_range,context=self.current_context, exclude_nested_contexts=exclude_nested_contexts)
    
    def count_total_logs_for_levels(self, levels: Union[LogLevel, List[LogLevel]], entire_level_range: bool = False) -> int:
        """Count logs using _by_level_counts for long-term memory"""
        if isinstance(levels, LogLevel):
            if entire_level_range:
                # Get all level names within range
                return sum(
                    self._by_level_counts.get(level.name, 0)
                    for level in LogLevel
                    if levels.value <= level.value < levels.value + self.LEVELS_DIFF
                )
            else:
                # Single level
                return self._by_level_counts.get(levels.name, 0)
        else:
            # List of levels - ignore range flag
            return sum(
                self._by_level_counts.get(level.name, 0)
                for level in levels
            )

    # def _count_logs(self, context_string: str, exact_context_match=False,
    #                levels: Optional[Union[LogLevel, List[LogLevel], range]] = None,
    #                exclude_pipeline_levels=True):
    #     """Counts logs based on context, exact match, and log levels.
    #     Args:
    #         context_string (str): The context string to match.
    #         exact_match (bool, optional): If True, matches the entire context string. 
    #                                    If False (default), matches context prefixes.
    #         levels (Optional[Union[LogLevel, List[LogLevel], range]], optional):
    #             - If None, counts all log levels.
    #             - If a single LogLevel, counts logs for that level.
    #             - If a list of LogLevels, counts logs for all levels in the list.
    #             - If a range object, counts logs with level values within that range. 
    #     """
    #     if levels is None:
    #         level_values = [level.value for level in LogLevel] # Count all levels
    #     elif isinstance(levels, LogLevel):
    #         level_values = [levels.value]
    #     elif isinstance(levels, range):
    #         level_values = list(levels)
    #     elif isinstance(levels, list) and all(isinstance(level, LogLevel) for level in levels):
    #         level_values = [level.value for level in levels]
    #     else:
    #         raise ValueError("Invalid 'levels' argument. Must be None, a LogLevel, a list of LogLevels, or a range.")
        
    #     if exclude_pipeline_levels:
    #         # Exclude pipeline-level log levels

    #         level_values = [lv for lv in level_values if lv not in self.PIPELINE_LEVELS]

    #     return sum(
    #         1 for log in self._logs
    #         if (log["context"] == context_string if exact_context_match else log["context"].startswith(context_string)) and
    #            log["level_code"] in level_values
    #     )
    
    # def count_logs_for_current_context(self, levels: Optional[Union[LogLevel, List[LogLevel], range]] = None, exclude_pipeline_levels=True):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=levels, exclude_pipeline_levels=exclude_pipeline_levels)

    # def count_logs_for_current_and_nested_contexts(self, levels: Optional[Union[LogLevel, List[LogLevel], range]] = None, exclude_pipeline_levels=True):
    #     return self._count_logs(self.current_context, levels=levels, exclude_pipeline_levels=exclude_pipeline_levels)
    
    # def count_failures(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.FAILED.value <= level.value < LogLevel.FAILED.value + self.LEVELS_DIFF and level.value not in self.PIPELINE_LEVELS)

    # def count_failures_for_current_context(self,exclude_pipeline_levels=True):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.FAILED.value, LogLevel.FAILED.value + self.LEVELS_DIFF), exclude_pipeline_levels=exclude_pipeline_levels)

    # def count_failures_for_current_and_nested_contexts(self,exclude_pipeline_levels=True):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.FAILED.value, LogLevel.FAILED.value + self.LEVELS_DIFF), exclude_pipeline_levels=exclude_pipeline_levels)

    # def count_successes(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.SUCCESS.value <= level.value < LogLevel.SUCCESS.value + self.LEVELS_DIFF and level.value not in self.PIPELINE_LEVELS)
    # def count_successes_for_current_context(self,exclude_pipeline_levels=True):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.SUCCESS.value, LogLevel.SUCCESS.value + self.LEVELS_DIFF), exclude_pipeline_levels=exclude_pipeline_levels)

    # def count_successes_for_current_and_nested_contexts(self,exclude_pipeline_levels=True):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.SUCCESS.value, LogLevel.SUCCESS.value + self.LEVELS_DIFF), exclude_pipeline_levels=exclude_pipeline_levels)        

    # def count_errors(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.ERROR.value <= level.value < LogLevel.ERROR.value + self.LEVELS_DIFF)

    # def count_errors_for_current_context(self):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.ERROR.value, LogLevel.ERROR.value + self.LEVELS_DIFF))

    # def count_errors_for_current_and_nested_contexts(self):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.ERROR.value, LogLevel.ERROR.value + self.LEVELS_DIFF))     
    
    # def count_warnings_and_errors(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.WARNING.value <= level.value < LogLevel.ERROR.value + self.LEVELS_DIFF)

    # def count_warnings_and_errors_for_current_context(self):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.WARNING.value, LogLevel.ERROR.value + self.LEVELS_DIFF))

    # def count_warnings_and_errors_for_current_and_nested_contexts(self):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.WARNING.value, LogLevel.ERROR.value + self.LEVELS_DIFF))
    
    # def count_warnings(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.WARNING.value <= level.value < LogLevel.WARNING.value + self.LEVELS_DIFF)

    # def count_warnings_for_current_context(self):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.WARNING.value, LogLevel.WARNING.value + self.LEVELS_DIFF))

    # def count_warnings_for_current_and_nested_contexts(self):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.WARNING.value, LogLevel.WARNING.value + self.LEVELS_DIFF))        

    # def count_actions(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.ACTION.value <= level.value < LogLevel.ACTION.value + self.LEVELS_DIFF)

    # def count_actions_for_current_context(self):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.ACTION.value, LogLevel.ACTION.value + self.LEVELS_DIFF))

    # def count_actions_for_current_and_nested_contexts(self):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.ACTION.value, LogLevel.ACTION.value + self.LEVELS_DIFF))        

    # def count_notices(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.NOTICE.value <= level.value < LogLevel.NOTICE.value + self.LEVELS_DIFF)

    # def count_notices_for_current_context(self):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.NOTICE.value, LogLevel.NOTICE.value + self.LEVELS_DIFF))

    # def count_notices_for_current_and_nested_contexts(self):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.NOTICE.value, LogLevel.NOTICE.value + self.LEVELS_DIFF))

    # def count_infos(self):
    #     return sum(self._by_level_counts.get(level.name, 0) for level in LogLevel if LogLevel.INFO.value <= level.value < LogLevel.INFO.value + self.LEVELS_DIFF)

    # def count_infos_for_current_context(self):
    #     return self._count_logs(self.current_context, exact_context_match=True, levels=range(LogLevel.INFO.value, LogLevel.INFO.value + self.LEVELS_DIFF))

    # def count_infos_for_current_and_nested_contexts(self):
    #     return self._count_logs(self.current_context, exact_context_match=False, levels=range(LogLevel.INFO.value, LogLevel.INFO.value + self.LEVELS_DIFF))

    def generate_file_name(self, file_prefix=None, include_base_context=True):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if not file_prefix:
            file_prefix = "pipelinelogs"
        if include_base_context:
            file_name = f"{file_prefix}_{timestamp}_{self.base_context}_len{len(self._logs)}.json"
        else:
            file_name = f"{file_prefix}_{timestamp}_len{len(self._logs)}.json"

        return file_name

    def import_logs_from_json(self, json_or_file, logger=None):
        def log_message(message):
            if logger:
                logger.info(message)

        def log_warning(message, exc_info=False):
            if logger:
                logger.warning(message, exc_info=exc_info)

        try:
            imported_logs = None
            if isinstance(json_or_file, str):  # Load from string
                imported_logs = json.loads(json_or_file)
            elif hasattr(json_or_file, 'read'):  # Load from file-like object
                imported_logs = json.load(json_or_file)
            self.add_logs(imported_logs)
            log_message("Successfully imported logs from json.")
        except Exception as e:
            log_warning(f"Failed to import logs from json: {type(e).__name__} - {str(e)}", exc_info=True)


    def generate_execution_summary(self, countable_subject: str, total_countables: int) -> str:
        """Generates a final log message summarizing the pipeline execution."""
        execution_duration = self.get_duration_since_start()
        started_subjects = self.count_total_logs_for_levels(levels=LogLevel.INFO_SUBJECT_STARTED)
        success_subjects = self.count_total_logs_for_levels(levels=[LogLevel.SUCCESS_SUBJECT_COMPLETE, LogLevel.SUCCESS_SUBJECT_COMPLETE_WITH_NOTICES, LogLevel.SUCCESS_SUBJECT_COMPLETE_WITH_WARNINGS])
        failures = self.count_total_logs_for_levels(levels=[LogLevel.FAILED_SUBJECT, LogLevel.FAILED_SUBJECT_COMPLETE_WITH_ERRORS])
        unfinished = started_subjects-success_subjects -failures if started_subjects >= success_subjects + failures else "Unknown"
        skipped = total_countables - success_subjects - failures - unfinished if isinstance(unfinished, int) else "Unknown"

        execution_summary = f"""
        --------------------------------------------------
        Pipeline Execution Report
        --------------------------------------------------
        Base Context: {self.base_context}
        Pipeline ID: {self.id}
        Early Stop: {self.early_stop}
        Early Stop Reason: {self.early_stop_reason}
        Execution Duration: {execution_duration}
        --------------------------------------------------
        Results Summary:
        --------------------------------------------------
        SUBJECT STATUSES:
        - Started : {started_subjects}/{total_countables} {countable_subject}(s)
        - Successes: {success_subjects}/{total_countables} {countable_subject}(s)
        - Failures: {failures}/{total_countables} {countable_subject}(s)
        - Unfinished: {unfinished}/{total_countables} {countable_subject}(s)
        - Skipped: {skipped}/{total_countables} {countable_subject}(s)
        STATUS RANGE SUMMARY:
        - Infos : {self.count_total_logs_for_levels(levels=LogLevel.INFO, entire_level_range=True)}
        - Read Tasks : {self.count_total_logs_for_levels(levels=LogLevel.READ, entire_level_range=True)}
        - In_Memory Tasks : {self.count_total_logs_for_levels(levels=LogLevel.IN_MEMORY_TASK, entire_level_range=True)}
        - Action/Persistance Tasks : {self.count_total_logs_for_levels(levels=LogLevel.ACTION, entire_level_range=True)}
        - Successes : {self.count_total_logs_for_levels(levels=LogLevel.SUCCESS, entire_level_range=True)}
        - Notices: {self.count_total_logs_for_levels(levels=LogLevel.NOTICE, entire_level_range=True)}
        - Warnings: {self.count_total_logs_for_levels(levels=LogLevel.WARNING, entire_level_range=True)}
        - Errors: {self.count_total_logs_for_levels(levels=LogLevel.ERROR, entire_level_range=True)}
        - Failures[Except Pipeline Failure]: {self.count_total_logs_for_levels(levels=LogLevel.FAILED, entire_level_range=True)}
        --------------------------------------------------
        """
        # --------------------------------------------------
        # Detailed Breakdown:
        # --------------------------------------------------
        # Add detailed breakdown for all levels with neat formatting
        # for level in LogLevel:
        #     count = self._by_level_counts.get(level.name, 0)
        #     if count > 0:
        #         execution_summary += f"\n  - {level.name}: {count}"

        # execution_summary += "\n--------------------------------------------------"
        return execution_summary
    
    def get_breakdown_by_loglevel(self):
        """Returns a str log level breakdowns."""

        breakdown_print = """
        --------------------------------------------------
        Detailed LogLevel Breakdown:
        --------------------------------------------------
        """
        for level in LogLevel:
            count = self._by_level_counts.get(level.name, 0)
            if count > 0:
                breakdown_print += f"\n     - {level.name}: {count}  "
        
        breakdown_print += "\n      -------------------------------------------------- \n"
        
        return breakdown_print

    def log_final_description(self, countable_subject: str, total_countables: int, final_description: Optional[str]=None, generallogger: Optional[logging.Logger]=None):
        if final_description:
            final_log_message = final_description
        else:
            final_log_message = self.generate_execution_summary(countable_subject=countable_subject, total_countables=total_countables)
        if self.contains_any_logs_for_level(levels= LogLevel.ERROR, entire_level_range=True):
            generallogger.error(final_log_message)
        elif self.contains_any_logs_for_level(levels= LogLevel.WARNING, entire_level_range=True):
            generallogger.warning(final_log_message)
        else:
            generallogger.info(final_log_message)

    def end(self,countable_subject: Optional[str]=None, total_countables: Optional[int]=None, pipeline_flow_updated:Optional[str]=None, generallogger: Optional[logging.Logger]=None):
        """Logs the end of the pipeline execution with the appropriate final status.
        Args: 
            countable_subject (str, optional): The reference name for the countables processed. --> Can be Tasks, Iterations, Items, Tickers etc.
            total_countables (int): The total number of countables processed in the pipeline.
            generallogger (Optional[logging.Logger], optional): The logger to use for the final log message.
            early_stop (bool, optional): If True, the pipeline execution was stopped early.
            """
       
       
        execution_duration = self.get_duration_since_start()
        final_level = None
        description = f"Pipeline execution completed in {execution_duration}."
        if self.early_stop:
            final_level = LogLevel.FAILED_PIPELINE_EARLY_EXITED
            description = f"Pipeline execution stopped early due to {self.early_stop_reason}. Execution Duration: {execution_duration}."
        elif self.contains_any_logs_for_level(levels= LogLevel.ERROR, entire_level_range=True):
            final_level = LogLevel.FAILED_PIPELINE_COMPLETE_WITH_ERRORS
            description = f"Pipeline execution completed with errors. Execution Duration: {execution_duration}."
        elif self.contains_any_logs_for_level(levels= LogLevel.WARNING, entire_level_range=True):
            final_level = LogLevel.SUCCESS_PIPELINE_COMPLETE_WITH_WARNINGS
        elif self.contains_any_logs_for_level(levels= LogLevel.NOTICE, entire_level_range=True):
            final_level = LogLevel.SUCCESS_PIPELINE_COMPLETE_WITH_NOTICES
        else:
            final_level = LogLevel.SUCCESS_PIPELINE_COMPLETE

        
        execution_summary = self.generate_execution_summary(countable_subject=countable_subject, total_countables=total_countables)
        pipeline_description= description + " \n" + pipeline_flow_updated + " \n" + execution_summary if pipeline_flow_updated else description + " \n" + execution_summary

        self.add_log(ContextLog(
            level=final_level,
            subject="PIPELINE_END",
            description=pipeline_description
        ))

        final_pipeline_descirption_message = pipeline_description + " \n" + self.get_breakdown_by_loglevel()

        if generallogger:
            self.log_final_description(countable_subject=countable_subject, total_countables=total_countables,
                                       final_description=final_pipeline_descirption_message, generallogger=generallogger)
