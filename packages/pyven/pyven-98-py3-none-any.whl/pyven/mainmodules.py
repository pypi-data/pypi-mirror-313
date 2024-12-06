from venvpool import checkpath, commandornone, dotpy as extension, scriptregex
import ast, logging, os, re, sys

log = logging.getLogger(__name__)

def _lastiflineno(text):
    for i, l in reversed(list(enumerate(text.splitlines()))):
        if re.search(scriptregex, l) is not None:
            return 1 + i

def _funcpath(func):
    v = []
    while True:
        try:
            v.append(func.id)
            return '.'.join(reversed(v))
        except AttributeError:
            v.append(func.attr)
            func = func.value

def main():
    logging.basicConfig()
    paths = sys.argv[1:]
    projectdir = paths.pop(0)
    for relpath in paths:
        fullpath = os.path.join(projectdir, relpath)
        if not checkpath(projectdir, fullpath):
            continue
        with open(fullpath) as f:
            text = f.read()
        iflineno = _lastiflineno(text)
        if iflineno is None:
            continue
        command = commandornone(fullpath)
        if command is None:
            continue
        try:
            m = ast.parse(text)
        except SyntaxError:
            log.warning("Skip: %s" % relpath, exc_info = True)
            continue
        result = dict(
            command = command,
            doc = ast.get_docstring(m),
            relpath = relpath,
        )
        ifstatement, = (obj for obj in m.body if iflineno == obj.lineno)
        expr, = ifstatement.body
        call = expr.value
        if call.args or call.keywords:
            log.warning("Bad call: %s", command)
        else:
            result['console_script'] = "%s=%s:%s" % (command, relpath[:-len(extension)].replace(os.sep, '.'), _funcpath(call.func))
        print(result)

if ('__main__' == __name__):
    main()
