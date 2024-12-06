from .divcheck import commentregex
from .files import Files
from .pipify import InstallDeps
from .projectinfo import ProjectInfo, SimpleInstallDeps
from .util import bgcontainer, Excludes, initapt, pyversiontags, stderr
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from aridity.util import NoSuchPathException, openresource
from diapyr.util import singleton
from itertools import chain
from lagoon import diff
from lagoon.program import NOEOL, partial
from setuptools import find_packages
from shutil import copytree, ignore_patterns
from tempfile import NamedTemporaryFile
from venvpool import dotpy, initlogging, Pool, Task, TemporaryDirectory
import logging, os, re, shutil, subprocess, sys

log = logging.getLogger(__name__)
skip = object()

@singleton
class yesno:

    d = dict(no = False, yes = True)

    def __call__(self, s):
        return self.d[s]

def _localrepo():
    cc = ConfigCtrl()
    cc.loadsettings()
    return cc.node.buildbot.repo

def _runcheck(variant, check, *args):
    sys.stderr.write("%s[%s]: " % (check.__name__, variant))
    sys.stderr.flush()
    stderr('SKIP' if check(*args) is skip else 'OK')

class EveryVersion:

    def __init__(self, info, siblings, userepo, noseargs, docker, transient):
        self.files = Files(info.projectdir)
        self.info = info
        self.siblings = siblings
        self.userepo = userepo
        self.noseargs = noseargs
        self.docker = docker
        self.transient = transient

    def allchecks(self):
        for check in self.licheck, self.nlcheck, self.execcheck, self.divcheck, self.pyflakes, self.nose, self.readme, self.github, self.linktree:
            check()

    def licheck(self):
        from .licheck import licheck
        def g():
            excludes = Excludes(self.info.config.licheck.exclude.globs)
            for path in self.files.allsrcpaths:
                if os.path.relpath(path, self.files.root) not in excludes:
                    yield path
        _runcheck('*', licheck, self.info, list(g()))

    def nlcheck(self):
        from .nlcheck import nlcheck
        _runcheck('*', nlcheck, self.files.allsrcpaths)

    def execcheck(self):
        from .execcheck import execcheck
        _runcheck('*', execcheck, self.files.pypaths)

    def divcheck(self):
        from . import divcheck
        scriptpath = divcheck.__file__
        def divcheck():
            if pyversion >= 3:
                return skip
            subprocess.check_call(["python%s" % pyversion, scriptpath] + self.files.pypaths)
        for pyversion in self.info.config.pyversions:
            _runcheck(pyversion, divcheck)

    def pyflakes(self):
        paths = [path for excludes in [Excludes(self.info.config.flakes.exclude.globs)]
                for path in self.files.pypaths if os.path.relpath(path, self.files.root) not in excludes]
        def pyflakes():
            if paths:
                with Pool(pyversion).readonlyortransient[self.transient](SimpleInstallDeps(['pyflakes'])) as venv:
                    venv.run('check_call', [], 'pyflakes', paths)
        for pyversion in self.info.config.pyversions:
            _runcheck(pyversion, pyflakes)

    def nose(self):
        upstream_devel_packages = list(self.info.config.upstream.devel.packages)
        upstream_devel_scripts = list(self.info.config.upstream.devel.scripts) if self.userepo else []
        with InstallDeps(self.info, self.siblings, _localrepo() if self.userepo else None) as installdeps:
            installdeps.add('nose-cov', *self.info.config.test.requires) # TODO: Facility to freeze test requires tree.
            for pyversion in self.info.config.pyversions:
                reportsdir = os.path.join(self.info.projectdir, 'var', str(pyversion))
                os.makedirs(reportsdir, exist_ok = True)
                xmlpath = os.path.join(reportsdir, 'nosetests.xml')
                if self.docker:
                    coveragepath = os.path.join(self.info.projectdir, '.coverage')
                    with bgcontainer('-v', "{0}:{0}".format('/var/run/docker.sock'), '--network', 'host', '-v', "%s:%s" % (os.path.abspath(self.info.projectdir), Container.workdir), "python:%s" % pyversiontags[pyversion][0]) as container:
                        container = Container(container)
                        container.cp(installdeps.workspace, 'installdeps')
                        container.inituser()
                        if upstream_devel_packages:
                            container.initapt()
                        for command in ['apt-get', 'update'], ['apt-get', 'install', '-y', 'sudo'] + upstream_devel_packages:
                            container.call(command, check = True, root = True)
                        for script in upstream_devel_scripts:
                            from lagoon import docker
                            dirpath = docker[NOEOL]('exec', container.container, 'mktemp', '-d') # No need to cleanup, will die with container.
                            log.debug("In container dir %s run script: %s", dirpath, script)
                            docker.exec[print]('-w', dirpath, '-t', container.container, 'sh', '-c', script)
                        installdeps.cinvoke(container)
                        cpath = lambda p: os.path.relpath(p, self.info.projectdir).replace(os.sep, '/')
                        status = container.call([
                            'nosetests', '--exe', '-v',
                            '--with-doctest', '--doctest-extension', '.md',
                            '--with-xunit', '--xunit-file', cpath(xmlpath),
                            '--with-cov', '--cov-report', 'term-missing',
                        ] + sum((['--cov', p] for p in chain(find_packages(self.info.projectdir), self.info.py_modules())), []) + [cpath(p) for p in self.files.testpaths(xmlpath)] + self.noseargs)
                else:
                    coveragepath = '.coverage'
                    with Pool(pyversion).readonlyortransient[self.transient](installdeps) as venv:
                        status = venv.run('call', installdeps.localreqs, Task('''import collections
try:
    collections.Callable
except AttributeError:
    from collections.abc import Callable
    collections.Callable = Callable''', 'nose'), [
                            '--exe', '-v',
                            '--with-doctest', '--doctest-extension', '.md',
                            '--with-xunit', '--xunit-file', xmlpath,
                            '--with-cov', '--cov-report', 'term-missing',
                        ] + sum((['--cov', p] for p in chain(find_packages(self.info.projectdir), self.info.py_modules())), []) + self.files.testpaths(xmlpath) + self.noseargs)
                if os.path.exists(coveragepath):
                    shutil.copy2(coveragepath, os.path.join(reportsdir, 'coverage')) # Replace whatever the status, as if we configured the location.
                    os.remove(coveragepath) # Can't simply use rename cross-device in release case.
                assert not status

    def readme(self):
        def first(scope, resolvable):
            for _, o in resolvable.resolve(scope).resolveditems():
                return o
            raise NoSuchPathException('Empty set.')
        def getpydoc(mainmodules):
            from lagoon import pydoc_markdown
            with TemporaryDirectory() as pydocparent:
                pydocdir = os.path.join(pydocparent, 'project')
                copytree(self.info.projectdir, pydocdir, ignore = ignore_patterns('test_*'))
                internal = {(os.path.dirname(mm.relpath) if '__init__.py' == os.path.basename(mm.relpath) else mm.relpath[:-len(dotpy)]).replace(os.sep, '.') for mm in mainmodules}
                internal.update(self.info.config.internal_module)
                modules = []
                for dirpath, dirnames, filenames in os.walk(pydocdir):
                    for name in filenames:
                        if name.endswith(dotpy):
                            pypath = os.path.join(dirpath, name)
                            with open(pypath, 'r+') as f:
                                text = f.read()
                                cleantext = re.sub(commentregex, '', text, flags = re.MULTILINE)
                                if cleantext != text:
                                    f.seek(0)
                                    f.write(cleantext)
                                    f.truncate()
                            modules.append(os.path.relpath(dirpath if '__init__.py' == name else pypath[:-len(dotpy)], pydocdir).replace(os.sep, '.'))
                acc = re.sub('^#', '###', pydoc_markdown('--search-path', pydocdir), flags = re.MULTILINE)
                acc = re.split('(?=^<a id="(?:%s)")' % '|'.join(map(re.escape, modules)), acc, flags = re.MULTILINE) # Module names are markup attribute-safe.
                return ''.join(sorted(block for block in acc if block and re.search('"([^"]+)', block).group(1) not in internal))
        def readme():
            if not (self.info.config.github.participant or self.info.config.pypi.participant):
                return skip
            config = (-self.info.config).childctrl().node
            config.first = first
            if self.info.config.readme_verbose:
                config.verbose_blank = ''
            (-config).execute('commands * name = $label()')
            mainmodules = sorted(self.info.mainmodules(), key = lambda mm: mm.command)
            undocumented = [mm.command for mm in mainmodules if mm.doc is None]
            if undocumented:
                raise Exception("Undocumented: %s" % undocumented)
            for mm in mainmodules:
                (-config).printf("commands %s doc = %s", mm.command, mm.doc)
            if self.info.config.pydoc_enabled:
                config.pydoc = getpydoc(mainmodules)
            with NamedTemporaryFile('w') as g:
                with openresource(__name__, 'README.md.aridt') as f:
                    (-config).processtemplate(f, g)
                g.flush()
                completed = diff(g.name, os.path.join(self.info.projectdir, 'README.md'), check = False)
                sys.stdout.write(completed.stdout)
                assert completed.returncode in {0, 1}
                assert all('<' != l[0] for l in completed.stdout.splitlines())
        _runcheck('*', readme)

    def github(self):
        def github():
            if not self.info.config.github.participant:
                return skip
            description, _ = self.info.descriptionandurl()
            assert self.info.config.tagline == description
        _runcheck('*', github)

    def linktree(self):
        def linktree():
            account = self.info.config.linktree.account
            if account is None:
                return skip
            from urllib.request import urlopen
            from xml.sax.saxutils import escape
            with urlopen("https://linktr.ee/%s" % account) as f: # TODO: Percent-encode.
                assert ">%s \N{BULLET} %s<" % tuple(map(escape, [self.info.config.name, self.info.config.tagline])) in f.read().decode('utf-8') # TODO: Deduce encoding, consider lagoon URL.
        _runcheck('*', linktree)

