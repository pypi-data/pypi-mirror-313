# ZennewPy

ZennewPy is a Python package for interacting with the Zenodo API, allowing users to manage depositions, metadata, and files on Zenodo.

## Features

- Retrieve all depositions with full metadata
- Find community identifiers
- Set and unset depositions
- Create, delete, and manage depositions
- Upload and update files
- Publish depositions
- Create new versions of existing depositions
- Modify metadata for both published and unpublished depositions

## Installation

```bash
pip install zennewpy
```

## Usage

1. **Create a Zenodo access token** by first logging into your account and clicking on your username in the top right corner. Navigate to "Applications" and then "+new token" under "Personal access tokens".  Keep this window open while you proceed to step 2 because **the token is only displayed once**. Note that Sandbox.zenodo is used for testing and zenodo for production. If you want to use both, create for each a token as desribed above.
2. **Store the token** in `~/.zenodo_token` using the following command.

```sh
# zenodo token
 { echo 'ACCESS_TOKEN: your_access_token_here' } > ~/.zenodo_token

# sandbox.zenodo token
 { echo 'ACCESS_TOKEN-sandbox: your_access_token_here' } > ~/.zenodo_token
```


```python
import zennewpy

# Initialize the client
client = zennewpy.Client(sandbox=True)

# Set up your Zenodo token
# Ensure you have a ~/.zenodo_token file with your ACCESS_TOKEN


# Create a new deposition
deposition_id = client.create_new_deposition()

# Set the client to work with this deposition
client.set_deposition(deposition_id)

# Add metadata
metadata = {
    "title": "My Research Data",
    "description": "This dataset contains...",
    "upload_type": "dataset"
}
client.create_metadata(metadata)

# Upload a file
client.upload_file("path/to/your/file.csv")

# Publish the deposition
client.publish_deposition()
```

## Main Classes and Methods

### Client

The main class for interacting with Zenodo.

- `__init__(self, title=None, bucket=None, deposition_id=None, sandbox=None, token=None)`
- `get_all_depositions()`
- `set_deposition(id_value)`
- `create_new_deposition()`
- `delete_deposition(deposition_id=None)`
- `create_metadata(metadata, **kwargs)`
- `upload_file(file_path, remote_filename=None, file_id=None)`
- `publish_deposition()`
- `create_new_version()`
- `modify_metadata(metadata_updates, **kwargs)`

## Authentication

ZennewPy uses a token-based authentication system. Store your Zenodo API token in a `~/.zenodo_token` file.

## Contributing

Contributions to ZennewPy are welcome. Please ensure you follow the coding style and add unit tests for any new features.

## Acknowledgments

ZennewPy is a fork of zenodopy, an original project by L. Gloege. This
package builds upon the foundational work of the original zenodopy
library, extending and modifying its functionality while maintaining
the core API interaction principles.

## License

ZennewPy is distributed under the MIT License, which allows for free use, modification, and distribution of the software, in line with the original zenodopy project's licensing.
Key Acknowledgment: This project respectfully derives from and credits
the original zenodopy library, preserving its open-source spirit and
collaborative approach.

## Citation

If you use ZennewPy in your research, please cite it using the information provided in our CITATION.cff file. You can find this file in the root directory of our GitHub repository.
