import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch
from google.cloud import bigquery
from typing import Any, Dict, List, Union
import json

from ipulse_shared_base_ftredge import DataActionType, LogLevel
from ipulse_shared_data_eng_ftredge import Pipelinemon, ContextLog, read_query_for_rows_matching_dates_bigquery_extended


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


params = {
        "project_id": "data-platform-436809",
        "table_full_path": "data-platform-436809.dev__dp_oracle_fincore_historic_market__datasets.fact_ohlcva_eod",
        "date_column": "date_id",
        "rows_list": {
            "asset_id": "stock_6edcf954-d122-5e8c-ab4b-a267848bbd17"
        },
        "date_range": (date(2024, 10, 1), date(2024, 11, 10))
    }

result = read_query_for_rows_matching_dates_bigquery_extended(**params)
print(format_multiline_message(result))