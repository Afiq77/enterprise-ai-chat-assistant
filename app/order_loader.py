# app/order_loader.py

import json
import os
import hashlib

ORDER_JSON_PATH = "app/data/orders.json"
CHECKSUM_FILE = "app/data/order_checksum.txt"


def load_raw_orders():
    # 🔄 This should be replaced with your own data loading logic or static file
    with open(ORDER_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_order_checksum(orders) -> str:
    data_str = json.dumps(orders, default=str, sort_keys=True)
    return hashlib.md5(data_str.encode("utf-8")).hexdigest()


def dump_orders_to_json():
    print("🔄 Loading and checking orders...")

    orders = load_raw_orders()

    new_checksum = get_order_checksum(orders)
    if os.path.exists(CHECKSUM_FILE):
        with open(CHECKSUM_FILE, "r") as f:
            old_checksum = f.read().strip()
        if new_checksum == old_checksum:
            print("⚡ Order data unchanged — skipping dump.")
            return orders

    with open(ORDER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

    with open(CHECKSUM_FILE, "w") as f:
        f.write(new_checksum)

    print(f"✅ {len(orders)} orders cached successfully.")
    return orders
