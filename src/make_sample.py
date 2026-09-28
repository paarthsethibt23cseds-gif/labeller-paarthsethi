"""Write data/sample.json (first 60 labeled videos + taxonomy) from the full file.
Run once after downloading, then commit sample.json as an offline fallback."""
import json
from pathlib import Path

data = Path(__file__).resolve().parent.parent / "data"
raw = json.load(open(data / "activity_net.json", encoding="utf-8"))
keep = [(k, v) for k, v in raw["database"].items() if v.get("annotations")][:60]
json.dump({"version": raw.get("version"), "taxonomy": raw["taxonomy"],
           "database": dict(keep)}, open(data / "sample.json", "w"))
print("wrote", data / "sample.json")
