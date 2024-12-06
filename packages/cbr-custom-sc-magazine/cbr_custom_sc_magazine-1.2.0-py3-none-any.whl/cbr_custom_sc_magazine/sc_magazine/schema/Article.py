from cbr_custom_sc_magazine.sc_magazine.schema.Content_Item  import Content_Item

class Article(Content_Item):
    author  : str
    content : str
    category: str
