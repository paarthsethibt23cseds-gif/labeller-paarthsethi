# ActivityNet Label Explorer

## Summary Card
| Section | What I did | Confidence (1-5) | Files |
|---|---|---|---|
| Dataset | Chose ActivityNet v1.3 annotations (video, real human labels) | 3.5 | [dataset.py](src/dataset.py), [download_data.py](src/download_data.py) |
| Ingest + summary | Parse JSON + taxonomy into one record per video; paginated table UI | 3 | [dataset.py](src/dataset.py), [app.py](src/app.py) |
| Search + filter | In-memory filter: label keyword, subset, category, duration range | 4 | [search.py](src/search.py) |
| Setup / run | `setup.sh` (venv, deps, dataset download), `run.sh` | 4 | [setup.sh](setup.sh), [run.sh](run.sh) |
| Deploy (bonus) |  "not done" | N/A | |

## Dataset
**ActivityNet v1.3** (annotation file `activity_net.v1-3.min.json`, ~4.7 MB, 19,994 videos).
- Why: video dataset with real, pre-attached annotations (labeled time segments), plus duration, subset, resolution and a category taxonomy, so the summary and filters have real metadata to work with. Only the annotation file is needed, not the videos.
- Searched/tried: I came across it at the first search and moved forward with it.

## How to run (Mac/Linux, needs only Python 3 and bash)
```bash
bash setup.sh   # creates .venv, installs Flask, downloads the annotations
bash run.sh     # then open http://localhost:5000
```
If the download fails, the app falls back to `data/sample.json` (60 real entries).
JSON API: `/api/videos?q=surf&subset=validation&limit=20`

## Assumptions
- One row per video. Labeled segments are listed inside the row with start/end seconds.
- "Category" is the parent node of a label in the dataset's taxonomy.
- Videos with no annotations (e.g. the hidden-label test split) are kept and shown as "no labels".
- Keyword search is a case-insensitive substring match on labels only.
- Data is loaded once at startup and filtered in memory (fine at ~20k rows).

## Time spent
- Dataset search: 25 minutes
- Setup + scripts: 90 minutes
- Parser + summary UI: 60 minutes
- Search/filter: 5 minutes
- README + testing: 10 minutes

## Reflections
**What would I improve with two more hours?** 
Could add a preview youtube video without clicking the actual video just for the ease of testing on the same frontend and also make the frontend more hands-on and easy to work on.

**One thing I didn't know how to do, and how I figured it out:** 
The raw-URL 404, wrong-folder issue, python vs python3.
