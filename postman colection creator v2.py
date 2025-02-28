import json
from urllib.parse import urlparse

# Read URL list from txt file
with open(r"C:\Users\Benwari Ezekiel\Downloads\urls.txt", "r") as file:
    urls = [line.strip() for line in file.readlines()]

# Build Postman Collection structure
collection = {
    "info": {
        "name": "URL List Collection",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": []
}

for url in urls:
    parsed_url = urlparse(url)

    # Build Postman-style URL object (recommended format for compatibility)
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
                print("uequal params")
        postman_url["query"] = query_params

    collection["item"].append({
        "name": url,  # Use full URL as the name
        "request": {
            "method": "GET",
            "url": postman_url
        }
    })

# Write to JSON file
with open(r"C:\Users\Benwari Ezekiel\Documents\postman_collection.json", "w") as file:
    json.dump(collection, file, indent=4)

print("✅ Postman collection JSON generated: postman_collection.json")
