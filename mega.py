# Mega support removed (megasdk too heavy for 512MB): inert shim.
class MegaApi:
    def __init__(self, *a, **k): pass
    def getVersion(self): return "removed"
    def __getattr__(self, n):
        raise RuntimeError("Mega is not supported in this build")
class MegaListener: pass
class MegaRequest: pass
class MegaTransfer: pass
class MegaError: pass
