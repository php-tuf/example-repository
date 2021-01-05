#!/usr/bin/env python3

# Removes an existing target file from a repository

# import our own "utils" module
from utils import *
import sys
from os import *

# base variables,
# @todo should be configurable via argv
basefolder = 'tuf-testrepo'
keystore = 'tufkeystore'
reponame = 'tufrepo'

target_location = sys.argv[1]
absolute_target = os.path.abspath(os.path.join(basefolder, reponame, 'targets', target_location));

print('Load existing TUF repository')
repository = load_repo(basefolder, reponame)

print('Load signing keys into repo')
load_signing_keys_into_repo(repository, keystore)

print('Removing target ', target_location, ' from repo')
remove_target(repository, target_location, absolute_target)