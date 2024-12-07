# BdsPackManager

**BdsPackManager** is a command-line tool designed for managing resource and behavior packs on a Minecraft Bedrock Dedicated Server (BDS). It allows you to easily add, validate, and manage packs, ensuring that your server is always up-to-date with the latest content.

## Features

- **Add Packs**: Supports adding `.mcpack`, `.mcaddon`, and directories containing valid `manifest.json` files.
- **Automatic Unzipping**: Automatically extracts and processes `.mcpack` and `.mcaddon` files.
- **Validation**: Ensures consistency between the packs listed in your server's configuration files and the actual content in the `resource_packs` and `behavior_packs` directories.
- **Configurable**: Specify the server directory using command-line arguments, environment variables, or `.env` files.
- **Interactive**: Prompts before overwriting existing packs to prevent accidental data loss.

## Installation

1. **Install via pip**:
    ```bash
    pip install bdspackmanager
    ```

2. **Set up your environment**:
    - Optionally, create a `.env` file in the root directory to store your BDS directory path:
      ```
      BDS_DIRECTORY=/path/to/your/bedrock_server
      ```

## Usage

### Command-line Arguments

```bash
python -m bds_pack_manager.main [OPTIONS] PACKS...
```

#### Options:
- `PACKS...`: One or more paths to `.mcpack`, `.mcaddon`, or directories containing a valid `manifest.json`.
- `--bds-dir`: Specify the path to the Bedrock Dedicated Server directory (overrides `.env` and environment variable).
- `--validate`: Validate and rescan JSON files for consistency with the actual content in the `resource_packs` and `behavior_packs` directories.

### Example Usage

1. **Adding a Pack**:
   ```bash
   python -m bds_pack_manager.main /path/to/your_pack.mcpack
   ```

2. **Adding Multiple Packs**:
   ```bash
   python -m bds_pack_manager.main /path/to/your_pack_1.mcpack /path/to/your_pack_2.mcaddon /path/to/pack_directory
   ```

3. **Validating Pack Consistency**:
   ```bash
   python -m bds_pack_manager.main --validate
   ```

## Directory Structure

```
.
├── bds_pack_manager
│   ├── __init__.py
│   ├── main.py
│   ├── pack_handler.py
│   ├── manifest_parser.py
│   ├── json_updater.py
│   ├── utils.py
├── tests
│   ├── test_pack_handler.py
│   ├── test_manifest_parser.py
│   ├── test_json_updater.py
│   ├── test_utils.py
├── .env
├── requirements.txt
└── README.md
```

## Development

### Running Tests

To run tests, use `pytest`:

```bash
pytest
```

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Notes

- Ensure that your Bedrock Dedicated Server is properly configured before using this tool.
- Handle with care: Always back up your server before making significant changes.