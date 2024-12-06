# Nomad Media CLI Tool

Command line interface for managing Nomad Media media assets.

## Installation

The current Nomad Media CLI is in a testing state. As such, you have to include the version # when installing.

```bash
// Fresh installation
pip install nomad-media-cli==0.0.1a14

// Upgrade
pip install --upgrade nomad-media-cli==0.0.1a14
```

## Configuration

The Nomad Media CLI stores some data locally for the SDK configuration. The location depends on the platform of your OS:

- Default config location: 
  - **Windows**: `%APPDATA%\Local\nomad_media_cli\config.json`
  - **Linux**: `~/.config/nomad_media_cli/config.json`
  - **Mac**: `~/Library/Application Support/nomad_media_cli/config.json`
- Custom config location: Use --config-path option.

## Commands

### init

Initializes CLI configuration

Options:

- `--service-api-url`: API endpoint URL (required)
- `--api-type`: API type [admin|portal]

## login

Logs into Nomad with given credentials

Options:

- `--username`: Username used for credentials. 
- `--password`: Password used for credentials.

### list-config-path

Outputs the local OS location where the config file is stored.

### update-config

Updates CLI configuration

Options:

- `--service-api-url`: API endpoint URL
- `--api-type`: API type [admin|portal]

### list-assets

List assets by id, Nomad URL or object-key. You should only specify **one **of the optional parameters.

Options:

- `--id`: Asset ID, collection id, or saved search id to list the assets for.
- `--url`: The Nomad URL of the Asset (file or folder) to list the assets for (bucket::object_key).
- `--object_key`: Object-key only of the Asset (file or folder) to list the assets for. This option assumes the default bucket that was previously set with the set-bucket\` command.

### upload-assets

Uploads a file or folder from the local OS to the Nomad asset storage. You should only specify **one **of the optional parameters for id, url or object-key. 

Options:

- `-r`: Recursive upload.
- `--source`: Local OS file or folder path specifying the files or folders to upload. For example: file.jpg or folderName/file.jpg.
- `--id`: Nomad ID of the Asset Folder to upload the source file(s) and folder(s) into.
- `--url`: The Nomad URL of the Asset folder to upload the source files/folders into (bucket::object_key).
- `--object_key`: Object-key only of the Asset folder to upload the source files/folders into. This option assumes the default bucket that was previously set with the set-bucket\` command.

### list-buckets

Lists all of the buckets registered in the Nomad instance.

### set-bucket

Sets the default bucket for use in the commands that take the object_key property. Note this must be set before using the other commands.

Options:

- `--bucket`: Name of the default bucket to set in config.

## Future Commands

### list-tags

Lists all of the tags

Options:

- `--size`: The number of results shown. Default is 10.
- `--offset`: The offset of the page.

### add-tag

Add the tag(s) to an asset.

Options:

- `--tag`: Name of the tag(s) to set in config. Use multiple flags for multiple tags.
- `--id`: Id of the asset to add the tag(s) to.
- `--createNew`: Create a new tag if the tag doesn't exits.