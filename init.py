# Set up new repository

from tuf import repository_tool as rt
import os
import shutil

# shorthand to create keypairs
def write_and_import_keypair(filename):
    pathpriv = 'tufkeystore/{}_key'.format(filename)
    pathpub = '{}.pub'.format(pathpriv)
    rt.generate_and_write_ed25519_keypair(password='pw', filepath=pathpriv)
    public_key = rt.import_ed25519_publickey_from_file(pathpub)
    private_key = rt.import_ed25519_privatekey_from_file(password='pw', filepath=pathpriv)
    return (public_key, private_key)

# shorthand to create full repo with all keys, only do this once
def create_repo(repo_dir):
    os.mkdir(repo_dir)
    os.chdir(repo_dir)
    (public_root_key, private_root_key) = write_and_import_keypair('root')
    (public_targets_key, private_targets_key) = write_and_import_keypair('targets')
    (public_snapshots_key, private_snapshots_key) = write_and_import_keypair('snapshot')
    (public_timestamps_key, private_timestamps_key) = write_and_import_keypair('timestamp')
    # Bootstrap Repository
    repository = rt.create_new_repository("tufrepo", repo_dir)
    repository.root.add_verification_key(public_root_key)
    repository.root.load_signing_key(private_root_key)
    # Add additional roles
    repository.targets.add_verification_key(public_targets_key)
    repository.targets.load_signing_key(private_targets_key)
    repository.snapshot.add_verification_key(public_snapshots_key)
    repository.snapshot.load_signing_key(private_snapshots_key)
    repository.timestamp.add_verification_key(public_timestamps_key)
    repository.timestamp.load_signing_key(private_timestamps_key)
    repository.status()
    # Make it so (consistently)
    repository.mark_dirty(['root', 'snapshot', 'targets', 'timestamp'])
    repository.writeall(consistent_snapshot=True)

create_repo('tuf-testrepo')
