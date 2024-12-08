'Show all XX''X/TO''DO/FIX''ME comments in project.'
from .files import Files
from argparse import ArgumentParser
import subprocess

def main():
    parser = ArgumentParser()
    parser.add_argument('-q', action = 'count', default = 0)
    config = parser.parse_args()
    root, = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().splitlines()
    agcommand = ['ag', '--noheading', '--nobreak']
    # XXX: Integrate with declared project resource types?
    paths = list(Files.relpaths(root, ['.py', '.pyx', '.h', '.cpp', '.ui', '.java', '.kt', '.c', '.s', '.sh', '.arid', '.aridt', '.gradle', '.java', '.mk', '.js'], ['Dockerfile', 'Makefile']))
    for tag in ['XX''X', 'TO''DO', 'FIX''ME'][config.q:]:
        subprocess.call(agcommand + [tag + ' LATER'] + paths, cwd = root)
        subprocess.call(agcommand + [tag + '(?! LATER)'] + paths, cwd = root)

if '__main__' == __name__:
    main()
