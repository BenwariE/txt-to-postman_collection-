import json
import os
from urllib.parse import urlparse

# Read URL list from txt file
with open(r"C:\Users\Benwari Ezekiel\Downloads\urls.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

# Define output folder
output_folder = r"C:\Users\Benwari Ezekiel\Documents\Postman_Collections"
os.makedirs(output_folder, exist_ok=True)

# Split URLs into chunks of 1000
chunk_size = 1000
url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

# Process each chunk into a separate collection file
for index, chunk in enumerate(url_chunks, start=1):
    collection = {
        "info": {
            "name": f"URLs Collection {index}",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    for url in chunk:
        parsed_url = urlparse(url)

        # Build Postman-style URL object
        postman_url = {
            "raw": url,
            "protocol": parsed_url.scheme,
            "host": parsed_url.netloc.split('.'),
            "path": parsed_url.path.strip('/').split('/') if parsed_url.path else [],
        }

        # Add query parameters if present
        if parsed_url.query:
            query_params = []
            for param in parsed_url.query.split('&'):
                try:
                    key, value = param.split('=', 1)
                    query_params.append({"key": key, "value": value})
                except:
                    print(f"⚠️ Skipped malformed query parameter in URL: {url}")
            postman_url["query"] = query_params

        collection["item"].append({
            "name": url,
            "request": {
                "method": "GET",
                "url": postman_url
            }
        })

    # Write each collection to a separate file
    collection_file_path = os.path.join(output_folder, f"urls_collection_{index}.json")
    with open(collection_file_path, "w") as file:
        json.dump(collection, file, indent=4)

    print(f"✅ Collection saved: {collection_file_path}")

print("✅ All collections generated successfully.")
