from typing                             import List
from osbot_utils.base_classes.Type_Safe import Type_Safe


class Content_Item(Type_Safe):
    title       : str
    url         : str
    date        : str
    description : str
    image_url   : str
    tags        : List[str]