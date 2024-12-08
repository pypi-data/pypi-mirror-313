from aridity.model import Function, wrap

def fwrap(scope, fresolvable):
    def g(scope, *resolvables):
        return wrap(fresolvable.resolve(scope).scalar(*(r.resolve(scope).scalar for r in resolvables)))
    return Function(g)
