'Generate setuptools files for a project.arid project.'
from .projectinfo import ProjectInfo, Req, SimpleInstallDeps
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from diapyr.util import bfs
from pkg_resources import resource_filename
from tempfile import mkdtemp
from venvpool import initlogging, Pool
import logging, os, shutil, subprocess, sys

log = logging.getLogger(__name__)

def pipify(info, version = None):
    release = version is not None
    # Allow release of project without origin:
    if release:
        if info.config.github.participant:
            _, url = info.descriptionandurl()
        elif info.config.pypi.participant:
            url = "https://pypi.org/project/%s/" % info.config.name
        else:
            raise Exception
    else:
        url = None
    cc = ConfigCtrl()
    cc.execute('''py_modules := $list()
install_requires := $list()
console_scripts := $list()
''')
    cc.w.name = info.config.name
    cc.w.tagline = info.config.tagline
    for t in info.config.resource.types:
        cc.w.resource.types += t
    cc.w.version = version if release else info.devversion()
    cc.w.description = info.config.tagline
    cc.w.long_description = 'long_description()' if release else repr(None)
    cc.w.url = url
    cc.w.author = info.config.author if release else None
    cc.w.author_email = info.config.author_email if release else None
    for m in info.py_modules():
        cc.w.py_modules += m
    for r in info.allrequires:
        cc.w.install_requires += r
    for s in info.console_scripts():
        cc.w.console_scripts += s
    cc.w.universal = int({2, 3} <= set(info.config.pyversions))
    # XXX: Use soak to generate these?
    tasks = [
        ['setup.py', 'setup.py.aridt', 'pystr'],
        ['setup.cfg', 'setup.cfg.aridt', 'void'],
    ]
    @bfs(info.allbuildrequires)
    def proc(bfsinfo, name):
        cc.w.build_requires += name
    if proc.donekeys != {'setuptools', 'wheel'}:
        tasks.append(['pyproject.toml', 'pyproject.toml.aridt', 'tomlquote'])
    for name, template, quote in tasks:
        cc.printf('" = $(%s)', quote)
        cc.processtemplate(
                resource_filename(__name__, template), # TODO LATER: Make aridity get the resource.
                os.path.abspath(os.path.join(info.projectdir, name)))

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('--transient', action = 'store_true')
    parser.add_argument('--version')
    parser.add_argument('projectdir', nargs = '?') # FIXME: When projectdir is passed in its console_scripts are not populated!
    args = parser.parse_args()
    info = ProjectInfo.seek('.') if args.projectdir is None else ProjectInfo(args.projectdir, os.path.join(args.projectdir, ProjectInfo.projectaridname))
    pipify(info, args.version)
    setupcommand(info, sys.version_info.major, args.transient, 'egg_info')

def setupcommand(info, pyversion, transient, *command):
    def setup(absexecutable):
        subprocess.check_call([absexecutable, 'setup.py'] + list(command), cwd = info.projectdir)
    if {'setuptools', 'wheel'} == set(info.allbuildrequires) and sys.version_info.major == pyversion:
        setup(sys.executable)
    else:
        with Pool(pyversion).readonlyortransient[transient](SimpleInstallDeps(info.allbuildrequires)) as venv:
            setup(venv.programpath('python'))

class VolatileReq:

    @property
    def namepart(self):
        return self.info.config.name

    def __init__(self, info):
        self.info = info

    def acceptversion(self, versionstr):
        return self.info.devversion() == versionstr

class InstallDeps:

    @property
    def pypireqs(self):
        return [VolatileReq(i) for i in self.volatileprojects] + self.fetchreqs

    def __init__(self, info, siblings, localrepo):
        self.info = info
        self.siblings = siblings
        self.localrepo = localrepo

    def __enter__(self):
        self.workspace = mkdtemp()
        editableprojects = {}
        volatileprojects = {}
        pypireqs = []
        def adddeps(i, root):
            for r in i.parsedrequires():
                name = r.namepart
                if name in editableprojects or name in volatileprojects:
                    continue
                if self.siblings:
                    siblingpath = r.siblingpath(i.contextworkspace())
                    if os.path.exists(siblingpath):
                        editableprojects[name] = j = ProjectInfo.seek(siblingpath)
                        yield j, True
                        continue
                if self.localrepo is not None:
                    repopath = os.path.join(self.localrepo, "%s.git" % name)
                    if os.path.exists(repopath):
                        if self.siblings:
                            log.warning("Not a sibling, install from repo: %s", name)
                        clonepath = os.path.join(self.workspace, name)
                        subprocess.check_call(['git', 'clone', '--depth', '1', "file://%s" % repopath, clonepath])
                        subprocess.check_call(['git', 'fetch', '--tags'], cwd = clonepath)
                        volatileprojects[name] = j = ProjectInfo.seek(clonepath)
                        yield j, False
                        continue
                if root: # Otherwise pip will handle it.
                    pypireqs.append(r.reqstr)
        @bfs([(self.info, True)])
        class Proc:
            def newdepth(self):
                log.debug("Examine deps of: %s", ', '.join(i.config.name for i, _ in self.currentkeys))
            def process(self, t):
                return adddeps(*t)
        for i in volatileprojects.values(): # Assume editables already pipified.
            pipify(i)
        self.localreqs = [i.projectdir for i in editableprojects.values()]
        self.volatileprojects = volatileprojects.values()
        self.fetchreqs = list(Req.published(pypireqs))
        return self

    def add(self, *requires):
        self.fetchreqs.extend(Req.parselines(requires))

    def invoke(self, venv):
        venv.install([i.projectdir for i in self.volatileprojects] + [r.reqstr for r in self.fetchreqs])

    def cinvoke(self, container):
        container.install(["/installdeps/%s" % os.path.relpath(i.projectdir, self.workspace).replace(os.sep, '/') for i in self.volatileprojects] + [r.reqstr for r in self.fetchreqs])

    def __exit__(self, *exc_info):
        shutil.rmtree(self.workspace)

if '__main__' == __name__:
    main()
