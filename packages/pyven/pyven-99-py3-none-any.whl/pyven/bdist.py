from argparse import ArgumentParser
from glob import iglob
from tempfile import mkdtemp
import logging, os, shutil, subprocess

log = logging.getLogger(__name__)
distdir = 'dist'

def main():
    logging.basicConfig(format = "<%(levelname)s> %(message)s", level = logging.DEBUG)
    parser = ArgumentParser()
    parser.add_argument('--plat', required = True)
    parser.add_argument('pyversions', nargs = '+')
    args = parser.parse_args()
    holder = mkdtemp()
    try:
        for pip in sorted(iglob("/opt/python/cp[%s]*/bin/pip" % ''.join(args.pyversions))):
            compatibility = pip.split(os.sep)[3]
            log.info("Make wheel(s) for implementation-ABI: %s", compatibility)
            try:
                subprocess.check_call([pip, '--no-cache-dir', 'wheel', '--no-deps', '-w', holder, '.'])
            except subprocess.CalledProcessError:
                log.warning('Skip compatibility:', exc_info = True)
                continue
            wheelpath, = (os.path.join(holder, n) for n in os.listdir(holder))
            subprocess.check_call(['auditwheel', 'repair', '--plat', args.plat, '-w', distdir, wheelpath])
            plaintarget = os.path.join(distdir, os.path.basename(wheelpath))
            if os.path.exists(plaintarget):
                log.info("Replace plain wheel: %s", plaintarget)
            shutil.copy2(wheelpath, distdir)
            os.remove(wheelpath)
    finally:
        shutil.rmtree(holder)

if ('__main__' == __name__):
    main()
