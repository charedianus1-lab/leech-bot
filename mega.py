# Mega support removed (megasdk too heavy for 512MB): inert shim.
class _Any(type):
    def __getattr__(cls, n):
        return 0

class MegaApi:
    def __init__(self, *a, **k): pass
    def getVersion(self): return "removed"
    def __getattr__(self, n):
        raise RuntimeError("Mega is not supported in this build")

class MegaListener(metaclass=_Any): pass
class MegaRequest(metaclass=_Any): pass
class MegaTransfer(metaclass=_Any): pass
class MegaError(metaclass=_Any): pass
