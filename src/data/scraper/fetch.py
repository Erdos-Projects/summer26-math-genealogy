import asyncio
import json
import os

import aiohttp
import async_timeout

from parse import parse

ERROR_STRING = 'You have specified an ID that does not exist in the database.'

DATA_FILE = 'data.json'
ERRORS_FILE = 'errors.txt'

START_ID = 1
END_ID = 500000        # change this if you want
SAVE_EVERY = 1000
CONCURRENCY = 5

errors = {}
data = []
bad_ids = set()


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, tuple):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, set):
        return list(obj)
    else:
        return obj


def save_data():
    print("Saving data...")

    safe_data = make_json_safe(data)

    with open(DATA_FILE, "w", encoding="utf-8") as outfile:
        json.dump({"nodes": safe_data}, outfile, indent=2, ensure_ascii=False)

    with open(ERRORS_FILE, "w", encoding="utf-8") as outfile:
        for mgp_id, error in errors.items():
            outfile.write(f"{mgp_id},{error}\n")

    print(f"Saved {len(data)} records.")


print("Loading existing data...")

try:
    with open(DATA_FILE, "r", encoding="utf-8") as infile:
        data = json.load(infile).get("nodes", [])
    print(f"Found {len(data)} existing records.")
except Exception:
    print("No existing data found.")
    data = []


existing = set()

for item in data:
    try:
        existing.add(int(item["id"]))
    except Exception:
        pass

print(f"Skipping {len(existing)} already saved records.")


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            print(f"fetching {url}")
            return await response.text()


async def fetch_by_id(session, sem, mgp_id):
    async with sem:
        url = f"https://genealogy.math.ndsu.nodak.edu/id.php?id={mgp_id}"

        try:
            raw_html = await fetch(session, url)

            if ERROR_STRING in raw_html:
                print(f"bad id={mgp_id}")
                bad_ids.add(mgp_id)
                return

            try:
                info_dict = parse(mgp_id, raw_html)

                if int(info_dict["id"]) not in existing:
                    data.append(info_dict)
                    existing.add(int(info_dict["id"]))

                print(f"saved id={mgp_id}")

            except Exception as e:
                print(f"Failed to parse id={mgp_id}")
                errors[mgp_id] = f"parse error: {e}"

        except Exception as e:
            print(f"Failed to fetch id={mgp_id}")
            errors[mgp_id] = f"fetch error: {e}"


async def main():
    sem = asyncio.BoundedSemaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:
        for batch_start in range(START_ID, END_ID + 1, SAVE_EVERY):
            batch_end = min(batch_start + SAVE_EVERY, END_ID + 1)

            print()
            print(f"Processing IDs {batch_start} to {batch_end - 1}")

            tasks = [
                fetch_by_id(session, sem, mgp_id)
                for mgp_id in range(batch_start, batch_end)
                if mgp_id not in existing and mgp_id not in bad_ids
            ]

            if tasks:
                await asyncio.gather(*tasks)

            save_data()


asyncio.run(main())

print("Final save...")
save_data()

print("Done!")