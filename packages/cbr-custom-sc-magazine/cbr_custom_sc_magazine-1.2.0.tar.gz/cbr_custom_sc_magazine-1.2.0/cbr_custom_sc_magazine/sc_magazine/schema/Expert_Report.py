from typing                                                 import List
from cbr_custom_sc_magazine.sc_magazine.schema.Content_Item import Content_Item

class Expert_Report(Content_Item):
    file_url    : str
    file_type   : str
    authors     : List[str]

