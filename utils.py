# common utilities for other scripts


from tuf import repository_tool as rt
import os
import shutil

# shorthand to create keypairs
def write_and_import_keypair(keystorefolder, filename):
    pathpriv = keystorefolder + '/{}_key'.format(filename)
    pathpub = '{}.pub'.format(pathpriv)
    rt.generate_and_write_ed25519_keypair(password='pw', filepath=pathpriv)
    public_key = rt.import_ed25519_publickey_from_file(pathpub)
    private_key = rt.import_ed25519_privatekey_from_file(password='pw', filepath=pathpriv)
    return (public_key, private_key)

# loads keys from the files, should be used whenever someone wants to interact with the
# the repository (e.g. adding a new target)
def loadkey(keystorefolder, filename):
    pathpriv = keystorefolder + '/{}_key'.format(filename)
    pathpub = '{}.pub'.format(pathpriv)
    public_key = rt.import_ed25519_publickey_from_file(pathpub)
    private_key = rt.import_ed25519_privatekey_from_file(password='pw', filepath=pathpriv)
    return (public_key, private_key)

# shorthand to create full repo with all keys, only do this once
def create_repo(basefolder, keystorefolder, reponame):
    if not os.path.isdir(basefolder):
        os.mkdir(basefolder)
    os.chdir(basefolder)
    (public_root_key, private_root_key) = write_and_import_keypair(keystorefolder, 'root')
    (public_targets_key, private_targets_key) = write_and_import_keypair(keystorefolder, 'targets')
    (public_snapshots_key, private_snapshots_key) = write_and_import_keypair(keystorefolder, 'snapshot')
    (public_timestamps_key, private_timestamps_key) = write_and_import_keypair(keystorefolder, 'timestamp')
    # Bootstrap Repository
    repository = rt.create_new_repository(reponame, basefolder)
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
    # Make it happen (consistently)
    repository.mark_dirty(['root', 'snapshot', 'targets', 'timestamp'])
    repository.writeall(consistent_snapshot=True)

def load_repo(basefolder, reponame):
    os.chdir(basefolder)
    repository = rt.load_repository(reponame)
    return repository


def load_signing_keys_into_repo(repository, keystorefolder):
    (public_root_key, private_root_key) = loadkey(keystorefolder, 'root')
    (public_targets_key, private_targets_key) = loadkey(keystorefolder, 'targets')
    (public_snapshots_key, private_snapshots_key) = loadkey(keystorefolder, 'snapshot')
    (public_timestamps_key, private_timestamps_key) = loadkey(keystorefolder, 'timestamp')
    #repository.root.add_verification_key(public_root_key)
    repository.root.load_signing_key(private_root_key)
    # Add additional roles
    #repository.targets.add_verification_key(public_targets_key)
    repository.targets.load_signing_key(private_targets_key)
    #repository.snapshot.add_verification_key(public_snapshots_key)
    repository.snapshot.load_signing_key(private_snapshots_key)
    #repository.timestamp.add_verification_key(public_timestamps_key)
    repository.timestamp.load_signing_key(private_timestamps_key)


def add_target(repository, target, absolute_source, absolute_target):
    repository.status()
    # copy absolute_source into targets folder
    # Copy the source file to the targets location as TUF expects the file to already be present
    os.makedirs(os.path.dirname(absolute_target), exist_ok=True)
    shutil.copyfile(absolute_source, absolute_target)

    repository.targets.add_targets([target])
    repository.mark_dirty(['snapshot', 'targets', 'timestamp'])
    repository.writeall(consistent_snapshot=True)


def remove_target(repository, target, absolute_target):
    repository.status()
    repository.targets.remove_target(target)
    os.remove(absolute_target)
    repository.mark_dirty(['snapshot', 'targets', 'timestamp'])
    repository.writeall(consistent_snapshot=True)
