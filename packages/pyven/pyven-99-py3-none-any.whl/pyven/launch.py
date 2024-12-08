'Run project using a suitable venv from the pool.'
from .pipify import InstallDeps
from .projectinfo import ProjectInfo
from argparse import ArgumentParser
from venvpool import initlogging, Pool
import subprocess, sys

def main(): # TODO: Retire in favour of venvpool module.
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('--build', action = 'store_true', help = 'rebuild native components')
    args = parser.parse_args()
    info = ProjectInfo.seekany('.')
    _, objref = next(iter(info.console_scripts())).split('=') # XXX: Support more than just the first?
    modulename, qname = objref.split(':')
    with InstallDeps(info, False, None) as installdeps, Pool(sys.version_info.major).readonlyorreadwrite[args.build](installdeps) as venv:
        if args.build:
            venv.install(['--no-deps', '-e', info.projectdir]) # XXX: Can this be done without venv install?
        status = subprocess.call([venv.programpath('python'), '-c', "from %s import %s; %s()" % (modulename, qname.split('.')[0], qname)])
    sys.exit(status)

if '__main__' == __name__:
    main()
