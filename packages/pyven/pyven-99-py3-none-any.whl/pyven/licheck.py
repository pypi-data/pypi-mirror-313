import hashlib, os, re, shlex, sys

gpltemplate = """# Copyright %(years)s %(author)s

# This file is part of %(name)s.
#
# %(name)s is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# %(name)s is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with %(name)s.  If not, see <http://www.gnu.org/licenses/>.
"""
intersection = '''# This file incorporates work covered by the following copyright and
# permission notice:
'''

def _hassuffix(name, *suffixes):
    return name.endswith(suffixes) or name.endswith(tuple("%s.aridt" % s for s in suffixes))

def _checkmd5(info, name, expected):
    licpath = os.path.join(info.projectdir, name)
    md5 = hashlib.md5()
    with open(licpath) as f:
        md5.update(f.read().encode('utf_8'))
    if expected != md5.hexdigest():
        raise Exception(licpath)

def licheck(info, paths):
    if not info.config.licheck.enabled:
        sys.stderr.write('SKIP ')
        return
    sections = []
    for name in info.config.licenses:
        if sections:
            sections.append(intersection)
        if 'GPL' == name:
            sections.append(gpltemplate % {
                'years': ', '.join(str(y) for y in info.config.years),
                'author': info.config.author,
                'name': info.config.name,
            })
        elif 'MIT' == name:
            with open(info.mitpath()) as f:
                sections.append(''.join(('# ' if l.rstrip() else '#') + l for l in f))
        elif 'UNLICENSE' == name:
            pass
        else:
            raise Exception(name)
    master = ''.join(s + '\n' for s in sections) # Check each section ends with 2 newlines.
    def checkone(path):
        with open(path) as f:
            text = f.read()
        if text.startswith('#!'):
            for _ in range(2):
                text = text[text.index('\n') + 1:]
        if _hassuffix(path, '.s'):
            text = re.sub('^;', '#', text, flags = re.MULTILINE)
        elif _hassuffix(path, '.h', '.cpp', '.cxx', '.gradle', '.java'):
            text = re.sub('^//', '#', text, flags = re.MULTILINE)
        elif _hassuffix(path, '.arid'):
            text = re.sub('^:', '#', text, flags = re.MULTILINE)
        return master == text[:len(master)]
    badpaths = [p for p in paths if not checkone(p)]
    if badpaths:
        raise Exception(' '.join(map(shlex.quote, badpaths)))
    if 'GPL' in info.config.licenses:
        _checkmd5(info, 'COPYING', 'd32239bcb673463ab874e80d47fae504')
    if 'UNLICENSE' in info.config.licenses:
        _checkmd5(info, 'UNLICENSE', '7246f848faa4e9c9fc0ea91122d6e680')
