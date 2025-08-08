from datetime import datetime
from utils.slack_notify import notify_slack

def compare_and_notify(label, url, old_data, new_data, data_type="table"):
    changes = []
    if data_type == "table":
        # Compare lists of dicts by keys
        if not (isinstance(old_data, list) and isinstance(new_data, list)):
            return False
        # Only compare if both have at least one row
        if old_data and new_data:
            old_row = old_data[0]
            new_row = new_data[0]
            for key in new_row:
                old_val = old_row.get(key)
                new_val = new_row.get(key)
                if old_val != new_val:
                    try:
                        old_num = float(str(old_val).replace('%',''))
                        new_num = float(str(new_val).replace('%',''))
                        diff = new_num - old_num
                        direction = 'up' if diff > 0 else 'down'
                        percent = abs(diff)
                        changes.append(f"{key} - from {old_val} to {new_val} ({direction} by {percent:.2f})")
                    except Exception:
                        changes.append(f"{key} changed from {old_val} to {new_val}")
    elif data_type == "text":
        if old_data != new_data:
            changes.append("Text content changed.")
    if changes:
        message = (
            f"Date and Time: {datetime.now().strftime('%m/%d/%Y %H:%M')}\n"
            f"Website URL: {url}\n"
            f"Changes:\n" + "\n".join(changes)
        )
        notify_slack(message)
        return True
    return False 