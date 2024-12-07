import argparse
import os
import logging
from dotenv import load_dotenv, dotenv_values
from bdspackmanager.pack_handler import PackHandler
from bdspackmanager.utils import validate_bds_directory, update_version

def load_config():
    """
    Load configuration from .env and ~/.bdspackrc files.
    Returns a dictionary of merged environment variables.
    """
    home_rc_path = os.path.expanduser("~/.bdspackrc")
    home_config = dotenv_values(home_rc_path) if os.path.exists(home_rc_path) else {}
    load_dotenv()  # Load .env if present
    return {**os.environ, **home_config}

def main():
    """
    Main function to manage Minecraft Bedrock Dedicated Server packs.
    """
    # Load configurations
    config = load_config()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Minecraft Bedrock Dedicated Server Pack Manager")
    parser.add_argument('packs', nargs='*', help=".mcpack, .mcaddon, or pack directory")
    parser.add_argument('--bds-dir', help="Path to the Bedrock Dedicated Server directory (overrides ~/.bdspackrc and .env)")
    parser.add_argument('--world-name', help="Name of the world to target (optional)")
    parser.add_argument('--validate', action='store_true', help="Validate and rescan JSON files")
    parser.add_argument('--update', action='store_true', help="Update @minecraft/server dependency versions in behavior packs")
    parser.add_argument('--update-only', help="Update @minecraft/server versions for packs in the specified folder")
    parser.add_argument('--version', help="Target version for @minecraft/server when using --update or --update-only")
    parser.add_argument('--force', action='store_true', help="Force overwrite of existing packs without confirmation")

    args = parser.parse_args()

    # Ensure valid BDS directory if required
    bds_directory = args.bds_dir or config.get("BDS_DIRECTORY")
    if not bds_directory and not args.update_only:
        logging.error("Invalid or missing BDS directory. Use --bds-dir, ~/.bdspackrc, or set BDS_DIRECTORY in .env.")
        return

    # Handle --update and --update-only
    if args.update or args.update_only:
        if not args.version:
            logging.error("The --update or --update-only flag requires a --version argument to specify the target version.")
            return

        if args.update_only:
            logging.info(f"Updating @minecraft/server versions in {args.update_only} to {args.version}")
            update_version(args.version, args.update_only)
        else:
            logging.info(f"Updating @minecraft/server versions in behavior packs to {args.version}")
            update_version(args.version, os.path.join(bds_directory, 'behavior_packs'))
        logging.info("Update completed.")
        return

    # Initialize PackHandler
    if bds_directory:
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
            logging.warning("No action specified. Use --validate, --update, --update-only, or provide packs to add.")
    else:
        logging.error("Pack management requires a valid BDS directory. Use --update-only for targeted updates.")

if __name__ == "__main__":
    main()
