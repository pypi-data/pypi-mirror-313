import re

class MoreThanOneEolStyleException(Exception): pass

def nlcheck(paths):
    for path in paths:
        with open(path, 'rb') as f:
            text = f.read().decode()
        eols = set(re.findall(r'\r\n|[\r\n]', text))
        if len(eols) > 1:
            raise MoreThanOneEolStyleException(path)
