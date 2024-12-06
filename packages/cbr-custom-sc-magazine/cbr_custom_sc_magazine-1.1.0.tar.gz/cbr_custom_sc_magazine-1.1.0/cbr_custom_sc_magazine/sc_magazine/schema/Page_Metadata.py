from osbot_utils.base_classes.Type_Safe import Type_Safe


class Page_Metadata(Type_Safe):
    title          : str
    description    : str
    og_title       : str
    og_description : str
    og_image       : str
    twitter_card   : str
    canonical_url  : str

    # def __post_init__(self):
    #     if not self.title:
    #         raise ValueError("Page title is required")
    #     # Set OpenGraph defaults if not provided
    #     if not self.og_title:
    #         self.og_title = self.title
    #     if not self.og_description:
    #         self.og_description = self.description
