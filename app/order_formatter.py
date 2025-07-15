# app/order_formatter.py

from datetime import datetime

def format_order_record(order: dict) -> str:
    def fmt_date(date_str):
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str).strftime("%B %d, %Y at %I:%M %p")
        except Exception:
            return str(date_str)

    parts = []

    if order.get("orderno") and order.get("qty"):
        parts.append(f"Order {order['orderno']} includes {order['qty']} units.")

    if order.get("status_name"):
        parts.append(f"Status: {order['status_name']}.")

    if order.get("material_name"):
        parts.append(f"Material: {order['material_name']} ({order.get('material_code', '')}).")

    if order.get("branch_name"):
        parts.append(f"Branch: {order['branch_name']}.")

    if order.get("created_at"):
        parts.append(f"Created on: {fmt_date(order['created_at'])}.")

    if order.get("updated_at"):
        parts.append(f"Last updated: {fmt_date(order['updated_at'])}.")

    return "\n".join(parts)
