import os
import json

# Script to generate metadata based on packs from folders

normal_folder_relative = 'normal'
normal_folder = os.path.abspath(normal_folder_relative)
normal_metadata = []

# Function to process each pack folder
# Get name and version from each pack's json
def process_pack_folder(pack_path):
    with open(pack_path, 'r') as f:
        metadata = f.read()
        metadata_json = json.loads(metadata)
        normal_metadata.append({
            "id": metadata_json.get("id", "unknown"),
            "version": metadata_json.get("version", "unknown")
        })


# Pass through all packs in the normal folder
for pack in os.listdir(normal_folder):
    pack_path = os.path.join(normal_folder, pack)
    if os.path.isfile(pack_path):
        # Process each pack folder
        process_pack_folder(pack_path)

# Construct full metadata
full_metadata = {
    "normalPacks": normal_metadata,
    "specialPacks": []
}

# Save the full metadata to a file
metadata_file = os.path.abspath('metadata.json')
with open(metadata_file, 'w') as f:
    json.dump(full_metadata, f, indent=2)