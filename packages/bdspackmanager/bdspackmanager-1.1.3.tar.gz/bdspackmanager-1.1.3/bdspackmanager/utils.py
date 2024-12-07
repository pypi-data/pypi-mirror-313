import zipfile
import os
import json
import logging

def validate_bds_directory(directory):
    """
    Validates that the given directory contains the required subdirectories for a BDS (Bedrock Dedicated Server) setup.

    Args:
        directory (str): The path to the directory to validate.

    Returns:
        bool: True if the directory contains all required subdirectories ('resource_packs', 'behavior_packs', 'worlds'), False otherwise.
    """
    required_dirs = ['resource_packs', 'behavior_packs', 'worlds']
    return all(os.path.exists(os.path.join(directory, d)) for d in required_dirs)


def update_version(target_version, pack_dir):
    """
    Updates the @minecraft/server dependency version in all manifest files within the specified directory.
    Supports handling `.mcpack` files by extracting, updating, and re-zipping them.

    Parameters:
    - target_version (str): The desired version for @minecraft/server.
    - pack_dir (str): The directory containing packs to be updated.

    Returns:
    - None
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    if not os.path.exists(pack_dir):
        logging.error(f"Specified directory does not exist: {pack_dir}")
        return

    logging.info(f"Updating pack versions in: {pack_dir}")
    updated_packs = 0

    for root, _, files in os.walk(pack_dir):
        for file in files:
            if file.endswith('.mcpack'):
                # Handle mcpack files
                pack_path = os.path.join(root, file)
                temp_dir = os.path.splitext(pack_path)[0]

                try:
                    with zipfile.ZipFile(pack_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    logging.info(f"Extracted {pack_path} to {temp_dir}")

                    if _update_manifest_version(temp_dir, target_version):
                        updated_packs += 1
                        _repack_mcpack(temp_dir, pack_path)
                        logging.info(f"Updated and re-packed {pack_path}")

                    # Clean up extracted directory
                    _clean_up(temp_dir)

                except Exception as e:
                    logging.error(f"Failed to process {pack_path}: {e}")

            elif file == 'manifest.json':
                # Handle raw directories with manifest.json
                manifest_dir = os.path.dirname(os.path.join(root, file))
                if _update_manifest_version(manifest_dir, target_version):
                    updated_packs += 1

    logging.info(f"Completed updates. Total packs updated: {updated_packs}")


def _update_manifest_version(directory, target_version):
    """
    Updates the @minecraft/server version in the manifest.json file within the specified directory.

    Parameters:
    - directory (str): The directory containing the manifest.json file.
    - target_version (str): The desired version for @minecraft/server.

    Returns:
    - bool: True if the manifest was updated, False otherwise.
    """
    manifest_path = os.path.join(directory, 'manifest.json')
    if not os.path.exists(manifest_path):
        logging.warning(f"Manifest not found in {directory}")
        return False

    try:
        with open(manifest_path, 'r') as file:
            manifest = json.load(file)

        updated = False
        for dependency in manifest.get('dependencies', []):
            if dependency.get('module_name') == '@minecraft/server':
                current_version = dependency.get('version')
                if current_version != target_version:
                    dependency['version'] = target_version
                    updated = True
                    logging.info(f"Updated {manifest_path}: {current_version} -> {target_version}")

        if updated:
            with open(manifest_path, 'w') as file:
                json.dump(manifest, file, indent=4)

        return updated

    except Exception as e:
        logging.error(f"Error updating manifest in {directory}: {e}")
        return False


def _repack_mcpack(directory, output_file):
    """
    Repackages a directory into an .mcpack file.

    Parameters:
    - directory (str): The directory to repackage.
    - output_file (str): The path to save the .mcpack file.

    Returns:
    - None
    """
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zip_ref.write(file_path, arcname)
    logging.info(f"Repacked directory {directory} into {output_file}")


def _clean_up(directory):
    """
    Deletes a directory and its contents.

    Parameters:
    - directory (str): The directory to delete.

    Returns:
    - None
    """
    import shutil
    try:
        shutil.rmtree(directory)
        logging.info(f"Cleaned up directory: {directory}")
    except Exception as e:
        logging.error(f"Failed to clean up {directory}: {e}")
