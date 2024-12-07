import argparse
import os
import logging
from dotenv import load_dotenv
from bdspackmanager.pack_handler import PackHandler
from bdspackmanager.utils import validate_bds_directory, update_version

def main():
    """
    Main function to manage Minecraft Bedrock Dedicated Server packs.
    This function performs the following tasks:
    1. Loads environment variables.
    2. Configures logging.
    3. Sets up argument parsing for command-line arguments.
    4. Resolves the Bedrock Dedicated Server (BDS) directory.
    5. Handles the --update flag to update @minecraft/server dependency versions.
    6. Initializes the PackHandler for managing packs.
    7. Validates and rescans JSON files if --validate flag is provided.
    8. Adds packs specified in the command-line arguments.
    Command-line Arguments:
    - packs: List of .mcpack, .mcaddon, or pack directories to add.
    - --bds-dir: Path to the Bedrock Dedicated Server directory (can also be set in .env).
    - --world-name: Name of the world to target (optional).
    - --validate: Validate and rescan JSON files.
    - --update: Update @minecraft/server dependency versions in behavior packs.
    - --version: Target version for @minecraft/server when using --update.
    - --force: Force overwrite of existing packs without confirmation.
    Returns:
    None
    """
    # Load environment variables
    load_dotenv()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Minecraft Bedrock Dedicated Server Pack Manager")
    parser.add_argument('packs', nargs='*', help=".mcpack, .mcaddon, or pack directory")
    parser.add_argument('--bds-dir', help="Path to the Bedrock Dedicated Server directory (can also be set in .env)")
    parser.add_argument('--world-name', help="Name of the world to target (optional)")
    parser.add_argument('--validate', action='store_true', help="Validate and rescan JSON files")
    parser.add_argument('--update', action='store_true', help="Update @minecraft/server dependency versions in behavior packs")
    parser.add_argument('--version', help="Target version for @minecraft/server when using --update")
    parser.add_argument('--force', action='store_true', help="Force overwrite of existing packs without confirmation")
    parser.add_argument('--update-only', help="Update @minecraft/server version for packs in the specified directory")

    args = parser.parse_args()

    # Handle --update-only
    if args.update_only:
        if not args.version:
            logging.error("The --update-only flag requires a --version argument to specify the target version.")
            return

        logging.info(f"Updating @minecraft/server dependency to version {args.version} in directory: {args.update_only}")
        update_version(args.version, args.update_only)
        logging.info("Update-only operation completed.")
        return

    # Resolve BDS directory
    bds_directory = args.bds_dir or os.getenv("BDS_DIRECTORY")
    if not bds_directory or not validate_bds_directory(bds_directory):
        logging.error("Invalid or missing BDS directory. Use --bds-dir or set BDS_DIRECTORY in your .env file.")
        return

    # Handle --update
    if args.update:
        if not args.version:
            logging.error("The --update flag requires a --version argument to specify the target version.")
            return

        logging.info(f"Updating @minecraft/server dependency to version {args.version}")
        update_version(args.version, bds_directory)
        logging.info("Update completed.")
        return

    # Initialize PackHandler
    pack_handler = PackHandler(bds_directory, world_name=args.world_name, force=args.force)

    if args.validate:
        # Validate and rescan JSON files
        pack_handler.json_updater.validate_json_files()
        logging.info("Validation completed.")
    elif args.packs:
        # Add packs
        for pack in args.packs:
            try:
                logging.info(f"Processing pack: {pack}")
                pack_handler.add_pack(pack)
            except Exception as e:
                logging.error(f"Error processing pack {pack}: {e}")
    else:
        logging.warning("No action specified. Use --validate, --update, or provide packs to add.")

if __name__ == "__main__":
    main()
