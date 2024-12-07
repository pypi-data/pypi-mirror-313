import os
import json
import zipfile
import shutil
import logging
import re
from bdspackmanager.manifest_parser import ManifestParser
from bdspackmanager.json_updater import JSONUpdater


class PackHandler:
    def __init__(self, bds_directory, world_name=None, force=False):
        """
        Initializes a PackHandler object.

        Parameters:
        - bds_directory (str): The directory path of the BDS installation.
        - world_name (str, optional): The name of the world to target.
        - force (bool, optional): Whether to overwrite existing packs without confirmation.
        """
        self.bds_directory = bds_directory
        self.resource_packs_dir = os.path.join(bds_directory, 'resource_packs')
        self.behavior_packs_dir = os.path.join(bds_directory, 'behavior_packs')
        self.worlds_dir = os.path.join(bds_directory, 'worlds')
        self.world_name = world_name if world_name else self._select_world()
        self.json_updater = JSONUpdater(bds_directory, self.world_name)
        self.force = force
        logging.basicConfig(level=logging.INFO)

    def _select_world(self):
        """
        Prompts the user to select a world if multiple worlds are found.
        """
        worlds = [d for d in os.listdir(self.worlds_dir) if os.path.isdir(os.path.join(self.worlds_dir, d))]
        if not worlds:
            raise ValueError("No worlds found in the 'worlds' directory.")
        if len(worlds) == 1:
            return worlds[0]
        print("Multiple worlds found. Please select one:")
        for idx, world in enumerate(worlds):
            print(f"{idx + 1}: {world}")
        selection = int(input("Enter the number of the world you want to use: ")) - 1
        return worlds[selection]

    def add_pack(self, pack_path):
        """
        Adds a pack to the pack handler.
        """
        if not os.path.exists(pack_path):
            logging.error(f"Pack path does not exist: {pack_path}")
            return

        if pack_path.endswith('.mcaddon'):
            self._unzip_mcaddon(pack_path)
        elif pack_path.endswith('.mcpack'):
            self._unzip_pack(pack_path)
        elif os.path.isdir(pack_path):
            self._process_pack_directory(pack_path)
        else:
            logging.error(f"Invalid pack format: {pack_path}")

    def _unzip_mcaddon(self, addon_path):
        """
        Unzips the specified MCAddon file and processes the pack directories.
        """
        with zipfile.ZipFile(addon_path, 'r') as zip_ref:
            for item in zip_ref.namelist():
                if item.endswith('/'):
                    dir_name = os.path.basename(os.path.normpath(item))
                    extract_dir = self._generate_folder_name(dir_name)
                    zip_ref.extractall(extract_dir)
                    self._process_pack_directory(extract_dir)

    def _unzip_pack(self, zip_path):
        """
        Unzips the pack located at the given zip_path and processes its contents.
        """
        pack_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = self._generate_folder_name(pack_name)
        logging.info(f"Extracting pack to {extract_dir}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        self._process_pack_directory(extract_dir)

    def _process_pack_directory(self, directory):
        """
        Processes a pack directory by moving it to the appropriate pack folder and updating JSON files.
        """
        manifest_path = os.path.join(directory, 'manifest.json')
        if not os.path.exists(manifest_path):
            logging.error(f"Manifest.json not found in {directory}")
            return

        try:
            with open(manifest_path, 'r') as file:
                manifest = json.load(file)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse manifest in {directory}: {e}")
            return

        pack_type = ManifestParser.identify_pack_type(manifest_path)
        if pack_type == 'resource':
            destination_dir = self.resource_packs_dir
        elif pack_type == 'behavior':
            destination_dir = self.behavior_packs_dir
        else:
            logging.error(f"Unknown pack type in {directory}")
            return

        pack_name = os.path.basename(directory)
        destination_path = os.path.join(destination_dir, pack_name)

        if os.path.exists(destination_path):
            if not self.force:
                confirmation = input(f"Pack {pack_name} already exists. Overwrite? (y/n): ")
                if confirmation.lower() != 'y':
                    logging.info(f"Skipping {pack_name}")
                    return
            shutil.rmtree(destination_path)
            logging.info(f"Removed existing directory {destination_path}")

        shutil.move(directory, destination_path)
        logging.info(f"Pack {pack_name} added to {destination_dir}")

        self.json_updater.update_valid_known_packs(pack_type, manifest)
        self.json_updater.update_world_packs(pack_type, manifest)

    def _generate_folder_name(self, base_name):
        """
        Generates a folder name by cleaning and truncating the base name.
        """
        cleaned_name = re.sub(r'[^a-zA-Z0-9 ]', '', base_name)[:10]
        return os.path.join(self.bds_directory, cleaned_name)
