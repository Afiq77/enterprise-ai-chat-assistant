# app/order_filter.py

import re
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

def parse_date_range(query: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    now = datetime.now()
    query = query.lower()

    if "today" in query:
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
    elif "yesterday" in query:
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
    elif "this month" in query:
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = start + relativedelta(months=1)
    elif "last month" in query:
        end = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start = end - relativedelta(months=1)
    else:
        return None, None

    return start, end

def filter_orders(orders: List[dict], query: str) -> Tuple[List[dict], str]:
    query = query.lower()
    filtered = orders

    if "completed" in query:
        filtered = [o for o in filtered if "completed" in (o.get("status_name", "").lower())]
    elif "cancelled" in query:
        filtered = [o for o in filtered if "cancelled" in (o.get("status_name", "").lower())]

    start, end = parse_date_range(query)
    if start and end:
        def in_range(dt_str):
            try:
                dt = date_parser.parse(dt_str)
                return start <= dt < end
            except:
                return False

        filtered = [o for o in filtered if in_range(o.get("created_at"))]
        summary = f"{len(filtered)} orders created between {start.date()} and {end.date()}."
        return filtered, summary

    summary = f"{len(filtered)} matching orders found." if filtered else "No orders matched."
    return filtered, summary
