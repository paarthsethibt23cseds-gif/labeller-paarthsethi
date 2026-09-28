"""Load ActivityNet v1.3 annotations and flatten them into one record per video."""
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def find_dataset():
    """Full dataset if downloaded, else the small committed sample."""
    override = os.environ.get("DATASET_PATH")
    if override:
        return Path(override)
    for name in ("activity_net.json", "sample.json"):
        p = DATA_DIR / name
        if p.exists():
            return p
    raise FileNotFoundError("No dataset found in data/. Run: bash setup.sh")


def load_records(path=None):
    path = Path(path) if path else find_dataset()
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    # label -> broader category (parent node in the taxonomy)
    parents = {n["nodeName"]: n.get("parentName") for n in raw.get("taxonomy", [])}

    records = []
    for vid, e in raw.get("database", {}).items():
        segments = []
        for a in e.get("annotations") or []:
            seg = a.get("segment") or []
            if a.get("label") and len(seg) == 2:
                segments.append({"label": a["label"],
                                 "start": round(seg[0], 1), "end": round(seg[1], 1)})
        labels = sorted({s["label"] for s in segments})
        records.append({
            "id": vid,
            "url": e.get("url") or f"https://www.youtube.com/watch?v={vid}",
            "subset": e.get("subset", "unknown"),
            "duration": round(float(e.get("duration") or 0), 1),
            "resolution": e.get("resolution", ""),
            "segments": segments,
            "labels": labels,
            "categories": sorted({parents[l] for l in labels if parents.get(l)}),
        })
    records.sort(key=lambda r: r["id"])
    return records
