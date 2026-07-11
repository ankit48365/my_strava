import json
import glob
import os

# Match files like: file_name_date****_.json
for infile in glob.glob("weather_*.json"):
    outfile = os.path.splitext(infile)[0] + ".ndjson"

    with open(infile) as f:
        data = json.load(f)   # expects JSON array

    with open(outfile, "w") as f:
        for row in data:
            f.write(json.dumps(row) + "\n")

    print(f"Converted {infile} → {outfile}")