import csv
import json
import re
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


API_URL = "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items"
OUTPUT_DIR = Path("output")
STATE_FILE = Path("state.json")


# Convert column names to snake_case
def snake_case(name):
    name = name.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "_", name).strip("_")


# Download and process each CSV
def process_dataset(dataset):
    url = dataset["distribution"][0]["downloadURL"]
    filename = url.split("/")[-1]
    output_file = OUTPUT_DIR / filename

    with urllib.request.urlopen(url) as response:
        reader = csv.reader(
            (line.decode("utf-8-sig") for line in response)
        )

        with output_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = next(reader)
            writer.writerow([snake_case(col) for col in header])
            writer.writerows(reader)

    print(f"Processed: {filename}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load metadata from previous run
    if STATE_FILE.exists():
        with STATE_FILE.open() as f:
            state = json.load(f)
    else:
        state = {}

    # Get CMS datasets
    with urllib.request.urlopen(API_URL) as response:
        datasets = json.load(response)

    # Select new or modified Hospital datasets
    datasets_to_process = [
        d for d in datasets
        if "Hospitals" in d.get("theme", [])
        and state.get(d["identifier"]) != d.get("modified")
    ]

    # Process files in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(process_dataset, datasets_to_process))

    # Save metadata for the next run
    for d in datasets_to_process:
        state[d["identifier"]] = d.get("modified")

    with STATE_FILE.open("w") as f:
        json.dump(state, f, indent=2)


if __name__ == "__main__":
    main()
