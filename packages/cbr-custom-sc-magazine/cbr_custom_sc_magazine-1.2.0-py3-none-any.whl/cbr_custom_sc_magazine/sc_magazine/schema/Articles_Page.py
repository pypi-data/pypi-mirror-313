from typing                                             import List
from osbot_utils.base_classes.Type_Safe                 import Type_Safe
from cbr_custom_sc_magazine.sc_magazine.schema.Article  import Article

class Articles_Page(Type_Safe):
    articles : List[Article]