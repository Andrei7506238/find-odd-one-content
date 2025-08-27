import os
import json

normal_folder_relative = 'normal'
# Resolve normal folder relative to this script file
base_dir = os.path.dirname(os.path.abspath(__file__))
normal_folder = os.path.join(base_dir, normal_folder_relative)
normal_metadata = []

# Function to process each pack file (expecting JSON)
def process_pack_file(pack_path):
    if not pack_path.lower().endswith('.json'):
        print(f"skipping non-json: {pack_path}")
        return

    encodings = ['utf-8', 'utf-8-sig', 'cp1250', 'latin-1']
    metadata_json = None
    for enc in encodings:
        try:
            with open(pack_path, 'r', encoding=enc) as f:
                metadata_json = json.load(f)
            break
        except UnicodeDecodeError:
            # try next encoding
            continue
        except json.JSONDecodeError as e:
            print(f"invalid json in {pack_path} (encoding {enc}): {e}")
            return
        except Exception as e:
            print(f"error reading {pack_path} with encoding {enc}: {e}")
            return

    if metadata_json is None:
        print(f"failed to read {pack_path} with available encodings")
        return

    normal_metadata.append({
        "id": metadata_json.get("id", "unknown"),
        "version": metadata_json.get("version", "unknown"),
        "starsPrice": metadata_json.get("starsPrice", 0),
        "coinsPrice": metadata_json.get("coinsPrice", 0)
    })


# Pass through all files in the normal folder
if not os.path.isdir(normal_folder):
    print(f"normal folder not found: {normal_folder}")
else:
    for entry in os.listdir(normal_folder):
        pack_path = os.path.join(normal_folder, entry)
        if os.path.isfile(pack_path):
            process_pack_file(pack_path)

# Construct full metadata
full_metadata = {
    "normalPacks": normal_metadata,
    "specialPacks": []
}

# Save the full metadata to a file next to the script
metadata_file = os.path.join(base_dir, 'metadata.json')
with open(metadata_file, 'w', encoding='utf-8') as f:
    json.dump(full_metadata, f, indent=2)

print(f"wrote metadata to {metadata_file}")