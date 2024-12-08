'Print project.arid snippet pinning requires to their minimum allowed versions.'
from .projectinfo import ProjectInfo
from venvpool import initlogging

def main():
    initlogging()
    print("requires = $list(%s)" % ' '.join(r.minstr() for r in ProjectInfo.seek('.').parsedrequires()))

if '__main__' == __name__:
    main()
