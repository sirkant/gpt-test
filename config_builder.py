import json

def create_static_json_file():
    static_config = {
        "root": "./",
        "routes": {
            "/**": "index.html"
        }
    }

    return json.dumps(static_config, indent=2)