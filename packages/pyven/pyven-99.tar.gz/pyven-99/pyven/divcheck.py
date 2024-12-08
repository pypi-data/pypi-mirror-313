import ast, re, sys

commentregex = ' \N{NUMBER SIGN} .+'

def main():
    for path in sys.argv[1:]:
        with open(path) as f:
            text = f.read()
        for node in ast.walk(ast.parse(text)):
            if 'Div' == type(node).__name__:
                hasdiv = True
                break
        else:
            hasdiv = False
        if hasdiv == (re.search("^from __future__ import division(?:%s)?$" % commentregex, text, flags = re.MULTILINE) is None):
            raise Exception(path)

if ('__main__' == __name__):
    main()
