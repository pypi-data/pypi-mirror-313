from typing                             import List
from osbot_utils.base_classes.Type_Safe import Type_Safe

class Menu_Item(Type_Safe):
    text     : str
    url      : str
    children : List #['MenuItem']
    is_active: bool = False


    def has_children(self) -> bool:
        """Check if menu item has child items"""
        return bool(self.children)
