from abc import ABC

class DjablesCell(ABC):
    def __init__(self, is_simple):
        self.is_simple = is_simple


class DjablesSimpleCell(DjablesCell):
    def __init__(self, value=None, href=None, tool_tip=None):
        self.value = value
        self.href = href
        self.tool_tip=tool_tip
        super().__init__(True)


class DjablesActionCell(DjablesCell):
    def __init__(self, actions):
        self.actions = actions
        super().__init__(False)