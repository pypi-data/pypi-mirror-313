from itertools import chain
import glob, json

policyglobs = [
    '/opt/_internal/*/lib/python3.7/site-packages/auditwheel/policy/policy.json',
    '/opt/_internal/pipx/venvs/auditwheel/lib/python3.1?/site-packages/auditwheel/policy/manylinux-policy.json',
]
syslibs = 'libasound.so.2', 'libjack.so.0', 'libportaudio.so.2'

def main():
    policypath, = chain(*map(glob.iglob, policyglobs))
    with open(policypath) as f:
        policy = json.load(f)
    for edition in policy:
        if edition['name'].startswith('manylinux'):
            edition['lib_whitelist'].extend(syslibs)
    with open(policypath, 'w') as f:
        json.dump(policy, f)

if ('__main__' == __name__):
    main()
