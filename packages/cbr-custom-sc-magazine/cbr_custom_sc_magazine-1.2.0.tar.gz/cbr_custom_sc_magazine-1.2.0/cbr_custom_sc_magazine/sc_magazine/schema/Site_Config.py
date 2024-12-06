from typing                                                import List
from osbot_utils.base_classes.Type_Safe                    import Type_Safe
from cbr_custom_sc_magazine.sc_magazine.schema.Social_Link import Social_Link
from cbr_custom_sc_magazine.sc_magazine.schema.Navigation  import Navigation

class Site_Config(Type_Safe):

    site_name      : str = "SC Media UK"
    logo_url       : str
    analytics_id   : str
    social_accounts: List[Social_Link]
    navigation     : Navigation
