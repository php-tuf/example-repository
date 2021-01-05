# Example Repository

This repository is a first python3-based proof-of-concept to
set up a server-side repository as an example.


## Setup for Python 3.9

	pipenv install

## Usage

Setting up a new repo: './init.py'

Adding a target to a repo: './add_target.py /path/to/my-file.tar.gz project-name/my-file.tar.gz'

Removing an existing target from the repo: './remove_target.py project-name/my-file.tar.gz'

## Next steps

* Make the basic folders and paths configurable via argv
* Set up the keys outside of the folders
* Add commands for removing / invalidating keys
* Consider hashed bins
