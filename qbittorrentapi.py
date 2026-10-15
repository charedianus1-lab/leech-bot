# Torrent support removed: inert shim so the unchanged bot code imports cleanly.
class _Null:
    def __getattr__(self, n):
        if n == "version":
            return "removed"
        return lambda *a, **k: []
    app = property(lambda s: _Null())


def Client(*a, **k):
    return _Null()
