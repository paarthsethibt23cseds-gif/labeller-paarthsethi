import os
import urllib.request

URL = ("https://github.com/activitynet/ActivityNet/raw/refs/heads/master/"
       "Evaluation/data/activity_net.v1-3.min.json")
DEST = os.path.join("data", "activity_net.json")

os.makedirs("data", exist_ok=True)
print("Downloading ActivityNet annotations...")
urllib.request.urlretrieve(URL, DEST)
print("Saved to", DEST, "-", os.path.getsize(DEST), "bytes")
