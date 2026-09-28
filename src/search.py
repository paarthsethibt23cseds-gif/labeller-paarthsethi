"""In-memory search and filter over the records built by dataset.py."""


def filter_records(records, q="", subset="", category="",
                   min_duration=None, max_duration=None):
    q = (q or "").strip().lower()
    out = []
    for r in records:
        if subset and r["subset"] != subset:
            continue
        if category and category not in r["categories"]:
            continue
        if min_duration is not None and r["duration"] < min_duration:
            continue
        if max_duration is not None and r["duration"] > max_duration:
            continue
        if q and not any(q in label.lower() for label in r["labels"]):
            continue
        out.append(r)
    return out
