import os

execmask = 0x49
magic = '#!'

def execcheck(paths):
    for path in paths:
        basename = os.path.basename(path)
        executable = bool(os.stat(path).st_mode & execmask)
        with open(path) as f:
            hasmagic = f.readline().startswith(magic)
        if basename.lower().startswith('test'):
            if not basename.startswith('test_'):
                raise Exception("Inconsistent name: %s" % path) # Note pyflakes already checks for duplicate method names.
            if executable:
                raise Exception("Should not be executable: %s" % path)
            if hasmagic:
                raise Exception("Using %s is obsolete: %s" % (magic, path))
        else:
            if executable != hasmagic:
                raise Exception(path)
