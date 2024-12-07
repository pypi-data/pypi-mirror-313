import os
import json
import logging


class JSONUpdater:
    def __init__(self, bds_directory, world_name=""):
        """
        Initializes a JSONUpdater object.

        Parameters:
        - bds_directory (str): The directory path of the BDS server.
        - world_name (str): The name of the world.
        """
        self.bds_directory = bds_directory
        self.world_name = world_name
        self.world_dir = os.path.join(bds_directory, 'worlds', world_name) if world_name else None
        logging.basicConfig(level=logging.INFO)

    def update_valid_known_packs(self, pack_type, manifest):
        """
        Update the valid_known_packs.json file with the new pack information.
        """
        valid_known_packs_path = os.path.join(self.bds_directory, 'valid_known_packs.json')
        pack_path = f"{pack_type}_packs/{manifest['header']['name']}"
        new_entry = {
            "file_system": "RawPath",
            "path": pack_path,
            "uuid": manifest['header']['uuid'],
            "version": ".".join(map(str, manifest['header']['version']))
        }

        if os.path.exists(valid_known_packs_path):
            with open(valid_known_packs_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        updated = False
        for entry in data:
            if entry.get("uuid") == new_entry["uuid"]:
                entry.update(new_entry)
                updated = True
                break

        if not updated:
            data.append(new_entry)

        with open(valid_known_packs_path, 'w') as file:
            json.dump(data, file, indent=4)

        logging.info(f"Updated valid_known_packs.json with pack {manifest['header']['uuid']}")

    def update_world_packs(self, pack_type, manifest):
        """
        Update or create world resource/behavior pack JSON files with new pack information.
        """
        if not self.world_name:
            logging.warning("World name not specified. Skipping world-specific updates.")
            return

        json_file = 'world_resource_packs.json' if pack_type == 'resource' else 'world_behavior_packs.json'
        file_path = os.path.join(self.world_dir, json_file)
        new_entry = {"pack_id": manifest['header']['uuid'], "version": manifest['header']['version']}

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        if new_entry not in data:
            data.append(new_entry)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        logging.info(f"Updated {json_file} with pack {manifest['header']['uuid']}")

    def validate_json_files(self):
        """
        Validate the presence of packs in world-specific JSON files.
        """
        if not self.world_name:
            logging.warning("World name not specified. Skipping validation.")
            return

        resource_json = os.path.join(self.world_dir, 'world_resource_packs.json')
        behavior_json = os.path.join(self.world_dir, 'world_behavior_packs.json')
        self._validate_json(resource_json, os.path.join(self.bds_directory, 'resource_packs'))
        self._validate_json(behavior_json, os.path.join(self.bds_directory, 'behavior_packs'))

    def _validate_json(self, json_file, pack_dir):
        """
        Validate a JSON file against the existence of packs in a directory.
        """
        if not os.path.exists(json_file):
            logging.warning(f"{json_file} does not exist. Skipping validation.")
            return

        with open(json_file, 'r') as file:
            data = json.load(file)

        for entry in data:
            pack_uuid = entry.get('pack_id')
            if not pack_uuid:
                continue
            if not any(pack_uuid in fname for fname in os.listdir(pack_dir)):
                logging.warning(f"Pack {pack_uuid} in {json_file} is missing from {pack_dir}.")
            else:
                logging.info(f"Pack {pack_uuid} validated successfully in {json_file}.")
