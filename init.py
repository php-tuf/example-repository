#!/usr/bin/env python3

# Set up new repository
# should only be called once

# import our own "utils" module
from utils import *
import sys

# base variables, should be configurable via argv
basefolder = 'tuf-testrepo'
# keystore folder is expected to be put inside the repo folder
keystore = 'tufkeystore'
reponame = 'tufrepo'

create_repo(basefolder, keystore, reponame)