class Container:

    workdir = '/io'

    def __init__(self, container):
        from lagoon import id
        self.uid = int(id._u())
        self.gid = int(id._g())
        self.container = container

    def inituser(self):
        from lagoon import docker
        docker('exec', self.container, 'groupadd', '-g', os.stat('/var/run/docker.sock').st_gid, 'docker', stdout = None)
        docker('exec', self.container, 'groupadd', '-g', self.gid, 'pyvengroup', stdout = None)
        docker('exec', self.container, 'useradd', '-g', self.gid, '-G', 'docker', '-u', self.uid, '-m', 'pyvenuser', stdout = None)

    def initapt(self):
        from lagoon import docker
        initapt(docker[partial]('exec', self.container, stdout = None))

    def install(self, args):
        from lagoon import docker
        if args:
            docker('exec', '-w', self.workdir, self.container, 'pip', 'install', *args, stdout = None)

    def call(self, args, check = False, root = False):
        from lagoon import docker
        return docker('exec', '-w', self.workdir, self.container, *([] if root else ['sudo', '-u', 'pyvenuser']) + args, stdout = None, check = check)

    def cp(self, src, dest):
        from lagoon import docker
        docker.cp[print](src, f"{self.container}:{dest}")

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('--docker', action = 'store_true')
    parser.add_argument('--repo', type = yesno, default = True)
    parser.add_argument('--siblings', type = yesno, default = True)
    parser.add_argument('--transient', action = 'store_true')
    args, noseargs = parser.parse_known_args()
    EveryVersion(ProjectInfo.seekany('.'), args.siblings, args.repo, noseargs, args.docker, args.transient).allchecks()
