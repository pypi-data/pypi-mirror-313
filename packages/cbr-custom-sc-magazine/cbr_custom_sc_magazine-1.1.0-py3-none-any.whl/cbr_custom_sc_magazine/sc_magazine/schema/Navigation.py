from typing                                                import List
from osbot_utils.base_classes.Type_Safe                    import Type_Safe
from cbr_custom_sc_magazine.sc_magazine.schema.Menu_Item   import Menu_Item
from cbr_custom_sc_magazine.sc_magazine.schema.Social_Link import Social_Link

class Navigation(Type_Safe):
    main_menu   : List[Menu_Item  ]
    social_links: List[Social_Link]
