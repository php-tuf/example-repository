# Set up new repository

from tuf import repository_tool as rt
import os
import shutil


def loadkey(filename):
    pathpriv = 'tufkeystore/{}_key'.format(filename)
    pathpub = '{}.pub'.format(pathpriv)
    public_key = rt.import_ed25519_publickey_from_file(pathpub)
    private_key = rt.import_ed25519_privatekey_from_file(password='pw', filepath=pathpriv)
    return (public_key, private_key)

def add_target(repo_dir, target):
    os.chdir(repo_dir)
    repository = rt.load_repository('tufrepo')
    (public_root_key, private_root_key) = loadkey('root')
    (public_targets_key, private_targets_key) = loadkey('targets')
    (public_snapshots_key, private_snapshots_key) = loadkey('snapshot')
    (public_timestamps_key, private_timestamps_key) = loadkey('timestamp')
    #repository.root.add_verification_key(public_root_key)
    repository.root.load_signing_key(private_root_key)
    # Add additional roles
    #repository.targets.add_verification_key(public_targets_key)
    repository.targets.load_signing_key(private_targets_key)
    #repository.snapshot.add_verification_key(public_snapshots_key)
    repository.snapshot.load_signing_key(private_snapshots_key)
    #repository.timestamp.add_verification_key(public_timestamps_key)
    repository.timestamp.load_signing_key(private_timestamps_key)
    repository.status()
    repository.targets.add_targets([target])
    # Make it so (consistently)
    repository.mark_dirty(['root', 'snapshot', 'targets', 'timestamp'])
    repository.writeall(consistent_snapshot=True)

add_target('tuf-testrepo', 'my-file.txt')
