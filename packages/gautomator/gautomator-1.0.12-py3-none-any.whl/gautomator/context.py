

class Context(object):

    """
    Set of supported context strategies.
    """

    UE_UMG = "umg"
    UE_SLATE = "slate"
    UE_ACTOR = "UE_ACTOR"
    UNITY_GAMEOBJECT = "UNITY_GAMEOBJECT"

    #Special contexts:
    CURRENT_CONTEXT = "CURRENT_CONTEXT"
    INVALID_CONTEXT = "INVALID_CONTEXT"
    ALL_CONTEXTS = "ALL_CONTEXTS"

    def __init__(self):
        self._context= Context.INVALID_CONTEXT

    @property
    def context(self) -> str:
        return self._context

    @property
    def current_context(self) -> str:
        return self._context

    @context.setter
    def context(self, value):
        self._context = value